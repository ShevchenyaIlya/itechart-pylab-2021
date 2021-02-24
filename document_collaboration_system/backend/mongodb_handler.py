from datetime import datetime
from typing import Dict, List, Optional

from bson.objectid import ObjectId
from document_status import Status
from pymongo import MongoClient
from validators import role_validation


class MongoDBHandler:
    def __init__(self) -> None:
        self.client = MongoClient(port=27017)
        self.db = self.client.myDatabase

    def create_user(
        self, username: str, user_role: str, company: str
    ) -> Optional[ObjectId]:
        if role_validation(user_role) and not self.user_exist(username, company):
            return self.db.users.insert_one(
                {
                    "username": username,
                    "role": user_role,
                    "company": company,
                }
            ).inserted_id

        return None

    def find_user_by_name(self, nickname: str) -> Optional[Dict]:
        return self.db.users.find_one({"username": nickname})

    def find_user_by_id(self, user_identifier: ObjectId) -> Optional[Dict]:
        return self.db.users.find_one({"_id": user_identifier})

    def user_exist(self, username: str, company: str) -> bool:
        return (
            self.db.users.count_documents(
                {"username": username, "company": company}, limit=1
            )
            != 0
        )

    def update_user_role(self, user_id: str, new_role: str) -> None:
        if role_validation(new_role) and ObjectId.is_valid(user_id):
            self.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": {"role": new_role}}, upsert=False
            )

    def create_document(self, document_name: str, creator: str) -> Optional[Dict]:
        user = self.find_user_by_name(creator)

        if not self.document_exist(document_name) and user is not None:
            return self.db.documents.insert_one(
                {
                    "document_name": document_name,
                    "creation_date": datetime.now(),
                    "status": Status.CREATED,
                    "creator": user["username"],
                    "company": user["company"],
                    "content": {},
                }
            ).inserted_id

        return None

    def update_document(self, document_id: str, content: Dict) -> None:
        self.db.documents.update_one(
            {"_id": ObjectId(document_id)}, {"$set": {"content": content}}, upsert=False
        )

    def delete_document(self, document_id: str) -> None:
        if ObjectId.is_valid(document_id):
            self.db.posts.delete_one({"_id": ObjectId(document_id)})

    def document_exist(self, document_name: str) -> bool:
        return (
            self.db.documents.count_documents({"document_name": document_name}, limit=1)
            != 0
        )

    def find_document(self, document_id: str) -> Optional[Dict]:
        if ObjectId.is_valid(document_id):
            return self.db.documents.find_one({"_id": ObjectId(document_id)})

        return None

    def select_all_documents(self) -> List:
        return list(self.db.documents.find({}))
