import ruamel.yaml

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

    return yaml
