#!/usr/bin/env python3
""" Authorization Module"""
import bcrypt


def _hash_password(password: str):
    """
        Method to hash password string

        Args:
            password: the password string to hash

        Returns:
            a byte string - a salted hash password of `password`
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
