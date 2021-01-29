import json

import psycopg2


def load_database_connection_settings():
    with open("db_connection_setting.json") as json_file:
        return json.load(json_file)


def database_connection(connection_settings):
    return psycopg2.connect(**connection_settings)


def load_query(filename):
    with open(filename, "r") as sql_query:
        return sql_query.read()


def load_sql_queries():
    query_files = [
        "sql/create_posts_table.sql",
        "sql/create_users_table.sql",
        "sql/insert_post.sql",
        "sql/insert_user.sql",
        "sql/delete_post.sql",
        "sql/delete_user.sql",
        "sql/update_user.sql",
        "sql/update_post.sql",
        "sql/select_all_posts.sql",
        "sql/select_one_post.sql",
        "sql/row_count.sql",
        "sql/user_exists.sql",
        "sql/post_exists.sql",
    ]
    queries = {}
    for file in query_files:
        queries[file.strip("sql").strip("./")] = load_query(file)

    return queries


class PostgreSQLHandler:
    def __init__(self):
        self.connection = database_connection(load_database_connection_settings())
        self.cursor = self.connection.cursor()
        self.queries = load_sql_queries()
        self.create_tables()

    def __del__(self):
        self.close_connection()

    def create_tables(self):
        self.create_users_table()
        self.create_posts_table()

    def update(self, post):
        self.update_post(post)
        self.update_user(post)

    def delete(self, unique_id):
        if self.is_exist(unique_id):
            self.delete_post(unique_id)
            self.delete_user(unique_id)
            return True

        return False

    def create_posts_table(self):
        self.cursor.execute(self.queries["create_posts_table"])
        self.connection.commit()

    def create_users_table(self):
        self.cursor.execute(self.queries["create_users_table"])
        self.connection.commit()

    def insert_parsed_post(self, post):
        if not self.user_exists(post["username"]):
            self.cursor.execute(
                self.queries["insert_user"],
                (
                    post["username"],
                    post["user_karma"],
                    post["user_cake_day"],
                    post["post_karma"],
                    post["comment_karma"],
                ),
            )

        self.cursor.execute(
            self.queries["insert_post"],
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
        self.cursor.execute(self.queries["delete_post"], (unique_id,))
        self.connection.commit()

    def delete_user(self, unique_id):
        self.cursor.execute(
            self.queries["delete_user"],
            (unique_id,),
        )
        self.connection.commit()

    def update_post(self, post):
        self.cursor.execute(
            self.queries["update_post"],
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
            self.queries["update_user"],
            (
                post["user_karma"],
                post["user_cake_day"],
                post["post_karma"],
                post["comment_karma"],
                post["username"],
            ),
        )
        self.connection.commit()

    def get_all_posts(self):
        self.cursor.execute(self.queries["select_all_posts"])
        rows = self.cursor.fetchall()
        return [convert_selected_data(row) for row in rows]

    def get_single_post(self, unique_id):
        self.cursor.execute(
            self.queries["select_one_post"],
            (unique_id,),
        )
        row = self.cursor.fetchall()
        if row:
            return convert_selected_data(row[0])

    def row_count(self):
        self.cursor.execute(self.queries["row_count"])
        return self.cursor.fetchall()[0][0]

    def is_exist(self, unique_id):
        self.cursor.execute(self.queries["post_exists"], (unique_id,))
        return self.cursor.fetchall()[0][0]

    def user_exists(self, username):
        self.cursor.execute(self.queries["user_exists"], (username,))
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
        "post_category": row[6],
    }


if __name__ == "__main__":
    handler = PostgreSQLHandler()
    load_sql_queries()
