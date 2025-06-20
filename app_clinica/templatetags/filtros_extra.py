from django import template

register = template.Library()

@register.filter
def until(value, max_val):
    return range(value, int(max_val))