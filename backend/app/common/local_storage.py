import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from app.common.file_manager import FileManager
from typing import List


class LocalFileManager(FileManager):

    def __init__(self, base_directory: str):
        self.base_directory = base_directory

    def _full_path(self, path: str) -> str:
        '''
        Generate the full path for the given relative path.
        '''
        return os.path.join(self.base_directory, path)

    def save(self, file: FileStorage, directory: str = '') -> str:
        '''
        Save the file to the given directory within the base directory.
        '''
        filename = secure_filename(file.filename)
        if directory:
            full_path = self._full_path(os.path.join(directory, filename))
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
        else:
            full_path = self._full_path(filename)

        file.save(full_path)
        return full_path

    def delete(self, path: str) -> bool:
        '''
        Delete the file at the given path.
        '''
        full_path = self._full_path(path)
        if os.path.isfile(full_path):
            os.remove(full_path)
            return True
        return False

    def list_files(self, directory: str = '') -> List[str]:
        '''List all files in a directory.'''
        full_path = self._full_path(directory)
        return [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]

    def update_file(self, file: FileStorage, path: str) -> str:
        '''Update an existing file.'''
        full_path = self._full_path(path)
        if os.path.isfile(full_path):
            os.remove(full_path)
        file.save(full_path)
        return full_path

    def get_path(self, filename: str, directory: str = '') -> str:
        '''
        Get the full path to the file in the given directory.
        '''
        if directory:
            return self._full_path(os.path.join(directory, filename))
        return self._full_path(filename)

# Example usage:
# file_manager = LocalFileManager('/path/to/base/directory')
# file_manager.save(file, 'uploads')
# file_manager.list_files('uploads')
# file_manager.update_file(file, 'uploads/updatedfile.txt')
# file_manager.delete('uploads/myfile.txt')
