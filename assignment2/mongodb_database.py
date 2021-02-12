from datetime import datetime

from pymongo import ASCENDING, DESCENDING, MongoClient

from assignment2.converters import (
    convert_date_to_string,
    convert_string_to_date,
    get_selected_filters,
)


def split_post(post):
    user_fields = [
        "username",
        "user_karma",
        "user_cake_day",
        "post_karma",
        "comment_karma",
    ]
    post = post.items()
    post_data = list(filter(lambda item: item[0] not in user_fields, post))
    user_data = list(filter(lambda item: item[0] in user_fields, post))

    return dict(post_data), dict(user_data)


class MongoDBHandler:
    def __init__(self):
        self.client = MongoClient(port=27017)
        self.db = self.client.test_db

    def insert(self, post):
        convert_string_to_date(post)
        post_data, user_data = split_post(post)

        if not self.user_exist(user_data["username"]):
            _id = self.db.users.insert_one(user_data).inserted_id
        else:
            _id = self.select_user_by_name(user_data["username"])["_id"]

        post_data["owner_id"] = _id
        self.db.posts.insert_one(post_data)

    def update(self, post):
        convert_string_to_date(post)
        post_data, user_data = split_post(post)

        self.update_post(post_data)
        self.update_user(
            self.select_post(post_data["unique_id"])["owner_id"], user_data
        )

    def delete(self, unique_id):
        result = False

        if self.post_exist(unique_id):
            self.delete_post(unique_id)
            result = True

        return result

    def select_all_posts(self, filters, *, posts_count=0):
        if not filters and posts_count == 0:
            all_posts = self.db.posts.find({})
        else:
            condition_filters, ordering_filters = get_filter_groups(filters)
            all_posts = self.db.posts.find(condition_filters)

            if ordering_filters.get("sorting_field", False):
                all_posts.sort(
                    filters["sorting_field"],
                    ASCENDING if filters["order"] == "ASC" else DESCENDING,
                )

            all_posts.skip(int(filters.get("page", 0)) * posts_count).limit(posts_count)

        joined_posts = []
        for post in all_posts:
            self._join_user_and_post_info(post)
            convert_date_to_string(post)
            joined_posts.append(post)

        return joined_posts

    def select_single_post(self, unique_id):
        post = self.select_post(unique_id)

        if post:
            self._join_user_and_post_info(post)
            convert_date_to_string(post)

        return post

    def _join_user_and_post_info(self, post_data):
        user_data = self.select_user_by_id(post_data["owner_id"])
        post_data.update(user_data)
        post_data.pop("owner_id")
        post_data.pop("_id")

    def update_post(self, post_data):
        self.db.posts.update_one(
            {"unique_id": post_data["unique_id"]}, {"$set": post_data}
        )

    def update_user(self, user_id, user_data):
        self.db.users.update_one({"_id": user_id}, {"$set": user_data})

    def delete_user(self, user_id):
        self.db.users.delete_one({"_id": user_id})

    def delete_post(self, unique_id):
        self.db.posts.delete_one({"unique_id": unique_id})

    def select_user_by_id(self, user_id):
        return self.db.users.find_one({"_id": user_id})

    def select_user_by_name(self, username):
        return self.db.users.find_one({"username": username})

    def select_post(self, unique_id):
        return self.db.posts.find_one({"unique_id": unique_id})

    def entry_count(self):
        return self.db.posts.estimated_document_count()

    def user_exist(self, username):
        return self.db.users.count_documents({"username": username}, limit=1) != 0

    def post_exist(self, unique_id):
        return self.db.posts.count_documents({"unique_id": unique_id}, limit=1) != 0

    def posts_categories(self):
        return self.db.posts.distinct("post_category")


def get_filter_groups(filters: dict):
    condition_filters = get_selected_filters(
        filters, ["post_category", "votes_number", "post_date"]
    )
    ordering_filters = get_selected_filters(filters, ["sorting_field", "order"])

    if date := condition_filters.get("post_date", False):
        condition_filters["post_date"] = datetime.strptime(date, "%Y-%m-%d")

    if borders := condition_filters.get("votes_number", False):
        borders = borders.split("-")
        condition_filters["votes_number"] = {
            "$gte": int(borders[0]),
            "$lte": int(borders[1]),
        }

    return condition_filters, ordering_filters
