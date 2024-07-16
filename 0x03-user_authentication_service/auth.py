#!/usr/bin/env python3
""" Authorization Module"""
import bcrypt
from typing import ByteString


def _hash_password(password: str) -> ByteString:
    """
        Method to hash password string

        Args:
            password: the password string to hash

        Returns:
            a byte string - a salted hash password of `password`
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


print(_hash_password("Hello Holberton"))
