def validate_url_parameters(filter_name: str):
    possible_filters = ["page", "filter_field", "order"]
    return filter_name in possible_filters


def page_number_validation(value: str):
    return value.isdigit()


def filter_fields_validation(value: str):
    possible_filters = ["post_date", "post_category", "votes_number"]

    return value in possible_filters


def order_validation(value: str):
    possible_orders = ["ASC", "DESC"]

    return value in possible_orders


def validate_url_parameters_values(parameter_pairs: dict):
    validator = {
        "page": page_number_validation,
        "filter_field": filter_fields_validation,
        "order": order_validation,
    }

    for key in list(parameter_pairs):
        if not validator[key](parameter_pairs[key]):
            parameter_pairs.pop(key)
