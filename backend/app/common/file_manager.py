from abc import ABC, abstractmethod
from werkzeug.datastructures import FileStorage
from typing import List


class FileManager(ABC):

    @abstractmethod
    def save(self, file: FileStorage, path: str) -> str:
        '''Save a file and return the path.'''
        pass

    @abstractmethod
    def delete(self, path: str) -> bool:
        '''Delete a file.'''
        pass

    @abstractmethod
    def list_files(self, directory: str) -> List[str]:
        '''List all files in a directory.'''
        pass

    @abstractmethod
    def update_file(self, file: FileStorage, path: str) -> str:
        '''Update an existing file.'''
        pass

    @abstractmethod
    def get_path(self, identifier: str) -> str:
        '''Retrieve the path to a file.'''
        pass
