import os
import sys
from inspect import signature, Parameter
import runpy

import ruamel.yaml
from YAMLMacros.api import get_yaml_instance, Context

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

def process_macros(input, context=None):
    yaml = get_yaml_instance()

    for token in ruamel.yaml.scan(input):
        if isinstance(token, ruamel.yaml.tokens.DocumentStartToken):
            break
        elif isinstance(token, ruamel.yaml.tokens.DirectiveToken) and token.name == 'TAG':
            handle, prefix = token.value
            if not prefix.startswith('tag:yaml-macros:'): break

            macro_path = prefix.split(':')[2]
            macros = load_macros(macro_path)

            yaml.Constructor.add_multi_constructor(handle,
                lambda loader, suffix, node: apply_transformation(loader, node, macros[suffix])
            )

    if context:
        with Context(context):
            return yaml.load(input)
    else:
        return yaml.load(input)

def build_yaml_macros(input, output=None, context=None):
    syntax = process_macros(input, context)
    yaml = get_yaml_instance()

    yaml.dump(syntax, stream=output)
