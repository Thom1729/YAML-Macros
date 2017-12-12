from os import path
from zipfile import ZipFile

class SublimeResources():
    platform_data_paths = {
        'Windows': r'%APPDATA%\Sublime Text 3',
        'Linux': r'~/.config/sublime-text-3',
        'Darwin': r'~/Library/Application Support/Sublime Text 3'
    }

    @classmethod
    def get_data_path(cls):
        import platform
        data_path = path.expandvars(platform_data_paths[platform.system()])

    @classmethod
    def find_resources(cls, glob):
        try:
            from sublime import find_resources as sublime_find_resources
            return sublime_find_resources(glob)
        except ImportError:
            # TODO: find all files that match the given glob, by searching through:
            #       - loose files in the data Packages folder
            #       - files in a .sublime-package file in the Installed Packages folder
            #       - files in a .sublime-package file in the ST installation Packages folder
            #         (where no .sublime-package file with the same name exists in the Installed Packages folder)
            #       and then sort them according to lexographical order (first, ignore duplicates by using a "set")
            return []

    @classmethod
    def load_resource(cls, package_path):
        try:
            from sublime import load_resource as sublime_load_resource
            return sublime_load_resource(package_path)
        except ImportError:
            if package_path.startswith('Packages/'):
                data_path = get_data_path()
                
                # if the file exists in the Packages folder, return that
                full_path = path.join(data_path, package_path)
                if path.isfile(full_path):
                    with open(full_path, 'r', encoding='utf-8') as file:
                        return file.read()
                
                # otherwise, it must exist in a .sublime-package file, if at all
                # so find the Package name, and the path inside the zip file
                package_name, sub_path = package_path[len('Packages/'):].split('/', 1)
                
                # look in the relevant Installed Packages .sublime-package file, if it exists
                full_path = path.join(data_path, 'Installed Packages/', package_name, '.sublime-package')
                if path.isfile(full_path):
                    return get_file_from_zip(full_path, sub_path)
                
                # TODO: otherwise, try the ST installation path
                pass

            raise IOError('resource not found')

    @classmethod
    def get_files_in_zip(cls, zipfile_path):
        with ZipFile(zipfile_path, 'r') as z:
            return z.namelist()

    @classmethod
    def get_file_from_zip(cls, zipfile_path, path_inside_zip):
        with ZipFile(zipfile_path, 'r') as z:
            with z.open(path_inside_zip, 'r', 'utf-8') as file:
                return file.read()
