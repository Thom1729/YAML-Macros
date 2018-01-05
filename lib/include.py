from YAMLMacros.api import process_macros

def include(path):
    with open(path, 'r') as file:
        return process_macros(
            file.read(),
            arguments={ "file_path": path },
        )

def include_resource(resource):
    import sublime
    import os
    file_path = os.path.join( sublime.packages_path(), resource )
    file_contents = sublime.load_resource(resource)
    return process_macros(
        file_contents,
        arguments={ "file_path": file_path },
    )
