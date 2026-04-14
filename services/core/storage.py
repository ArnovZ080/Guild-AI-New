"""
Guild-AI File Storage
Supports local filesystem and Supabase Storage backends.
"""
import os
import uuid
import logging
from pathlib import Path
from typing import Optional

from services.core.config import settings

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path(settings.MEDIA_UPLOAD_DIR)


class StorageBackend:
    """Abstract storage interface."""

    async def save(self, file_bytes: bytes, filename: str, mime_type: str, user_id: str) -> str:
        """Save file, return public URL."""
        raise NotImplementedError

    async def delete(self, storage_url: str) -> bool:
        """Delete a file. Return True if deleted."""
        raise NotImplementedError

    async def get_url(self, storage_path: str) -> str:
        """Get a public/signed URL for the file."""
        raise NotImplementedError


class LocalStorage(StorageBackend):
    """Store files on local filesystem. Serve via FastAPI static files."""

    def __init__(self):
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    async def save(self, file_bytes: bytes, filename: str, mime_type: str, user_id: str) -> str:
        user_dir = UPLOAD_DIR / user_id
        user_dir.mkdir(parents=True, exist_ok=True)

        ext = Path(filename).suffix or ".jpg"
        stored_name = f"{uuid.uuid4().hex}{ext}"
        file_path = user_dir / stored_name

        file_path.write_bytes(file_bytes)

        # Return URL path (served by FastAPI static mount)
        return f"/media/{user_id}/{stored_name}"

    async def delete(self, storage_url: str) -> bool:
        relative = storage_url.replace("/media/", "")
        file_path = UPLOAD_DIR / relative
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    async def get_url(self, storage_path: str) -> str:
        return storage_path


class SupabaseStorage(StorageBackend):
    """Store files in Supabase Storage (S3-compatible)."""

    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from supabase import create_client
                self._client = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_SERVICE_KEY or "",
                )
            except Exception as e:
                logger.error("Supabase client init failed: %s", e)
                raise
        return self._client

    async def save(self, file_bytes: bytes, filename: str, mime_type: str, user_id: str) -> str:
        client = self._get_client()
        ext = Path(filename).suffix or ".jpg"
        storage_path = f"{user_id}/{uuid.uuid4().hex}{ext}"

        bucket = settings.SUPABASE_STORAGE_BUCKET
        try:
            client.storage.from_(bucket).upload(
                path=storage_path,
                file=file_bytes,
                file_options={"content-type": mime_type},
            )
        except Exception as e:
            # If bucket doesn't exist, try creating it
            if "not found" in str(e).lower() or "404" in str(e):
                logger.info("Creating storage bucket '%s'", bucket)
                client.storage.create_bucket(bucket, options={"public": True})
                client.storage.from_(bucket).upload(
                    path=storage_path,
                    file=file_bytes,
                    file_options={"content-type": mime_type},
                )
            else:
                raise

        # Return public URL
        public_url = client.storage.from_(bucket).get_public_url(storage_path)
        return public_url

    async def delete(self, storage_url: str) -> bool:
        client = self._get_client()
        bucket = settings.SUPABASE_STORAGE_BUCKET

        # Extract path from URL
        # URL format: https://xxx.supabase.co/storage/v1/object/public/media/user_id/filename
        try:
            path_part = storage_url.split(f"/{bucket}/")[-1]
            client.storage.from_(bucket).remove([path_part])
            return True
        except Exception as e:
            logger.warning("Supabase delete failed: %s", e)
            return False

    async def get_url(self, storage_path: str) -> str:
        client = self._get_client()
        return client.storage.from_(settings.SUPABASE_STORAGE_BUCKET).get_public_url(storage_path)


# Factory — select backend based on config
def get_storage() -> StorageBackend:
    backend = getattr(settings, "STORAGE_BACKEND", "local")
    if backend == "supabase":
        return SupabaseStorage()
    return LocalStorage()


storage = get_storage()
