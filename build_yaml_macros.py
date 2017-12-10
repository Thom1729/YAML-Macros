import sublime
import sublime_plugin

import os
from os import path

from YAMLMacros.src.build import process_macros
from YAMLMacros.src.yaml_provider import get_yaml_instance

class BuildYamlMacrosCommand(sublime_plugin.WindowCommand):
    def run(self, working_dir=None):
        if working_dir:
            os.chdir(working_dir)

        view = self.window.active_view()
        source_path = view.file_name()

        output_path, extension = path.splitext(source_path)

        if extension != '.yaml-macros': raise "Not a .yaml-macros file!"

        result = process_macros(
            view.substr( sublime.Region(0, view.size()) ),
            context={
                "file_path": source_path
            },
        )

        serializer = get_yaml_instance()

        with open(output_path, 'w') as output_file:
            serializer.dump(result, stream=output_file)
