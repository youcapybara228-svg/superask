from cryptography.fernet import Fernet

from src.config import config


def _get_cipher() -> Fernet:
    return Fernet(config.encryption_key.encode())


def save_password(password: str):
    cipher = _get_cipher()
    encrypted = cipher.encrypt(password.encode())
    config.sua_password_path.write_bytes(encrypted)
    config.sua_password = password


def get_password() -> str | None:
    if config.sua_password:
        return config.sua_password
    try:
        if config.sua_password_path.exists():
            cipher = _get_cipher()
            encrypted = config.sua_password_path.read_bytes()
            password = cipher.decrypt(encrypted).decode()
            config.sua_password = password
            return password
    except Exception:
        return None
    return None


def clear_password():
    config.sua_password = ""
    if config.sua_password_path.exists():
        config.sua_password_path.unlink()
