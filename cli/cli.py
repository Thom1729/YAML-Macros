#!/bin/env python3

import sys
from os import path

sys.path.append(
    path.join(path.dirname(path.realpath(__file__)), '../..')
)

from YAMLMacros.api import process_macros
from YAMLMacros.api import get_yaml_instance

result = process_macros(sys.stdin.read())

serializer = get_yaml_instance()
serializer.dump(result, stream=sys.stdout)