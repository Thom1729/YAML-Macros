from YAMLMacros.api import apply as _apply
from YAMLMacros.api import raw_macro

import copy

@raw_macro
def argument(name, default=None, *, eval, arguments):
    if name.value in arguments:
        return arguments[name.value]
    elif default:
        return eval(default)
    else:
        return None

@raw_macro
def if_(condition, then, else_=None, *, eval):
    if eval(condition):
        return eval(then)
    elif else_:
        return eval(else_)
    else:
        return None

@raw_macro
def foreach(in_, value, *, as_=None, eval):
    collection = eval(in_)

    if isinstance(collection, dict):
        items = collection.items()
    elif isinstance(collection, list):
        items = enumerate(collection)
    else:
        raise TypeError('Invalid collection.')

    if as_:
        as_ = eval(as_)

        if isinstance(as_, dict):
            key_binding = as_.get('key', None)
            value_binding = as_.get('value', None)
        elif isinstance(as_, list):
            if len(as_) == 1:
                key_binding = None
                value_binding = as_[0]
            elif len(as_) == 2:
                key_binding = as_[0]
                value_binding = as_[1]
        else:
            key_binding = None
            value_binding = as_
    else:
        key_binding = 'key'
        value_binding = 'value'

    return [
        eval(copy.deepcopy(value), {
            key_binding: k,
            value_binding: v,
        })
        for k, v in items
    ]

@raw_macro
def format(string, bindings=None, *, eval, arguments):
    if bindings:
        bindings = eval(bindings)
    else:
        bindings = arguments

    return _apply(string.value.format, bindings)
