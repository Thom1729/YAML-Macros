import threading

_ns = threading.local()

def _get_context_stack():
    if 'context' not in _ns.__dict__:
        _ns.context = [ {} ]
    return _ns.context

class Context():
    @staticmethod
    def get(key, default=None):
        return _get_context_stack()[-1].get(key, default)

    def __init__(self, context):
        self.context = context

    def __enter__(self):
        stack = _get_context_stack()
        new = stack[-1].copy()
        new.update(self.context)
        stack.append(new)

    def __exit__(self, *args):
        _get_context_stack().pop()
