import json
from django import template

register = template.Library()


@register.filter
def lookup(d, key):
    return d.get(key)


@register.filter
def jsonify(d):
    return json.dumps(d)
