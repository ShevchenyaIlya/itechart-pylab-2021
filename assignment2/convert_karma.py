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


if __name__ == "__main__":
    print(convert_post_field("1,233m"))
