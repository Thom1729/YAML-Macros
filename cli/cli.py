#!/bin/env python3

import sys
from os import path

sys.path.append(
    path.join(path.dirname(path.realpath(__file__)), '../..')
)

from yamlmacros import process_macros
from yamlmacros import get_yaml_instance

result = process_macros(sys.stdin.read())

serializer = get_yaml_instance()
serializer.dump(result, stream=sys.stdout)
