import yaml
from os import path
import sys
import imp
from inspect import signature, Parameter

from .yamlordereddictloader import yamlordereddictloader

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
        if isinstance(node, yaml.ScalarNode):
            return transform(loader.construct_scalar(node))
        elif isinstance(node, yaml.SequenceNode):
            return transform(*loader.construct_sequence(node))
        elif isinstance(node, yaml.MappingNode):
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
    for token in yaml.scan(input):
        if isinstance(token, yaml.tokens.DocumentStartToken):
            break
        elif isinstance(token, yaml.tokens.DirectiveToken) and token.name == 'TAG':
            handle, prefix = token.value
            if not prefix.startswith('tag:yaml-macros:'): break
            macro_path = path.join(macros_search_path, prefix.split(':')[2])
            for name, transform in load_macros(macro_path):
                yaml.add_constructor(prefix+name, get_constructor(transform))

    syntax = yaml.load(input, Loader=yamlordereddictloader.Loader)

    return yaml.dump(syntax,
        version=(1,2),
        default_flow_style=False,
        tags=False,
        Dumper=yamlordereddictloader.Dumper
    )