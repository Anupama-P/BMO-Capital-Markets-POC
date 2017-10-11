from django import template

register = template.Library()


@register.filter
def get_key_value(some_dict, key, sub_key=None):
    if sub_key:
        return some_dict.get(key, '').get(sub_key, '')
    else:
        return some_dict.get(key, '')
