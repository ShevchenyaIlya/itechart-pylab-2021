import logging
from datetime import datetime

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
    filters = list(
        map(lambda filter_pair: filter_pair.split("="), url_parameters.split("&"))
    )

    return {
        filter_pair[0]: filter_pair[1]
        for filter_pair in filters
        if len(filter_pair) == 2 and validate_url_parameters(filter_pair[0])
    }


def validate_url_parameters(filter_name: str):
    possible_filters = ["page", "filter_field", "order"]

    return filter_name in possible_filters
