from abc import ABC, abstractmethod
from pathlib import Path


class StorageService(ABC):
    @abstractmethod
    def save_file(self, filename: str, content: bytes, subdirectory: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, relative_path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_file_path(self, relative_path: str) -> Path:
        raise NotImplementedError
