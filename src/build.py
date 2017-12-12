import os
import sys
from inspect import signature, Parameter
import runpy
import ruamel.yaml

from YAMLMacros.api import get_yaml_instance
from YAMLMacros.api import set_context

class MacroError(Exception):
    def __init__(self, message, node):
        self.message = message
        self.node = node

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
    try:
        if isinstance(node, ruamel.yaml.ScalarNode):
            return transform(loader.construct_scalar(node))
        elif isinstance(node, ruamel.yaml.SequenceNode):
            return transform(*loader.construct_sequence(node))
        elif isinstance(node, ruamel.yaml.MappingNode):
            ret = ruamel.yaml.comments.CommentedMap()
            loader.construct_mapping(node, ret)

            if any(
                param.kind == Parameter.VAR_POSITIONAL
                for name, param in signature(transform).parameters.items()
            ):
                # Before Python 3.6, **kwargs will not preserve order.
                return transform(*ret.items())
            else:                
                return transform(**ret)
    except TypeError as e:
        raise TypeError('Failed to transform node: {}\n{}'.format(str(e), node))

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

def process_macros(input, arguments=None):
    yaml = get_yaml_instance()

    for token in ruamel.yaml.scan(input):
        if isinstance(token, ruamel.yaml.tokens.DocumentStartToken):
            break
        elif isinstance(token, ruamel.yaml.tokens.DirectiveToken) and token.name == 'TAG':
            handle, prefix = token.value
            if not prefix.startswith('tag:yaml-macros:'): break

            macro_path = prefix.split(':')[2]

            try:
                macros = load_macros(macro_path)
            except ImportError as e:
                raise MacroError('Failed to load library.', token) from e

            yaml.Constructor.add_multi_constructor(handle,
                macro_multi_constructor(macros)
            )

    from YAMLMacros.lib.arguments import unthunk
    if arguments:
        with set_context(**arguments):
            return unthunk(yaml.load(input))
    else:
        return yaml.load(input)

def build_yaml_macros(input, output=None, context=None):
    syntax = process_macros(input, context)
    yaml = get_yaml_instance()

    yaml.dump(syntax, stream=output)
