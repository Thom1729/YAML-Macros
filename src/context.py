import threading
from contextlib import contextmanager
from YAMLMacros.src.util import merge

_ns = threading.local()

def _get_context_stack():
    if 'context' not in _ns.__dict__:
        _ns.context = [ {} ]
    return _ns.context

def get_context():
    return _get_context_stack()[-1]

@contextmanager
def set_context(**kwargs):
    stack = _get_context_stack()
    stack.append(merge(stack[-1], kwargs))
    yield
    stack.pop()
