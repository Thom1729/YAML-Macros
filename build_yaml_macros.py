import sublime
import sublime_plugin

import os
from os import path
import traceback

from YAMLMacros.api import process_macros
from YAMLMacros.api import get_yaml_instance
from YAMLMacros.api import MacroError

from YAMLMacros.src.output_panel import OutputPanel
from YAMLMacros.src.phantom_manager import PhantomManager

PHANTOM_TEMPLATE="""
<div class="error">{}</div>
"""

class BuildYamlMacrosCommand(sublime_plugin.WindowCommand):
    def run(self, working_dir=None):
        if working_dir:
            os.chdir(working_dir)

        view = self.window.active_view()
        source_path = view.file_name()

        output_path, extension = path.splitext(source_path)

        if extension != '.yaml-macros': raise "Not a .yaml-macros file!"

        panel = OutputPanel(self.window, 'YAMLMacros')
        panel.show()
        panel.print('Building %s...' % source_path)

        phantoms = PhantomManager(view, 'YAMLMacros', template=PHANTOM_TEMPLATE)
        phantoms.clear()

        try:
            result = process_macros(
                view.substr( sublime.Region(0, view.size()) ),
                arguments={ "file_path": source_path },
            )
        except MacroError as e:
            region = sublime.Region(
                e.node.start_mark.index,
                e.node.end_mark.index,
            )
            panel.print(e.message)

            if e.__cause__:
                cause = e.__cause__
                panel.print(''.join(traceback.format_exception(
                    None,
                    cause,
                    cause.__traceback__
                )))
            else:
                panel.print(str(e.node.start_mark))

            phantoms.add(region, e.message)

            panel.print('[Failure]')
            return
        except Exception as e:
            panel.print(str(e))
            panel.print('[Failure]')
            return

        serializer = get_yaml_instance()

        with open(output_path, 'w') as output_file:
            serializer.dump(result, stream=output_file)
            panel.print('Compiled to %s.' % output_path)
            panel.print('[Success]')
