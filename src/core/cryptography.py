import os
import json
import base64
from hashlib import sha256
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class SentinelSecurityCore:
    def __init__(self, user_secret_passphrase: str):
        self.key = sha256(user_secret_passphrase.encode()).digest()
        self.aesgcm = AESGCM(self.key)

    def encrypt_payload(self, data_dict: dict) -> dict:
        serialized = json.dumps(data_dict).encode('utf-8')
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, serialized, None)
        return {
            "cipher_algorithm": "AES-256-GCM",
            "nonce_b64": base64.b64encode(nonce).decode('utf-8'),
            "ciphertext_b64": base64.b64encode(ciphertext).decode('utf-8')
        }

    def decrypt_payload(self, envelope: dict) -> dict:
        nonce = base64.b64decode(envelope["nonce_b64"])
        ciphertext = base64.b64decode(envelope["ciphertext_b64"])
        decrypted_bytes = self.aesgcm.decrypt(nonce, ciphertext, None)
        return json.loads(decrypted_bytes.decode('utf-8'))
