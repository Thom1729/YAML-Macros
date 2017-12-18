from YAMLMacros.api import apply as _apply

import copy

def argument(node, eval, arguments):
    def ret(name, default=None):
        return arguments.get(name, default)

    return _apply(ret, node.value)

argument.raw = True

def if_(node, eval, arguments):
    def ret(condition, then, else_=None):
        if eval(condition):
            return eval(then)
        else:
            return eval(else_)

    return _apply(ret, eval(node, deep=False))

if_.raw = True

def foreach(node, eval, arguments):
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
            eval(copy.deepcopy(value), {
                key_binding: k,
                value_binding: v,
            })
            for k, v in it
        ]
    return _apply(ret, eval(node, deep=False))

foreach.raw = True

def format(node, eval, arguments):
    def ret(string, bindings=arguments):
        return _apply(string.format, bindings)

    return _apply(ret, node.value)

format.raw = True
