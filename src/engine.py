import os
import sys
import io
from inspect import signature, Parameter
import runpy
import ruamel.yaml
import functools

from YAMLMacros.src.yaml_provider import get_yaml_instance
from YAMLMacros.src.context import get_context
from YAMLMacros.src.context import set_context
from YAMLMacros.src.util import apply

class MacroError(Exception):
    def __init__(self, message, node):
        self.message = message
        self.node = node
        self.context = get_context()

def load_macros(macro_path):
    sys.path.append(os.getcwd())
    try:
        module = runpy.run_module(macro_path)

        return {
            name.rstrip('_'): func
            for name, func in module.items()
            if callable(func) and not name.startswith('_')
        }
    finally:
        sys.path.pop()

def apply_transformation(loader, node, transform):
    if getattr(transform, 'raw', False):
        def eval(node, deep=True):
            if node is None:
                return None
            elif deep:
                return loader.construct_object(node, deep=True)
            elif isinstance(node, ruamel.yaml.ScalarNode):
                return node
            elif isinstance(node, ruamel.yaml.SequenceNode):
                return node.value
            elif isinstance(node, ruamel.yaml.MappingNode):
                return { eval(key) : value for key, value in node.value }

        return transform(node, eval)
    else:
        if isinstance(node, ruamel.yaml.ScalarNode):
            args = loader.construct_scalar(node)
        elif isinstance(node, ruamel.yaml.SequenceNode):
            args = loader.construct_sequence(node)
        elif isinstance(node, ruamel.yaml.MappingNode):
            if any(
                param.kind == Parameter.VAR_POSITIONAL
                for name, param in signature(transform).parameters.items()
            ):
                # Before Python 3.6, **kwargs will not preserve order.
                ret = ruamel.yaml.comments.CommentedMap()
                loader.construct_mapping(node, ret)
                args = list(ret.items())
            else:
                args = loader.construct_mapping(node)

        return apply(transform, args)

def macro_multi_constructor(macros):
    def multi_constructor(loader, suffix, node):
        try:
            macro = macros[suffix]
        except KeyError:
            raise MacroError('Unknown macro "%s".' % suffix, node)

        try:
            return apply_transformation(loader, node, macros[suffix])
        except Exception as e:
            raise MacroError('Error in macro execution.', node) from e

    return multi_constructor

@functools.lru_cache(maxsize=16)
def get_parse(input):
    yaml = get_yaml_instance()
    stream = io.StringIO(input)

    yaml.get_constructor_parser(stream)
    tree = yaml.composer.get_single_node()
    macros = [
        (handle, tag.split(':')[2])
        for handle, tag in yaml.parser.tag_handles.items()
        if tag.startswith('tag:yaml-macros:')
    ]

    return (tree, macros)

def process_macros(input, arguments={}):
    with set_context(**arguments):
        tree, macros = get_parse(input)

        yaml = get_yaml_instance()

        for handle, macro_path in macros:
            macros = load_macros(macro_path)

            yaml.Constructor.add_multi_constructor(handle,
                macro_multi_constructor(macros)
            )

        return yaml.constructor.construct_document(tree)

def build_yaml_macros(input, output=None, context=None):
    syntax = process_macros(input, context)
    yaml = get_yaml_instance()

    yaml.dump(syntax, stream=output)
