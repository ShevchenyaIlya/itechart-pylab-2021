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
    query_files = ["sql/create_posts_table.sql", "sql/create_users_table.sql"]
    queries = {}
    for file in query_files:
        queries[file.strip("/.sql")] = load_query(file)

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
        if self.get_single_post(unique_id):
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
                "INSERT INTO users(username, user_karma, user_cake_day, post_karma, comment_karma) "
                "VALUES (%s, %s, %s, %s, %s);",
                (
                    post["username"],
                    post["user_karma"],
                    post["user_cake_day"],
                    post["post_karma"],
                    post["comment_karma"],
                ),
            )

        self.cursor.execute(
            "INSERT INTO posts(unique_id, post_url, post_date, comments_number,"
            "votes_number, post_category, owner) VALUES"
            "(%s, %s, %s, %s, %s, %s, (SELECT user_id from users WHERE username=%s))",
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
        self.cursor.execute("DELETE FROM posts WHERE unique_id=%s;", (unique_id,))
        self.connection.commit()

    def delete_user(self, unique_id):
        self.cursor.execute(
            "DELETE FROM users WHERE user_id=(SELECT owner FROM posts WHERE unique_id=%s);",
            (unique_id,),
        )
        self.connection.commit()

    def update_post(self, post):
        self.cursor.execute(
            "UPDATE posts "
            "SET post_date = %s,"
            "post_url = %s,"
            "comments_number = %s,"
            "votes_number = %s,"
            "post_category = %s,"
            "owner = (SELECT user_id from users WHERE username=%s)"
            "WHERE unique_id=%s;",
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
            "UPDATE users "
            "SET user_karma = %s,"
            "user_cake_day = %s,"
            "post_karma = %s,"
            "comment_karma = %s "
            "WHERE username=%s;",
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
        self.cursor.execute(
            "SELECT * FROM posts INNER JOIN users ON (posts.owner=users.user_id);"
        )
        rows = self.cursor.fetchall()
        return [convert_selected_data(row) for row in rows]

    def get_single_post(self, unique_id):
        self.cursor.execute(
            "SELECT * FROM posts INNER JOIN users ON (posts.owner=users.user_id) WHERE unique_id=%s;",
            (unique_id,),
        )
        row = self.cursor.fetchall()
        if row:
            return convert_selected_data(row[0])

    def row_count(self):
        self.cursor.execute("SELECT count(*) FROM posts")
        return self.cursor.fetchall()[0][0]

    def user_exists(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        return self.cursor.fetchall()

    def close_connection(self):
        self.connection.close()


def convert_selected_data(row):
    return {
        "unique_id": row[1],
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
