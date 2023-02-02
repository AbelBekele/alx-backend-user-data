#!/usr/bin/env python3
"""Some random docstring"""


def hash_password(password: str) -> bytes:
    """
    ---------------------
    METHOD: hash_password
    ---------------------
    Description:
        Takes in a string password and returns a
        hashed version of it
    Args:
        @password: password string
    """
    from bcrypt import hashpw, gensalt

    password, salt = bytes(password.encode()), gensalt()
    return hashpw(password, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    ----------------
    METHOD: is_valid
    ----------------
    Description:
        Validates whether a given password is
        actually valid
    Args:
        @hashed_password: hashed password
        @password: original password
    """
    from bcrypt import checkpw

    return checkpw(password.encode('UTF-8'), hashed_password)
