import ruamel.yaml
from collections import OrderedDict

def clone_class(klass):
    return type(
        'Cloned' + klass.__name__,
        (klass, object),
        {}
    )

def get_yaml_instance(
    version = (1, 2),
    indent = { 'mapping': 2, 'sequence': 4, 'offset': 2 },
    **kwargs
):
    yaml = ruamel.yaml.YAML(**kwargs)

    yaml.Constructor = clone_class(yaml.Constructor)
    yaml.Representer = clone_class(yaml.Representer)

    yaml.version = version
    yaml.indent(**indent);

    yaml.Representer.add_representer(OrderedDict, lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data))

    return yaml
