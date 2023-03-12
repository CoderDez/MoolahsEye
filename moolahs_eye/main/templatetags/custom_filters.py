from django import template

register = template.Library()

@register.filter
def lookup(dict, key):
    try:
        return dict[key]
    except:
        print(f"Couldn't find {key} in {dict}")
        return None

@register.filter
def get_item_at_index(collection, index):
    try:
        if index > (len(collection) - 1):
            return None
        else: return collection[index]
    except Exception as e:
        print(f"Couldn't get an item at index {index} in {collection}")

@register.filter
def get_values_from_dict(dict, key):
    try:
        return dict[key]
    except Exception as e:
        print(f"Couldn't get values from dict with key {key}", e)

@register.filter
def has_items(list: list) -> bool:
    try:
        return bool(len(list))
    except:
        return False
    
@register.filter
def format_float(val) -> str:
    try:
        return "{0:,.2f}".format(val)
    except Exception as e:
        return val
