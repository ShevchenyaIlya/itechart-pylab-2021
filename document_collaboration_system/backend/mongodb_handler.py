from typing import Dict, List, Optional

from bson.objectid import ObjectId
from pymongo import MongoClient


class MongoDBHandler:
    def __init__(self) -> None:
        self.client = MongoClient(port=27017)
        self.db = self.client.myDatabase

    def create_user(self, username: str, user_role: str, company: str) -> ObjectId:
        return self.db.users.insert_one(
            {
                "username": username,
                "role": user_role,
                "company": company,
            }
        ).inserted_id

    def find_user_by_name(self, nickname: str) -> Optional[Dict]:
        return self.db.users.find_one({"username": nickname})

    def create_document(self, document_name: str) -> Optional[Dict]:
        return (
            self.db.documents.insert_one(
                {
                    "document_name": document_name,
                    "content": {},
                }
            ).inserted_id
            if not self.document_exist(document_name)
            else None
        )

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
