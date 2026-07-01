from pathlib import Path
from uuid import uuid4

from app.core.config import settings
from app.storage.base import StorageService


class LocalStorageService(StorageService):
    def __init__(self, upload_dir: str | None = None) -> None:
        self.base_dir = Path(upload_dir or settings.upload_dir)

    def save_file(self, filename: str, content: bytes, subdirectory: str) -> str:
        target_dir = self.base_dir / subdirectory
        target_dir.mkdir(parents=True, exist_ok=True)
        safe_name = f"{uuid4().hex}_{Path(filename).name}"
        file_path = target_dir / safe_name
        file_path.write_bytes(content)
        return str(file_path.relative_to(self.base_dir))

    def delete_file(self, relative_path: str) -> None:
        file_path = self.get_file_path(relative_path)
        if file_path.exists():
            file_path.unlink()

    def get_file_path(self, relative_path: str) -> Path:
        return self.base_dir / relative_path
