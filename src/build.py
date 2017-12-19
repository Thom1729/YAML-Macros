import traceback
import time
from os import path

from YAMLMacros.api import process_macros
from YAMLMacros.api import get_yaml_instance
from YAMLMacros.src.engine import MacroError

def build(source_text, destination_path, error_stream, arguments, error_highlighter):
    t0 = time.perf_counter()

    error_stream.print('Building %s... (%s)' % (path.basename(arguments['file_path']), arguments['file_path']))

    def done(message):
        error_stream.print('[{message} in {time:.2f} seconds.]\n'.format(
            message=message,
            time = time.perf_counter() - t0
        ))

    def handle_error(e):
        if isinstance(e, MacroError):
            error_stream.print()
            error_stream.print(e.message)
            error_stream.print(str(e.node.start_mark))

            if e.__cause__:
                handle_error(e.__cause__)

            error_highlighter.highlight(
                e.context.get('file_path'),
                e.node.start_mark.index,
                e.node.end_mark.index,
                e.message,
            )
        else:
            error_stream.print()
            error_stream.print(''.join(traceback.format_exception(None, e, e.__traceback__)))

    try:
        result = process_macros(source_text, arguments=arguments)
    except Exception as e:
        handle_error(e)
        done('Failed')
        return

    serializer = get_yaml_instance()

    with open(destination_path, 'w') as output_file:
        serializer.dump(result, stream=output_file)
        error_stream.print('Compiled to %s. (%s)' % (path.basename(destination_path), destination_path))
        done('Succeeded')