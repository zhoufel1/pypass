#!/usr/bin/env python3
import base64 
import os 
import bcrypt

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def key_generator(password: str):
    """Return bytes representing a generated key"""
    encoded_pass = password.encode() 
    salt = b'\xbf\x07\xfc\xb2Y\x80\xbas\xb4\x02\x0f\x84\x9da\xb3\xfb' 
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = salt,
        iterations = 100000,
        backend = default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(encoded_pass))


def encrypt_password(password: str, key: bytes):
    """Return a string representing a password encrypted using Fernet given the key to be 
    stored in the database"""
    f = Fernet(key)
    return f.encrypt(password.encode()).decode('utf-8')


def decrypt_password(encrypted_pass: str, key: bytes):
    """Return a string representing a password retrieved from the database decrypted using 
    Fernet given the key"""  
    f = Fernet(key)
    return f.decrypt(encrypted_pass.encode()).decode('utf-8')


def hash_password(password: str):
    """Returns bytes representing a hashed password"""
    return bcrypt.hashpw(password, bcrypt.gensalt())
    