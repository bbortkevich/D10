from django import template

register = template.Library()

bad_words = ["дурак", "редиска", "олух"]


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError("incorrect value")

    for item in bad_words:
        part = item[1:]
        value = value.replace(item[1:], "*" * len(part))

    return value
