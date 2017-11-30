import threading

_ns = threading.local()

def _get_context_stack():
    if 'context' not in _ns.__dict__:
        _ns.context = [ {} ]
    return _ns.context

def get_context():
    return _get_context_stack()[-1]

class Context():
    def __init__(self, context):
        self.context = context
        self.stack = _get_context_stack()

    def __enter__(self):
        self.stack.append(self.context)
        return self.context

    def __exit__(self, *args):
        self.stack.pop()
