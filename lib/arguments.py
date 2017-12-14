from YAMLMacros.api import get_context
from YAMLMacros.api import set_context
from YAMLMacros.api import apply as _apply

import copy

def argument(name, default=None):
    return get_context().get(name, default)

def if_(node, eval):
    def ret(condition, then, else_=None):
        if eval(condition):
            return eval(then)
        else:
            return eval(else_)

    return _apply(ret, eval(node, deep=False))

if_.raw = True

def _with(bindings, node, eval):
    with set_context(**bindings):
        return eval(node)

def foreach(node, eval):
    def ret(collection, value, *, as_=None):

        def get_binding_map(as_):
            if as_ is None:
                return ( 'key', 'value' )
            elif isinstance(as_, dict):
                return ( as_.get('key', None), as_.get('value', None) )
            elif isinstance(as_, list):
                if len(as_) == 1:
                    return ( None, as_[0] )
                elif len(as_) == 2:
                    return ( as_[0], as_[1] )
            else:
                return (None, as_)

        collection = eval(collection)
        as_ = eval(as_)

        if isinstance(collection, dict):
            it = collection.items()
        elif isinstance(collection, list):
            it = enumerate(collection)
        else:
            raise TypeError('Invalid collection.')

        key_binding, value_binding = get_binding_map(as_)

        return [
            _with({
                key_binding: k,
                value_binding: v,
            }, copy.deepcopy(value), eval)
            for k, v in it
        ]
    return _apply(ret, eval(node, deep=False))

foreach.raw = True

def format(string, bindings=None):
    bindings = bindings or get_context()
    return string.format(**bindings)
