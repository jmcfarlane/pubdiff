"""Mako filters"""

def diff_after(value):
    value = value.strip()

    if value == '>':
        return 'content-added'
    elif value == '<':
        return 'content-removed'
    elif value == '|':
        return 'content-changed'
    else:
        return 'unchanged'

def diff_before(value):
    value = value.strip()

    if value == '<':
        return 'content-removed'
    elif value == '>':
        return ''
    elif value == '|':
        return 'content-changed'
    else:
        return 'unchanged'

def none2empty(value):
    if value == 'None' or value is None:
        return ''
    else:
        return value
