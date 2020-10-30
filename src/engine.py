import functools
import importlib
import io
import os
import sys
from inspect import Parameter, signature

import ruamel.yaml
from YAMLMacros.src.context import get_context
from YAMLMacros.src.context import set_context
from YAMLMacros.src.util import apply, merge
from YAMLMacros.src.yaml_provider import get_yaml_instance


class MacroError(Exception):
    def __init__(self, message, node):
        self.message = message
        self.node = node
        self.context = get_context()


def load_macros(macro_path):
    sys.path.append(os.getcwd())
    try:
        module = importlib.import_module(macro_path)

        return {
            name.rstrip('_'): func
            for name, func in module.__dict__.items()
            if callable(func) and not name.startswith('_')
        }
    finally:
        sys.path.pop()


def apply_transformation(loader, node, transform):
    if getattr(transform, 'raw', False):
        def eval_(node_, arguments=None):
            if arguments:
                with set_context(**arguments):
                    return eval_(node_)

            return loader.construct_object(node_, deep=True)

        return transform(node, arguments=get_context(), eval=eval_)
    else:
        if isinstance(node, ruamel.yaml.ScalarNode):
            args = loader.construct_scalar(node)
        elif isinstance(node, ruamel.yaml.SequenceNode):
            args = loader.construct_sequence(node)
        elif isinstance(node, ruamel.yaml.MappingNode):
            args = ruamel.yaml.comments.CommentedMap()
            loader.construct_mapping(node, args)

            if any(
                    param.kind == Parameter.VAR_POSITIONAL
                    for name, param in signature(transform).parameters.items()
            ):
                # Before Python 3.6, **kwargs will not preserve order.
                args = list(args.items())
        else:
            # Unknown node type
            raise NotImplementedError

        return apply(transform, args)


def macro_multi_constructor(macros):
    def multi_constructor(loader, suffix, node):
        try:
            macro = macros[suffix]
        except KeyError as e:
            raise MacroError('Unknown macro "%s".' % suffix, node) from e

        try:
            return apply_transformation(loader, node, macros[suffix])
        except Exception as e:
            raise MacroError('Error in macro execution.', node) from e

    return multi_constructor


@functools.lru_cache(maxsize=16)
def get_parse(input_):
    yaml = get_yaml_instance()
    stream = io.StringIO(input_)

    yaml.get_constructor_parser(stream)
    tree = yaml.composer.get_single_node()
    macros = [
        (handle, tag.split(':')[2])
        for handle, tag in yaml.parser.tag_handles.items()
        if tag.startswith('tag:yaml-macros:')
    ]

    return tree, macros


def process_macros(input_, arguments=None):
    if arguments is None:
        arguments = {}
    with set_context(**arguments):
        tree, macros = get_parse(input_)

        yaml = get_yaml_instance()

        for handle, macro_path in macros:
            macros = merge(*[load_macros(path) for path in macro_path.split(',')])

            yaml.Constructor.add_multi_constructor(
                handle,
                macro_multi_constructor(macros)
            )

        return yaml.constructor.construct_document(tree)


def build_yaml_macros(input_, output=None, context=None):
    syntax = process_macros(input_, context)
    yaml = get_yaml_instance()

    yaml.dump(syntax, stream=output)
