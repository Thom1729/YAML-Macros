import ruamel.yaml
from os import path

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


def merge(**x): return Merge(x)
def prepend(*x): return Prepend(list(x))


def extend(base, **extension):
    syntax = yaml.load( open( path.abspath(base),'r') )
    return Merge(extension).apply(syntax)