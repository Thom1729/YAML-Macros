from YAMLMacros.api import get_context, set_context
from collections import OrderedDict

def argument(name, default=None):
    # return get_context().get(name, default)

    return Thunk(lambda: get_context().get(name, default))

def if_(value, ifTrue, ifFalse=None):

    return Thunk(lambda: ifTrue if value else ifFalse)

    # if value:
    #     return ifTrue
    # else:
    #     return ifFalse

def with_(bindings, value):
    def foo():
        with set_context(**bindings):
            return value

    return Thunk(foo)

    # with set_context(**bindings):
    #     return value

def foreach(collection, value):

    collection = unthunk(collection)

    if isinstance(collection, dict):
        it = collection.items()
    elif isinstance(collection, list):
        it = enumerate(collection)
    else:
        raise TypeError('Invalid collection.')

    return [
        Thunk(lambda: value)
        for k, v, in it
    ]

    # return [
    #     with_({
    #         'key': k,
    #         'value': v,
    #     }, value)
    #     for k, v in it
    # ]

def format(string, bindings=None):
    bindings = bindings or get_context()
    return string.format(**bindings)

class Thunk():
    def __init__(self, f):
        self.f = f

    def eval(self):
        return self.f()

    def apply(self, *args):
        return Thunk(lambda: unthunk(self).apply(*args))

    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            def foo(value):
                return getattr(value, name)(value, *args, **kwargs)
            return Thunk(lambda: foo(unthunk(self)))
        return _missing

def unthunk(value):
    if isinstance(value, Thunk):
        return unthunk(value.eval())
    elif isinstance(value, dict):
        return OrderedDict(
            (unthunk(k), unthunk(v))
            for k, v in value.items()
        )
    elif isinstance(value, list):
        return map(unthunk, value)
    else:
        return value
