import logging
from datetime import datetime
from urllib import parse

from assignment2.validators import validate_url_parameters

_date_fields = ["user_cake_day", "post_date"]


def convert_string_to_date(post):
    for date in _date_fields:
        post[date] = datetime.strptime(post[date], "%Y-%m-%d")


def convert_date_to_string(post):
    for date in _date_fields:
        post[date] = post[date].strftime("%Y-%m-%d")


def string_to_logging_level(log_level: str) -> int:
    possible_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    return possible_levels[log_level]


def convert_post_numeric_fields(post_data: dict):
    need_convert = [
        "user_karma",
        "post_karma",
        "comment_karma",
        "comments_number",
        "votes_number",
    ]
    for field in need_convert:
        post_data[field] = convert_post_field(post_data[field])


def convert_post_field(karma: str) -> int:
    possible_suffix = {"k": 1000, "m": 1000000}
    last_symbol = karma[-1]
    if last_symbol in possible_suffix.keys():
        number = float(karma.replace(last_symbol, "").replace(",", "."))
        number = int(number * possible_suffix[last_symbol])
    elif "," in karma:
        number = int(karma.replace(",", ""))
    else:
        number = int(karma)

    return number


def parse_url_parameters(url_parameters: str):
    url_parameters = parse.urlsplit(url_parameters).query
    filters = parse.parse_qs(url_parameters)

    return {
        key: value[0] for key, value in filters.items() if validate_url_parameters(key)
    }


def convert_votes_number_pair(filters: dict):
    if filters.get("votes_number", None) is not None:
        votes_number_from, votes_number_to = list(
            map(int, filters.get("votes_number").split("-"))
        )
        filters.pop("votes_number")
        filters["votes_number_from"] = votes_number_from
        filters["votes_number_to"] = votes_number_to
