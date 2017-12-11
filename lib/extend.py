from collections import OrderedDict
from functools import reduce

from YAMLMacros.api import process_macros

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

class All(Operation):
    def apply(self, base):
        return reduce(
            lambda ret, ext: ext.apply(ret),
            [x for x in self.extension if x != None],
            base
        )

def merge(*items): return Merge(OrderedDict(items))
def prepend(*items): return Prepend(list(items))
def all(*items): return All(list(items))


def include(name):
    with open(name, 'r') as file:
        return process_macros(file.read())

def apply(base, *extensions):
    return all(*extensions).apply(base)

def extend(*items):
    extension = OrderedDict(items)
    base = extension['_base']
    del extension['_base']

    with open(base, 'r') as base_file:
        syntax = yaml.load(base_file)
    return Merge(extension).apply(syntax)
