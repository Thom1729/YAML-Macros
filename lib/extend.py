from collections import OrderedDict
import ruamel.yaml
from YAMLMacros.src.sublime_resources import SublimeResources
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


def merge(*items): return Merge(OrderedDict(items))
def prepend(*items): return Prepend(list(items))


def extend(*items):
    extension = OrderedDict(items)
    base = extension['_base']
    del extension['_base']

    if path.isfile(base):
        with open(base, 'r', encoding='utf-8') as base_file:
            syntax = yaml.load(base_file)
    else:
        found_path = SublimeResources.find_resources(base)[0]
        base_file_contents = SublimeResources.load_resource(found_path)
        syntax = yaml.load(base_file_contents)
    return Merge(extension).apply(syntax)
