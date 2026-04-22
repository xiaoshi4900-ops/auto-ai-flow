import base64


def encrypt_api_key(key: str, secret: str = "default-secret") -> str:
    payload = f"{secret}:{key}".encode()
    token = base64.urlsafe_b64encode(payload).decode()
    return f"v1:{token}"


def decrypt_api_key(encrypted: str, secret: str = "default-secret") -> str:
    if not encrypted:
        return ""
    if not encrypted.startswith("v1:"):
        return encrypted
    raw = encrypted[3:]
    try:
        decoded = base64.urlsafe_b64decode(raw.encode()).decode()
    except Exception:
        return ""
    prefix = f"{secret}:"
    if not decoded.startswith(prefix):
        return ""
    return decoded[len(prefix):]
