import json
from typing import Any, Dict, List, Optional, Tuple

from flask import Flask, Response, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from mongodb_handler import MongoDBHandler
from role import Role

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)
mongo = MongoDBHandler()


@app.route('/login', methods=["POST"])
def login() -> Tuple[Any, int]:
    nickname = request.data.decode("utf-8")
    # mongo.create_user(nickname, Role.LAWYER, "A")
    user = mongo.find_user_by_name(nickname)

    if user is None:
        return jsonify(nickname), 404

    access_token = create_access_token(identity=nickname)
    return jsonify(token=access_token, username=nickname), 200


@app.route('/document', methods=["POST"])
@jwt_required()
def create_document() -> Tuple[Any, int]:
    document_name = request.data.decode("utf-8")
    document_identifier = mongo.create_document(document_name, get_jwt_identity())

    if document_identifier is None:
        return jsonify([]), 403

    return jsonify(str(document_identifier)), 200


@app.route('/document/<identifier>', methods=["PUT", "GET", "DELETE"])
@jwt_required()
def update_document_content(identifier: str) -> Tuple[Any, int]:
    if request.method == "GET":
        document_content = mongo.find_document(identifier)

        if document_content is not None:
            return (
                jsonify(
                    content=document_content["content"], id=str(document_content["_id"])
                ),
                200,
            )

        return jsonify({}), 404
    elif request.method == "PUT":
        content = request.get_json()
        mongo.update_document(identifier, content)
    elif request.method == "DELETE":
        mongo.delete_document(identifier)

    return jsonify({}), 200


@app.route('/documents', methods=["GET"])
@jwt_required()
def get_documents() -> Tuple[Any, int]:
    documents = mongo.select_all_documents()

    for document in documents:
        document.pop("content")
        document["_id"] = str(document["_id"])

    return jsonify(documents), 200


@app.after_request
def after_request(response: Response) -> Response:
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')

    return response
