import sublime
import sublime_plugin

import os
from os import path
import traceback
import time

from YAMLMacros.api import process_macros
from YAMLMacros.api import get_yaml_instance
from YAMLMacros.api import MacroError

from YAMLMacros.src.output_panel import OutputPanel
from YAMLMacros.src.phantom_manager import PhantomManager

PHANTOM_TEMPLATE="""
<div class="error">{}</div>
"""

class BuildYamlMacrosCommand(sublime_plugin.WindowCommand):
    def run(self, *, source_path=None, destination_path=None, working_dir=None, arguments={}, build_id='YAMLMacros'):
        t0 = time.perf_counter()

        if working_dir:
            os.chdir(working_dir)

        if source_path:
            view = self.window.find_open_file(source_path)
        else:
            view = self.window.active_view()
            source_path = view.file_name()

        with open(source_path, 'r') as source_file:
            source_text = source_file.read()

        if not destination_path:
            destination_path, extension = path.splitext(source_path)
            if extension != '.yaml-macros': raise "Not a .yaml-macros file!"

        arguments['file_path'] = source_path

        panel = OutputPanel(self.window, build_id)
        panel.show()
        panel.print('Building %s... (%s)' % (path.basename(source_path), source_path))

        def done(message):
            panel.print('[{message} in {time:.2} seconds.]\n'.format(
                message=message,
                time = time.perf_counter() - t0
            ))

        if view:
            phantoms = PhantomManager(view, 'YAMLMacros', template=PHANTOM_TEMPLATE)
            phantoms.clear()

        try:
            result = process_macros(source_text, arguments=arguments)
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

            if view:
                phantoms.add(region, e.message)

            done('Failed')
            return
        except Exception as e:
            panel.print(str(e))
            done('Failed')
            raise e
            return

        serializer = get_yaml_instance()

        with open(destination_path, 'w') as output_file:
            serializer.dump(result, stream=output_file)
            panel.print('Compiled to %s. (%s)' % (path.basename(destination_path), destination_path))
            done('Succeeded')
