from YAMLMacros.api import get_context, set_context
from collections import OrderedDict

def argument(name, default=None):
    return get_context().get(name, default)

def if_(value, ifTrue, ifFalse=None):
    if value:
        return ifTrue
    else:
        return ifFalse

def with_(bindings, value):
    with set_context(**bindings):
        return value

def foreach(collection, value):
    if isinstance(collection, dict):
        it = collection.items()
    elif isinstance(collection, list):
        it = enumerate(collection)
    else:
        raise TypeError('Invalid collection.')

    return [
        with_({
            'key': k,
            'value': v,
        }, value)
        for k, v in it
    ]

def format(string, bindings=None):
    bindings = bindings or get_context()
    return string.format(**bindings)
