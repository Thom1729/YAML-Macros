import threading
from contextlib import contextmanager

_ns = threading.local()

def _get_context_stack():
    if 'context' not in _ns.__dict__:
        _ns.context = [ ContextFrame() ]
    return _ns.context

class ContextFrame(dict):
    def merge(self, other):
        child = self.copy()
        child.update(other)
        return ContextFrame(child)

def get_context():
    return _get_context_stack()[-1]

@contextmanager
def set_context(**kwargs):
    stack = _get_context_stack()
    stack.append(stack[-1].merge(kwargs))
    yield
    stack.pop()
