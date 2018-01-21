import sublime
import sublime_plugin

import os
from os import path

def plugin_loaded():
    import sys
    sys.path.append('Packages/yaml_macros_engine/st3')

class BuildYamlMacrosCommand(sublime_plugin.WindowCommand):
    def run(self, *, source_path=None, destination_path=None, working_dir=None, arguments={}, build_id='YAMLMacros'):
        if working_dir:
            os.chdir(working_dir)

        if not source_path:
            source_path = self.window.active_view().file_name()

        with open(source_path, 'r') as source_file:
            source_text = source_file.read()

        if not destination_path:
            destination_path, extension = path.splitext(source_path)
            if extension != '.yaml-macros': raise "Not a .yaml-macros file!"

        arguments['file_path'] = source_path

        from yamlmacros import build
        from yamlmacros.src.output_panel import OutputPanel
        from yamlmacros.src.error_highlighter import ErrorHighlighter

        build(
            source_text=source_text,
            destination_path=destination_path,
            arguments=arguments,
            error_stream=OutputPanel(self.window, build_id),
            error_highlighter=ErrorHighlighter(self.window, 'YAMLMacros'),
        )

class ClearViewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.erase(edit, sublime.Region(0, self.view.size()))
