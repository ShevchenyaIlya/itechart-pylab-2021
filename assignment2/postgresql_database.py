import json

import psycopg2
from psycopg2.extensions import AsIs


def load_database_connection_settings():
    with open("db_connection_setting.json") as json_file:
        return json.load(json_file)


def database_connection(connection_settings):
    return psycopg2.connect(**connection_settings)


def load_query(filename):
    with open(filename, "r") as sql_query:
        return sql_query.read()


class PostgreSQLHandler:
    def __init__(self):
        self.connection = database_connection(load_database_connection_settings())
        self.cursor = self.connection.cursor()
        self.sql_queries = {}

    def __del__(self):
        self.close_connection()

    def get_query(self, query: str):
        if not self.sql_queries.get(query, False):
            self.sql_queries[query] = load_query("".join(["sql/", query, ".sql"]))

        return self.sql_queries[query]

    def update(self, post):
        self.update_post(post)
        self.update_user(post)

    def delete(self, unique_id):
        if self.post_exist(unique_id):
            self.delete_post(unique_id)
            self.delete_user(unique_id)
            return True

        return False

    def insert(self, post):
        if not self.user_exist(post["username"]):
            self.cursor.execute(
                self.get_query("insert_user"),
                (
                    post["username"],
                    post["user_karma"],
                    post["user_cake_day"],
                    post["post_karma"],
                    post["comment_karma"],
                ),
            )

        if not self.category_exist(post["post_category"]):
            self.cursor.execute(
                self.get_query("insert_category"), (post["post_category"],)
            )

        self.cursor.execute(
            self.get_query("insert_post"),
            (
                post["unique_id"],
                post["post_url"],
                post["post_date"],
                post["comments_number"],
                post["votes_number"],
                post["post_category"],
                post["username"],
            ),
        )

        self.connection.commit()

    def delete_post(self, unique_id):
        self.cursor.execute(self.get_query("delete_post"), (unique_id,))
        self.connection.commit()

    def delete_user(self, unique_id):
        self.cursor.execute(
            self.get_query("delete_user"),
            (unique_id,),
        )
        self.connection.commit()

    def update_post(self, post):
        self.cursor.execute(
            self.get_query("update_post"),
            (
                post["post_date"],
                post["post_url"],
                post["comments_number"],
                post["votes_number"],
                post["post_category"],
                post["username"],
                post["unique_id"],
            ),
        )
        self.connection.commit()

    def update_user(self, post):
        self.cursor.execute(
            self.get_query("update_user"),
            (
                post["user_karma"],
                post["user_cake_day"],
                post["post_karma"],
                post["comment_karma"],
                post["username"],
            ),
        )
        self.connection.commit()

    def select_all_posts(self, page_size=0, **kwargs):
        if page_size == 0:
            self.cursor.execute(self.get_query("select_all_posts"))
        else:
            self.cursor.execute(
                self.get_query("select_all_posts_with_filters"),
                (
                    kwargs.get("post_category", None),
                    kwargs.get("post_date", None),
                    kwargs.get("votes_number_from", None),
                    kwargs.get("votes_number_to", None),
                    AsIs(kwargs.get("sorting_field", "post_date")),
                    AsIs(kwargs.get("order", "ASC")),
                    page_size,
                    int(kwargs.get("page", 0)) * page_size,
                ),
            )

        rows = self.cursor.fetchall()
        return [convert_selected_data(row) for row in rows]

    def select_single_post(self, unique_id):
        self.cursor.execute(
            self.get_query("select_one_post"),
            (unique_id,),
        )

        row = self.cursor.fetchall()
        if row:
            return convert_selected_data(row[0])

    def entry_count(self):
        self.cursor.execute(self.get_query("row_count"))
        return self.cursor.fetchall()[0][0]

    def posts_categories(self):
        self.cursor.execute(self.get_query("select_all_categories"))
        return self.cursor.fetchall()

    def post_exist(self, unique_id):
        self.cursor.execute(self.get_query("post_exists"), (unique_id,))
        return self.cursor.fetchall()[0][0]

    def user_exist(self, username):
        self.cursor.execute(self.get_query("user_exists"), (username,))
        return self.cursor.fetchall()[0][0]

    def category_exist(self, category):
        self.cursor.execute(self.get_query("category_exists"), (category,))
        return self.cursor.fetchall()[0][0]

    def close_connection(self):
        self.connection.close()


def convert_selected_data(row):
    return {
        "unique_id": row[1].replace("-", ""),
        "post_url": row[2],
        "username": row[9],
        "user_karma": row[10],
        "user_cake_day": str(row[11]),
        "post_karma": row[12],
        "comment_karma": row[13],
        "post_date": str(row[3]),
        "comments_number": row[4],
        "votes_number": row[5],
        "post_category": row[15],
    }
