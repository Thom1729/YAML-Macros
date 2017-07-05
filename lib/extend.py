from collections import OrderedDict
import ruamel.yaml
yaml = ruamel.yaml.YAML()

class Operation():
    def __init__(self, extension):
        self.extension = extension

class Merge(Operation):
    def apply(self, base):
        ret = base.copy()

        for key, value in self.extension.items():
            if key in base and isinstance(value, Operation):
                ret[key] = value.apply(base[key])
            else:
                ret[key] = value

        return ret

class Prepend(Operation):
    def apply(self, base):
        return self.extension + base


def merge(*items): return Merge(OrderedDict(items))
def prepend(*items): return Prepend(list(items))


def extend(*items):
    extension = OrderedDict(items)
    base = extension['_base']
    del extension['_base']

    syntax = yaml.load( open(base, 'r') )
    return Merge(extension).apply(syntax)