import sublime

import traceback
import time
from os import path

from YAMLMacros.api import process_macros
from YAMLMacros.api import get_yaml_instance
from YAMLMacros.api import MacroError

def build(source_text, destination_path, panel, arguments, window):
    t0 = time.perf_counter()

    panel.print('Building %s... (%s)' % (path.basename(arguments['file_path']), arguments['file_path']))

    for v in window.views():
        v.erase_phantoms('YAMLMacros')

    def done(message):
        panel.print('[{message} in {time:.2} seconds.]\n'.format(
            message=message,
            time = time.perf_counter() - t0
        ))

    def handle_error(e):
        if isinstance(e, MacroError):
            panel.print()
            panel.print(e.message)
            panel.print(str(e.node.start_mark))

            if e.__cause__:
                handle_error(e.__cause__)

            v = window.find_open_file(e.context.get('file_path'))
            if v:
                v.add_phantom(
                    'YAMLMacros',
                    sublime.Region(e.node.start_mark.index, e.node.end_mark.index),
                    PHANTOM_TEMPLATE.format(e.message),
                    sublime.LAYOUT_BELOW,
                )
        else:
            panel.print()
            panel.print(''.join(traceback.format_exception(None, e, e.__traceback__)))

    try:
        result = process_macros(source_text, arguments=arguments)
    except Exception as e:
        handle_error(e)
        done('Failed')
        return

    serializer = get_yaml_instance()

    with open(destination_path, 'w') as output_file:
        serializer.dump(result, stream=output_file)
        panel.print('Compiled to %s. (%s)' % (path.basename(destination_path), destination_path))
        done('Succeeded')