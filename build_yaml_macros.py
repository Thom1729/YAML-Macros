import sublime
import sublime_plugin

import os
from os import path

from .src.build import build_yaml_macros

class BuildYamlMacrosCommand(sublime_plugin.WindowCommand):
    def run(self, working_dir=None):
        if working_dir:
            os.chdir(working_dir)

        view = self.window.active_view();
        source_path = view.file_name()

        output_path, extension = path.splitext(source_path)

        if extension != '.yaml-macros': raise "Not a .yaml-macros file!"

        with open(output_path, 'w') as output_file:

            build_yaml_macros(
                view.substr( sublime.Region(0, view.size()) ),
                output_file,
                {
                    "file_path": source_path
                },
            )
