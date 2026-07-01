"""Local file storage implementation."""

import os
import aiofiles
from pathlib import Path

from app.core.config import settings
from app.utils.storage.base import StorageService


class LocalStorageService(StorageService):
    """Local file storage implementation."""

    def __init__(self):
        self.base_dir = Path(settings.upload_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file_path: str, file_content: bytes) -> str:
        """Save file to local directory."""
        full_path = self.base_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(full_path, "wb") as f:
            await f.write(file_content)

        return str(full_path)

    async def delete_file(self, file_path: str) -> bool:
        """Delete file from local directory."""
        full_path = self.base_dir / file_path
        try:
            if full_path.exists():
                full_path.unlink()
            return True
        except Exception:
            return False

    async def get_file_path(self, file_path: str) -> str:
        """Get file path for serving."""
        return f"/uploads/{file_path}"


# Singleton instance
storage_service = LocalStorageService()
