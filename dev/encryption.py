import base64
import bcrypt
from cryptography import fernet
from cryptography.hazmat import backends
from cryptography.hazmat import primitives
from cryptography.hazmat.primitives.kdf import pbkdf2


def generate_key(password: str) -> bytes:
    encoded_password = password.encode()
    key_deriver = pbkdf2.PBKDF2HMAC(
        algorithm=primitives.hashes.SHA256(),
        length=32,
        salt=b'',
        iterations=100000,
        backend=backends.default_backend()
        )
    return base64.urlsafe_b64encode(key_deriver.derive(encoded_password))


def encrypt_password(password: str, key: bytes) -> str:
    fernet_object = fernet.Fernet(key)
    return fernet_object.encrypt(password.encode()).decode('utf-8')


def decrypt_password(encrypted_pass: str, key: bytes) -> str:
    fernet_object = fernet.Fernet(key)
    return fernet_object.decrypt(encrypted_pass.encode()).decode('utf-8')


def hash_master_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
