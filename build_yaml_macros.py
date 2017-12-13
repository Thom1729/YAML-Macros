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

PHANTOM_TEMPLATE="""
<div class="error">{}</div>
"""

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

        panel = OutputPanel(self.window, build_id)
        panel.show()
        panel.print('Building %s... (%s)' % (path.basename(source_path), source_path))

        for v in self.window.views():
            v.erase_phantoms('YAMLMacros')

        build(source_text, destination_path, panel, arguments, self.window.find_open_file)

def build(source_text, destination_path, errors, arguments, find_view):
    def done(message):
        errors.print('[{message} in {time:.2} seconds.]\n'.format(
            message=message,
            time = time.perf_counter() - t0
        ))

    def handle_error(e):
        if isinstance(e, MacroError):
            errors.print('')
            errors.print(e.message)
            errors.print(str(e.node.start_mark))

            if e.__cause__:
                handle_error(e.__cause__)

            v = find_view(e.context.get('file_path'))
            if v:
                v.add_phantom(
                    'YAMLMacros',
                    sublime.Region(e.node.start_mark.index, e.node.end_mark.index),
                    PHANTOM_TEMPLATE.format(e.message),
                    sublime.LAYOUT_BELOW,
                )
        else:
            errors.print('')
            errors.print(''.join(traceback.format_exception(None, e, e.__traceback__)))

    t0 = time.perf_counter()

    try:
        result = process_macros(source_text, arguments=arguments)
    except Exception as e:
        handle_error(e)
        done('Failed')
        return

    serializer = get_yaml_instance()

    with open(destination_path, 'w') as output_file:
        serializer.dump(result, stream=output_file)
        errors.print('Compiled to %s. (%s)' % (path.basename(destination_path), destination_path))
        done('Succeeded')