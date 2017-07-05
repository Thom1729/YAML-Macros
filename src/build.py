import os
import sys
from os import path
import importlib
from inspect import signature, Parameter

import ruamel.yaml

from ruamel.yaml.comments import CommentedMap

def load_macros(macro_path):
    sys.path.append(os.getcwd())
    module = importlib.import_module(macro_path)

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
            ret = CommentedMap()
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

def get_constructor(transform):
    return lambda loader, node: apply_transformation(loader, node, transform)

def build_yaml_macros(input, output, context={}):
    yaml = ruamel.yaml.YAML()
    yaml.version = (1,2)

    for token in ruamel.yaml.scan(input):
        if isinstance(token, ruamel.yaml.tokens.DocumentStartToken):
            break
        elif isinstance(token, ruamel.yaml.tokens.DirectiveToken) and token.name == 'TAG':
            handle, prefix = token.value
            if not prefix.startswith('tag:yaml-macros:'): break

            macro_path = prefix.split(':')[2]
            for name, transform in load_macros(macro_path):
                yaml.constructor.add_constructor(handle+name, get_constructor(transform))

    syntax = yaml.load(input)

    yaml.dump(syntax, stream=output)
