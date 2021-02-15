from datetime import datetime


def validate_url_parameters(filter_name: str):
    possible_filters = {
        "page",
        "post_category",
        "post_date",
        "votes_number",
        "sorting_field",
        "order",
    }

    return filter_name in possible_filters


def sorting_field_validation(value: str):
    return value in {"post_category", "votes_number", "post_date"}


def page_number_validation(value: str):
    return value.isdigit()


def category_validation(value: str, categories: list):
    if any(isinstance(category, tuple) for category in categories):
        contained = (value,) in categories
    else:
        contained = value in categories

    return contained


def post_date_validation(value: str):
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False

    return True


def votes_number_validation(value: str):
    borders = value.split("-")

    if all([number.isdigit() for number in borders]):
        return borders[0] < borders[1]

    return False


def order_validation(value: str):
    possible_orders = ["ASC", "DESC"]

    return value in possible_orders


def validate_url_parameters_values(parameter_pairs: dict, categories):
    validator = {
        "page": page_number_validation,
        "post_category": category_validation,
        "post_date": post_date_validation,
        "votes_number": votes_number_validation,
        "sorting_field": sorting_field_validation,
        "order": order_validation,
    }

    for key, value in parameter_pairs.items():
        is_valid = (
            validator[key](value, categories)
            if key == "post_category"
            else validator[key](value)
        )

        if not is_valid:
            parameter_pairs.pop(key)
