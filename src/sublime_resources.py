from os import path, walk, sep
from zipfile import ZipFile
import glob
import fnmatch
import platform
try_st = False # set to False for easier testing of our custom methods when using ST

class SublimeResources():
    platform_data_paths = {
        'Windows': r'%APPDATA%\Sublime Text 3',
        'Linux': r'~/.config/sublime-text-3',
        'Darwin': r'~/Library/Application Support/Sublime Text 3'
    }

    @classmethod
    def get_portable_data_path(cls, potential_parent_of):
        """Given a path like H:\\STPortable\\3156\\Data\\Packages\\JavaScript\\JavaScript.sublime-syntax,
           it will correctly determine that the data folder is H:\\STPortable\\3156\\Data\\"""
        after_split = potential_parent_of.split('/Data/Packages/', 1)
        if len(after_split) == 1 and sep == '\\':
            after_split = potential_parent_of.split('\\Data\\Packages\\', 1)
        if len(after_split) == 1:
            return None
        return path.join(after_split[0], 'Data', '')
    
    @classmethod
    def get_data_path(cls):
        return path.expandvars(SublimeResources.platform_data_paths[platform.system()])

    @classmethod
    def find_resources(cls, glob_pattern):
        """
            find all files whose names match the given glob, by searching through:
            - loose files in the data Packages folder
            - files in a .sublime-package file in the Installed Packages folder
            - files in a .sublime-package file in the ST installation Packages folder
              (where no .sublime-package file with the same name exists in the Installed Packages folder)
            and then sort them according to lexographical order (ignoring duplicate results)
             (except with Default coming first and User last)
        """
        try:
            if try_st:
                from sublime import find_resources as sublime_find_resources
                return sublime_find_resources(glob_pattern)
        except ImportError:
            pass

        data_path = SublimeResources.get_data_path()
        matches = list()
        def found_match(path):
            # switch matches to use `/` folder sep if necessary (i.e. on Windows)
            if sep == '\\':
                path = path.replace('\\', '/')
            matches.append(path)
        
        # if a path separator exists in the glob pattern then there is no need to try to find anything - no filename will match
        if not '/' in glob_pattern:
            # loose files in the data Packages folder
            for root, dirnames, filenames in walk(path.join(data_path, 'Packages'), followlinks=True):
                for filepath in [path.join(root, filename)[len(path.join(data_path, '')):] for filename in filenames]:
                    if SublimeResources.glob_matches_filepath(filepath, glob_pattern):
                        found_match(filepath)
            
            # for each .sublime-package file in the Installed Packages folder
            for zipfile_path in glob.iglob(path.join(data_path, 'Installed Packages', '*.sublime-package')):
                matches += SublimeResources.find_files_matching_glob_in_zip(zipfile_path, glob_pattern)
            
            # search Packages subfolder of ST installation folder, where no .sublime-package file with the same name exists in the Installed Packages folder)
            for zipfile_path in glob.iglob(path.join(SublimeResources.get_st_installation_folder(), 'Packages', '*.sublime-package')):
                if not path.isfile(path.join(data_path, 'Installed Packages', path.basename(zipfile_path))):
                    matches += SublimeResources.find_files_matching_glob_in_zip(zipfile_path, glob_pattern)
            
        # use a set to remove duplicates - no such thing as an ordered set in Python 3.3, so convert back to a list
        matches = list(set(matches))
        return sorted(matches, key=SublimeResources.get_sortkey_for_package_filepath)

    @classmethod
    def glob_matches_filepath(cls, filepath, glob_pattern):
        return fnmatch.fnmatchcase(path.basename(filepath), glob_pattern)

    @classmethod
    def get_package_name_from_zipfile_name(cls, zipfile_path):
        return path.splitext(path.basename(zipfile_path))[0]

    @classmethod
    def find_files_matching_glob_in_zip(cls, zipfile_path, glob_pattern):
        package_name = SublimeResources.get_package_name_from_zipfile_name(zipfile_path)
        # get a list of files in the zip
        files = SublimeResources.get_files_in_zip(zipfile_path)
        # format the path to be relative from the Packages folder
        files = ['Packages/' + package_name + '/' + file for file in files]
        # find any that match the glob
        return [file for file in files if SublimeResources.glob_matches_filepath(file, glob_pattern)]

    @classmethod
    def split_package_filepath(cls, package_path):
        """Return a tuple with 2 args - the package name and the sub path inside the package."""
        return package_path[len('Packages/'):].split('/', 1)

    @classmethod
    def get_sortkey_for_package_filepath(cls, file_path):
        package_name, sub_path = SublimeResources.split_package_filepath(file_path)
        index = 1
        if package_name == 'Default':
            index = 0
        elif package_name == 'User':
            index = 2
        return str(index) + '/' + package_name + '/' + sub_path

    @classmethod
    def load_resource(cls, package_path):
        try:
            if try_st:
                from sublime import load_resource as sublime_load_resource
                return sublime_load_resource(package_path)
        except ImportError:
            pass

        if package_path.startswith('Packages/'):
            data_path = SublimeResources.get_data_path()
            
            # if the file exists in the Packages folder, return that
            full_path = path.join(data_path, package_path)
            if path.isfile(full_path):
                with open(full_path, 'r', encoding='utf-8') as file:
                    return file.read()
            
            # otherwise, it must exist in a .sublime-package file, if at all
            # so find the Package name, and the path inside the zip file
            package_name, sub_path = SublimeResources.split_package_filepath(package_path)
            
            # look in the relevant Installed Packages .sublime-package file, if it exists
            full_path = path.join(data_path, 'Installed Packages', package_name + '.sublime-package')
            if path.isfile(full_path):
                return SublimeResources.get_file_from_zip(full_path, sub_path)
            
            # otherwise, try the ST installation path
            full_path = path.join(SublimeResources.get_st_installation_folder(), 'Packages', package_name + '.sublime-package')
            if path.isfile(full_path):
                return SublimeResources.get_file_from_zip(full_path, sub_path)

        raise IOError('resource not found')

    @classmethod
    def get_files_in_zip(cls, zipfile_path):
        with ZipFile(zipfile_path, 'r') as z:
            return z.namelist()

    @classmethod
    def get_file_from_zip(cls, zipfile_path, path_inside_zip):
        with ZipFile(zipfile_path, 'r') as z:
            with z.open(path_inside_zip, 'r') as file:
                return file.read()

    @classmethod
    def get_st_installation_folder(cls):
        if platform.system() == 'Windows':
            import winreg
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'*\shell\Open with Sublime Text\command') as key:
                exe = winreg.QueryValue(key, None)
        else:
            # https://stackoverflow.com/a/39149470/4473405
            import shutil
            exe = shutil.which('subl')
        return path.dirname(exe)
