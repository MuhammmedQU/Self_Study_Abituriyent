"""Storage service package."""

from app.utils.storage.base import StorageService
from app.utils.storage.local_storage import storage_service

__all__ = ["StorageService", "storage_service"]
