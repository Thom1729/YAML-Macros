# import yaml
from os import path
import sys
import imp
from inspect import signature, Parameter
from io import StringIO

import ruamel.yaml

def load_macros(macro_path):
    search_path, name = path.split(path.abspath(macro_path))

    fileObject, file, description = imp.find_module( name, [ search_path ] )
    module = imp.load_module('macros', fileObject, file, description)

    return [
        (name.rstrip('_'), func)
        for name, func in module.__dict__.items()
        if callable(func) and not name.startswith('_')
    ]

def apply_transformation(loader, node, transform):
    try:
        if isinstance(node, ruamel.yaml.ScalarNode):
            return transform(loader.construct_scalar(node))
        elif isinstance(node, ruamel.yaml.SequenceNode):
            return transform(*loader.construct_sequence(node))
        elif isinstance(node, ruamel.yaml.MappingNode):
            if any(
                param.kind == Parameter.VAR_POSITIONAL
                for name, param in signature(transform).parameters.items()
            ):
                return transform(*loader.construct_mapping(node).items())
            else:
                return transform(**loader.construct_mapping(node))
    except TypeError as e:
        raise TypeError('Failed to transform node: {}\n{}'.format(str(e), node))

def get_constructor(transform):
    return lambda loader, node: apply_transformation(loader, node, transform)

def build_yaml_macros(input, macros_search_path):
    yaml = ruamel.yaml.YAML()
    yaml.version = (1,2)

    for token in ruamel.yaml.scan(input):
        if isinstance(token, ruamel.yaml.tokens.DocumentStartToken):
            break
        elif isinstance(token, ruamel.yaml.tokens.DirectiveToken) and token.name == 'TAG':
            handle, prefix = token.value
            if not prefix.startswith('tag:yaml-macros:'): break
            macro_path = path.join(macros_search_path, prefix.split(':')[2])
            for name, transform in load_macros(macro_path):
                # yaml.constructor.add_constructor(prefix+name, get_constructor(transform))
                yaml.constructor.add_constructor(handle+name, get_constructor(transform))

    syntax = yaml.load(input)

    output = StringIO()
    yaml.dump(syntax, stream=output)
    return output.getvalue()