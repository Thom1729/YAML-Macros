import sublime
import sublime_plugin

from os import path

from .src.build import build_yaml_macros

class BuildYamlMacrosCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view();
        source_path = view.file_name()

        output_path, extension = path.splitext(source_path)

        if extension != '.yaml-macros': raise "Not a .yaml-macros file!"

        output_file = open(output_path, 'w')

        build_yaml_macros(
            view.substr( sublime.Region(0, view.size()) ),
            output_file,
            path.dirname(source_path),
        )
