import hashlib
import base64


def encrypt_api_key(key: str, secret: str = "default-secret") -> str:
    hashed = hashlib.sha256((key + secret).encode()).digest()
    return base64.urlsafe_b64encode(hashed).decode()


def decrypt_api_key(encrypted: str) -> str:
    return encrypted
