import keyword
from functools import wraps
import ruamel.yaml
from inspect import signature, Parameter

def fix_keywords(d):
    return {
        (k+'_' if keyword.iskeyword(k) else k) : v
        for k, v in d.items()
    }

def apply(fn, args):
    if isinstance(args, dict):
        return fn(**fix_keywords(args))
    elif isinstance(args, list):
        return fn(*args)
    else:
        return fn(args)

def deprecated(*args):
    def _deprecated(f, message=None):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print('Warning: {name} is deprecated.{message}'.format(
                name=f.__name__,
                message=(' ' + message) if message else '',
            ))
            return f(*args, **kwargs)

        return wrapper

    if len(args) == 1 and callable(args[0]):
        return _deprecated(args[0])
    else:
        return lambda f: _deprecated(f, *args)

def flatten(*args):
    for arg in args:
        if isinstance(arg, list):
            yield from flatten(*arg)
        elif arg is not None:
            yield arg

def merge(*dicts):
    ret = {}
    for d in dicts:
        ret.update(d)
    return ret

def raw_macro(fn):
    def ret(node, eval, arguments):
        extras = { 'eval': eval, 'arguments': arguments }
        extras = {
            k:v for k, v in extras.items() if k in arg_names
        }

        if isinstance(node, ruamel.yaml.ScalarNode):
            return fn(node, **extras)
        elif isinstance(node, ruamel.yaml.SequenceNode):
            return fn(*node.value, **extras)
        elif isinstance(node, ruamel.yaml.MappingNode):
            kwargs = fix_keywords({ eval(k): v for k, v in node.value })
            collisions = (set(kwargs) & set(extras))
            if collisions:
                raise TypeError('Keyword parameters %s would be shadowed by raw macro parameters.' % str(collisions))

            return fn(**merge(kwargs, extras))

    if any(
        param.kind == Parameter.VAR_KEYWORD
        for name, param in signature(fn).parameters.items()
    ):
        raise TypeError('Raw macros using this decorator may not use **kwargs.')

    arg_names = { name for name, param in signature(fn).parameters.items() }

    ret.raw = True
    ret.wrapped = fn

    return ret
