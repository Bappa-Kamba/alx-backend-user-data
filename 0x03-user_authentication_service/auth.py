#!/usr/bin/env python3
""" Authorization Module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound



class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str):
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
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self.register_user(email, hashed_password)
            return new_user

