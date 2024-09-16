
from django import template

register = template.Library()

@register.simple_tag
def number_range(value):
    """Returns a range of numbers up to the given value."""
    return range(1, value + 1)