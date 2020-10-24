import sublime
import sublime_plugin

from YAMLMacros.api import build
from YAMLMacros.src.output_panel import OutputPanel
from YAMLMacros.src.error_highlighter import ErrorHighlighter

class BuildYamlMacrosCommand(sublime_plugin.WindowCommand):
    def run(self, *, source_path=None, target_path=None, working_dir=None, arguments={}, build_id='YAMLMacros'):
        error_stream = OutputPanel(self.window, build_id)

        if source_path is None:
            source_path = self.window.active_view().file_name()

        arguments['file_path'] = source_path
        arguments['working_dir'] = working_dir

        build(
            source_path=source_path,
            target_path=target_path,
            arguments=arguments,
            error_stream=error_stream,
            error_highlighter=ErrorHighlighter(self.window, 'YAMLMacros'),
        )

class ClearViewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.erase(edit, sublime.Region(0, self.view.size()))
