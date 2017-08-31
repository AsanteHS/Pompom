from django import template

register = template.Library()  # pylint: disable=C0103


@register.filter
def percentage(value):
    if value is None:
        return ""
    return format(value, ".0%")


@register.filter
def get_range(value):
    return range(value)
