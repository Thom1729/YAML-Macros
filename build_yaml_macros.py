import sublime
import sublime_plugin

from os import path

from . import build

class BuildYamlMacrosCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view();

        result = build.build_yaml_macros(
            view.substr( sublime.Region(0, view.size()) )
        )

        source_path = view.file_name()

        output_path, extension = path.splitext(path.basename(source_path))
        if extension != '.yaml-macros': raise "Not a .yaml-macros file!"

        output_file = open(output_path, 'w')
        output_file.write(result)
