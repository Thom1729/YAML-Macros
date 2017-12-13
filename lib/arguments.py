from YAMLMacros.api import get_context, set_context
from collections import OrderedDict

def argument(name, default=None):
    return get_context().get(name, default)

def if_(condition, then, ifFalse=None, *, __eval):
    if __eval(condition):
        return __eval(then)
    else:
        return __eval(ifFalse)

if_.raw = True

def with_(bindings, value, *, __eval):
    print(bindings)
    with set_context(**bindings):
        return __eval(value)

def foreach(collection, value, *, __eval):
    collection = __eval(collection)
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
        }, value, __eval=__eval)
        for k, v in it
    ]

foreach.raw = True

def format(string, bindings=None):
    bindings = bindings or get_context()
    return string.format(**bindings)
