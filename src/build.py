import os
import time
import traceback
from os import path

from YAMLMacros.src.engine import MacroError, process_macros
from YAMLMacros.src.yaml_provider import get_yaml_instance

EXT_DOT_SUBLIME_SYNTAX_YAML_MACROS = '.sublime-syntax.yaml-macros'


class SilentException(Exception):
    """Control-flow exception, assumes that the actual error was already handled."""


def build(source_path, target_path, error_stream, arguments, error_highlighter):
    # Note: messages indicating key phases of the build process are right-aligned
    # on their first word, which is a verb like 'Compiling', 'Finished' etc.
    # Current width is 12 characters, excluding white-space after verb.

    t0 = time.perf_counter()

    def done(ok: bool):
        if ok:
            message = '   [Finished in {elapsed:.1f}s]'
        else:
            # Not worth aligning, since errors are already cluttering the screen anyway.
            message = '[Finished in {elapsed:.1f}s with errors]'
        elapsed = time.perf_counter() - t0
        error_stream.print(message.format(elapsed=elapsed))

    def handle_error(e):
        if isinstance(e, SilentException):
            return
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
        # Derive target from source, if not set explicitly.
        if target_path is None:
            # Assume that source is a `*.sublime-syntax.yaml-macros` file,
            # so the target would be just `*.sublime-syntax` without `.yaml-macros` extension.
            target_path, _ = path.splitext(source_path)

        error_stream.print('   Compiling %s (%s)' % (path.basename(source_path), source_path))

        # Bail out if file extension is not supported.
        if not source_path.endswith(EXT_DOT_SUBLIME_SYNTAX_YAML_MACROS):
            # Just a regular message, shouldn't be right-aligned.
            error_stream.print()
            error_stream.print('Error: Source is not a YAML Macros file!')
            error_stream.print('Hint: Make sure source file has `{}` extension.'
                               .format(EXT_DOT_SUBLIME_SYNTAX_YAML_MACROS))
            error_stream.print()
            raise SilentException()

        working_dir = arguments['working_dir']
        if working_dir is not None:
            os.chdir(working_dir)

        with open(source_path, 'r') as source_file:
            source_text = source_file.read()

        result = process_macros(source_text, arguments=arguments)

        error_stream.print('    Building %s (%s)' % (path.basename(target_path), target_path))

        serializer = get_yaml_instance()
        with open(target_path, 'w') as output_file:
            serializer.dump(result, stream=output_file)

    except Exception as e:
        handle_error(e)
        done(ok=False)

    else:
        done(ok=True)
