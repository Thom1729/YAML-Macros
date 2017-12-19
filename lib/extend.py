from collections import OrderedDict
from functools import reduce

from YAMLMacros.api import get_yaml_instance
from YAMLMacros.src.util import deprecated, flatten

from ruamel.yaml.comments import CommentedOrderedMap

class Operation():
    def __init__(self, extension):
        self.extension = extension

class Merge(Operation):
    def apply(self, base):
        ret = base

        for key, value in self.extension.items():
            # print(type(value))
            if isinstance(value, Operation):
                ret[key] = value.apply(base.get(key, None))
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
            flatten(*self.extension),
            base,
        )

def merge(node, eval, arguments):
    loader = eval.loader

    ret = CommentedOrderedMap()
    loader.construct_mapping(node, ret)

    return Merge(ret)

merge.raw = True

def prepend(*items): return Prepend(list(items))
def all(*items): return All(list(items))


def apply(base, *extensions):
    return all(*extensions).apply(base)

@deprecated('Use !apply instead.')
def extend(*items):
    extension = OrderedDict(items)
    base = extension['_base']
    del extension['_base']

    yaml = get_yaml_instance()

    with open(base, 'r') as base_file:
        syntax = yaml.load(base_file)
    return Merge(extension).apply(syntax)
