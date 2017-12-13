import keyword

def apply(fn, args):
    if isinstance(args, dict):
        return fn(**{
            (k+'_' if keyword.iskeyword(k) else k) : v for k, v in args.items()
        })
    elif isinstance(args, list):
        return fn(*args)
    else:
        return fn(args)
