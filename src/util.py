import keyword
from functools import wraps

def apply(fn, args):
    if isinstance(args, dict):
        return fn(**{
            (k+'_' if keyword.iskeyword(k) else k) : v for k, v in args.items()
        })
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
