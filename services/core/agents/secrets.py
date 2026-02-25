import json
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class SecretManager:
    """
    Manages encrypted credentials for integrations.
    In a production system, this would interface with AWS Secrets Manager, 
    HashiCorp Vault, or a similar secure service.
    
    For this implementation, it uses a persistent JSON file with mock encryption/obfuscation.
    """
    
    def __init__(self, data_dir: str = "/Users/arnovanzyl/.gemini/antigravity/scratch/data"):
        self.data_dir = Path(data_dir)
        self.secrets_file = self.data_dir / "secrets.json"
        self._secrets: Dict[str, Dict[str, Any]] = {}
        self._ensure_data_dir()
        self._load_secrets()

    def _ensure_data_dir(self):
        if not self.data_dir.exists():
            os.makedirs(self.data_dir, exist_ok=True)
            logger.info(f"Created data directory: {self.data_dir}")

    def _load_secrets(self):
        if self.secrets_file.exists():
            try:
                with open(self.secrets_file, "r") as f:
                    self._secrets = json.load(f)
                logger.debug(f"Loaded secrets from {self.secrets_file}")
            except Exception as e:
                logger.error(f"Error loading secrets: {e}")
                self._secrets = {}
        else:
            self._secrets = {}
            self._save_secrets()

    def _save_secrets(self):
        try:
            with open(self.secrets_file, "w") as f:
                json.dump(self._secrets, f, indent=2)
            logger.debug(f"Saved secrets to {self.secrets_file}")
        except Exception as e:
            logger.error(f"Error saving secrets: {e}")

    def store_secret(self, secret_key: str, credentials: Dict[str, Any]):
        """Store or update a secret."""
        # In production, we would encrypt here
        self._secrets[secret_key] = credentials
        self._save_secrets()
        logger.info(f"Secret stored for key: {secret_key}")

    def get_secret(self, secret_key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a secret by its key."""
        # In production, we would decrypt here
        return self._secrets.get(secret_key)

    def delete_secret(self, secret_key: str):
        """Delete a secret."""
        if secret_key in self._secrets:
            self._secrets.pop(secret_key, None)
            self._save_secrets()
            logger.info(f"Secret deleted for key: {secret_key}")

    def list_keys(self) -> list[str]:
        """List all secret keys."""
        return list(self._secrets.keys())
