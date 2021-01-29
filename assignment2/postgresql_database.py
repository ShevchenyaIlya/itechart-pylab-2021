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


class PostgreSQLHandler:
    def __init__(self):
        self.connection = database_connection(load_database_connection_settings())
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.close_connection()

    def update(self, post):
        self.update_post(post)
        self.update_user(post)

    def delete(self, unique_id):
        if self.is_exist(unique_id):
            self.delete_post(unique_id)
            self.delete_user(unique_id)
            return True

        return False

    def insert_parsed_post(self, post):
        if not self.user_exists(post["username"]):
            self.cursor.execute(
                load_query("sql/insert_user.sql"),
                (
                    post["username"],
                    post["user_karma"],
                    post["user_cake_day"],
                    post["post_karma"],
                    post["comment_karma"],
                ),
            )

        self.cursor.execute(
            load_query("sql/insert_post.sql"),
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
        self.cursor.execute(load_query("sql/delete_post.sql"), (unique_id,))
        self.connection.commit()

    def delete_user(self, unique_id):
        self.cursor.execute(
            load_query("sql/delete_user.sql"),
            (unique_id,),
        )
        self.connection.commit()

    def update_post(self, post):
        self.cursor.execute(
            load_query("sql/update_post.sql"),
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
            load_query("sql/update_user.sql"),
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
        self.cursor.execute(load_query("sql/select_all_posts.sql"))
        rows = self.cursor.fetchall()

        return [convert_selected_data(row) for row in rows]

    def get_single_post(self, unique_id):
        self.cursor.execute(
            load_query("sql/select_one_post.sql"),
            (unique_id,),
        )

        row = self.cursor.fetchall()
        if row:
            return convert_selected_data(row[0])

    def row_count(self):
        self.cursor.execute(load_query("sql/row_count.sql"))
        return self.cursor.fetchall()[0][0]

    def is_exist(self, unique_id):
        self.cursor.execute(load_query("sql/post_exists.sql"), (unique_id,))
        return self.cursor.fetchall()[0][0]

    def user_exists(self, username):
        self.cursor.execute(load_query("sql/user_exists.sql"), (username,))
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
