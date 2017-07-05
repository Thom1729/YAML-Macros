#!/bin/env python3

import sys
from os import path

sys.path.append(
    path.join(path.dirname(path.realpath(__file__)), '../..')
)

from YAMLMacros.src.build import build_yaml_macros

print(build_yaml_macros(
    input = sys.stdin.read(),
    output = sys.stdout,
))