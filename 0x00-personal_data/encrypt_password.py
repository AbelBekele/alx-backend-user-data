#!/usr/bin/env python3
"""
    Encrypt a string
"""
import bcrypt


def hash_password(password: str = '') -> bytes:
    """
        Hashed the password

        Args:
            password: string to hashed

        Return:
            hashed password
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'),
                           bcrypt.gensalt(prefix=b"2b"))

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
        Look if is valid password

        Args:
            hashed_password: Password encrypt
            password: string to hashed

        Return:
            True If this are equals
    """
    valid = bcrypt.checkpw(password.encode('utf-8'),
                           hashed_password)

    return valid
