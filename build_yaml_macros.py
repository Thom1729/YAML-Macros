import sublime
import sublime_plugin

import os
from os import path

from YAMLMacros.api import build
from YAMLMacros.src.output_panel import OutputPanel
from YAMLMacros.src.error_highlighter import ErrorHighlighter

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
            if extension != '.yaml-macros':
                raise TypeError("Not a .yaml-macros file! Hint: add .yaml-macros extension.")

        arguments['file_path'] = source_path

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
