#!/usr/bin/env python3
""" Password Module """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Hash a password using the SHA-256 algorithm. """
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )

    return hashed_password
