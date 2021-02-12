import argparse
import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Tuple

from assignment2.converters import (
    convert_post_numeric_fields,
    parse_url_parameters,
    string_to_logging_level,
)
from assignment2.mongodb_database import MongoDBHandler
from assignment2.postgresql_database import PostgreSQLHandler
from assignment2.url_processing import find_matches, get_unique_id_from_url
from assignment2.validators import validate_url_parameters_values


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.database_handler = define_using_database()
        self.possible_endpoints = {
            ("GET", r"/posts/?"): self.get_all_posts_request,
            ("GET", r"/posts/\?.*"): self.get_all_posts_request,
            ("GET", r"/posts/.{32}/?"): self.get_single_post_request,
            ("POST", r"/posts/?"): self.post_request,
            ("DELETE", r"/posts/.{32}/?"): self.delete_request,
            ("PUT", r"/posts/.{32}/?"): self.put_request,
        }
        super().__init__(*args, **kwargs)

    def request_handler(self, command: str, uri: str):
        possible_endpoint = list(
            filter(lambda key: key[0] == command, self.possible_endpoints)
        )
        return self.possible_endpoints.get(find_matches(possible_endpoint, uri))

    def _get_request_body(self) -> dict:
        content_length = int(self.headers["Content-Length"])
        return json.loads(self.rfile.read(content_length).decode("utf-8"))

    def _set_response(self, status_code: int, name: str, body=None) -> None:
        self.send_response(status_code, name)
        self._set_content_type()
        if body:
            self.wfile.write(json.dumps(body).encode("utf-8"))

    def _set_content_type(self) -> None:
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self) -> None:
        logging.info(f"GET request, Path: {self.path}")
        get_method = self.request_handler(self.command, self.path)

        if get_method:
            self._set_response(*get_method())
        else:
            self._set_response(404, "Not Found")

    def do_POST(self) -> None:
        post_data = self._get_request_body()
        logging.info(f"POST request, Path: {str(self.path)}, Body: {post_data}")
        post_method = self.request_handler(self.command, self.path)

        if post_method:
            self._set_response(*post_method(post_data))
        else:
            self._set_response(200, "OK")

    def do_DELETE(self) -> None:
        logging.info(f"DELETE request, Path: {self.path}")
        delete_method = self.request_handler(self.command, self.path)

        if delete_method:
            self._set_response(*delete_method())
        else:
            self._set_response(404, "Not Found")

    def do_PUT(self) -> None:
        post_data = self._get_request_body()
        logging.info(f"PUT request, Path: {str(self.path)}, Body: {post_data}")
        put_method = self.request_handler(self.command, self.path)

        if put_method:
            self._set_response(*put_method(post_data))
        else:
            self._set_response(404, "Not Found")

    def get_all_posts_request(self) -> Tuple[int, str, list]:
        if not (filters := parse_url_parameters(self.path)):
            db_content = self.database_handler.select_all_posts(None)
        else:
            validate_url_parameters_values(
                filters, self.database_handler.posts_categories()
            )
            db_content = self.database_handler.select_all_posts(filters, posts_count=5)

        return (200, "OK", db_content) if db_content else (204, "No Content", [])

    def get_single_post_request(self):
        unique_id = get_unique_id_from_url(self.path)
        post = self.database_handler.select_single_post(unique_id)

        if post is not None:
            return 200, "OK", post
        else:
            return 404, "Not Found"

    def post_request(self, post_data: dict):
        unique_id = post_data["unique_id"]
        if self.database_handler.post_exist(unique_id):
            return 200, "OK"
        else:
            convert_post_numeric_fields(post_data)
            self.database_handler.insert(post_data)
            line_number = self.database_handler.entry_count()
            return 201, "Created", {unique_id: line_number}

    def delete_request(self) -> Tuple[int, str]:
        unique_id = get_unique_id_from_url(self.path)
        if self.database_handler.delete(unique_id):
            return 200, "OK"
        else:
            return 205, "No Content"

    def put_request(self, post_data: dict) -> Tuple[int, str]:
        unique_id = get_unique_id_from_url(self.path)
        if not self.database_handler.post_exist(unique_id):
            return 205, "No Content"
        else:
            convert_post_numeric_fields(post_data)
            self.database_handler.update(post_data)
            return 200, "OK"


def define_using_database():
    valid_databases = {"MongoDB": MongoDBHandler, "PostgreSQL": PostgreSQLHandler}
    try:
        with open("selected_database.json", "r") as file:
            choice = json.loads(file.read())
            database = valid_databases[choice["database"]]()
    except (FileNotFoundError, KeyError):
        database = PostgreSQLHandler()

    logging.debug(f"Using {database}")
    return database


def parse_command_line_arguments() -> tuple:
    argument_parser = argparse.ArgumentParser(description="Simple http server")
    argument_parser.add_argument("--port", metavar="port", type=int, default=8087)
    argument_parser.add_argument(
        "--log_level",
        metavar="log_level",
        type=str,
        default="CRITICAL",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Minimal logging level('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')",
    )
    args = argument_parser.parse_args()

    return args.port, args.log_level


def run_server(
    port, server_class=ThreadingHTTPServer, handler_class=CustomHTTPRequestHandler
):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    try:
        logging.info(f"Start server on port {port}")
        httpd.serve_forever()
    except KeyboardInterrupt as exception:
        logging.error(exception)
    finally:
        httpd.server_close()
        logging.info(f"Server closed on port {port}")


if __name__ == "__main__":
    port_number, logging_level = parse_command_line_arguments()
    logging.basicConfig(level=string_to_logging_level(logging_level))
    run_server(port_number)
