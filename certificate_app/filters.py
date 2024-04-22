# Create a Python file in your Django app, for example, filters.py
from django import template

register = template.Library()


@register.filter(name='get_value')
def get_value(dictionary, key):
    return dictionary.get(key, '')
