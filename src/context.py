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
        _get_context_stack().append(self.context)
        return self.context

    def __exit__(self, *args):
        _get_context_stack().pop()
