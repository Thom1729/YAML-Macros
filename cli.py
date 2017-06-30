#!/usr/bin/python

import os
import sys
from argparse import ArgumentParser

from .src.build import build_yaml_macros

parser = ArgumentParser()

parser.add_argument(
    "-m", "--macros-path",
    default=os.getcwd(),
    help="path to search for macro definitions",
)

args = parser.parse_args()

print(build_yaml_macros(
    input = sys.stdin.read(),
    macros_search_path=args.macros_path,
))