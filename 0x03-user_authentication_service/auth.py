#!/usr/bin/env python3
""" Authorization Module"""
import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
            Method to hash password string

            Args:
                password: the password string to hash

            Returns:
                a byte string - a salted hash password of `password`
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """
            Method to register a user in the database

            Args:
                email: the email of the user
                password: the password of the user

            Returns:
                the user
        """
        if not self._db.find_user_by(email=email):
            hashed_password = self._hash_password(password)
            return self._db.add_user(email, hashed_password)
        raise ValueError(f"User {email} exists")


email = 'me@me.com'
password = 'mySecuredPwd'

auth = Auth()

try:
    user = auth.register_user(email, password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))

try:
    user = auth.register_user(email, password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))
