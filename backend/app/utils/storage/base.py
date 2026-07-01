"""Storage service interface."""

from abc import ABC, abstractmethod


class StorageService(ABC):
    """Abstract storage service interface."""

    @abstractmethod
    async def save_file(self, file_path: str, file_content: bytes) -> str:
        """Save file and return path."""
        pass

    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """Delete file."""
        pass

    @abstractmethod
    async def get_file_path(self, file_path: str) -> str:
        """Get file path for serving."""
        pass
