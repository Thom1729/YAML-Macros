from YAMLMacros.api import Context

def argument(name, default=None):
    return Context.get(name, default)

def if_(value, ifTrue, ifFalse=None):
    if value:
        return ifTrue
    else:
        return ifFalse
