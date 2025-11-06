from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os
import json
from typing import Dict, Any

class EncryptionManager:
    def __init__(self, master_key_id: str):
        self.master_key_id = master_key_id
        # In production: fetch from Vault
        # For now: derive from env (DO NOT COMMIT REAL KEY)
        self._master_key = os.getenv("MASTER_ENCRYPTION_KEY", os.urandom(32))
    
    def encrypt_record(self, data: Dict[str, Any]) -> bytes:
        """Encrypt user payload with per-record nonce"""
        nonce = os.urandom(12)
        aesgcm = AESGCM(self._master_key)
        plaintext = json.dumps(data).encode()
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        return nonce + ciphertext
    
    def decrypt_record(self, encrypted: bytes) -> Dict[str, Any]:
        """Decrypt user payload"""
        nonce = encrypted[:12]
        ciphertext = encrypted[12:]
        aesgcm = AESGCM(self._master_key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return json.loads(plaintext.decode())

# Singleton instance
from .config import settings
encryption = EncryptionManager(settings.VAULT_KEY_ID)