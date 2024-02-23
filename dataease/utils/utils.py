import re


def to_snake_name(origin_name):
    snake_str = re.sub(r'([A-Z])', r'_\1', origin_name)
    return snake_str.lower().lstrip('_')


def to_capitalize_name(origin_name):
    return origin_name[0].upper() + origin_name[1:]