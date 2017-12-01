from YAMLMacros.src.context import get_context as _get_context

def argument(name):
    return _get_context().get(name, None)

def if_(value, ifTrue, ifFalse=None):
    if value:
        return ifTrue
    else:
        return ifFalse
