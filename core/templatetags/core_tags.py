from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Returns the value for the given key in a dictionary.
    Used to access dictionary values with a variable key in templates.
    """
    return dictionary.get(key) 