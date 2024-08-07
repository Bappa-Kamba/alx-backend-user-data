#!/usr/bin/env python3
""" Authorization Module"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
            Method to hash password string

            Args:
                password: the password string to hash

            Returns:
                a byte string - a salted hash password of `password`
        """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
            Method to generate a UUID for a user

            Returns:
                the UUID string
        """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

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
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
            Method to validate a user login

            Args:
                email: the email of the user
                password: the password of the user

            Returns:
                True if the user is valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password
            )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
            Method to create a session for a user

            Args:
                email: the email of the user

            Returns:
                the session id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
            Method to get a user from a session id

            Args:
                session_id: the session id of the user

            Returns:
                User or None
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
            Method to destroy a session for a user

            Args:
                user_id: the id of the user
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except ValueError:
            raise ValueError('Invalid argument')
        except NoResultFound:
            raise NoResultFound('No user found')

    def get_reset_password_token(self, email: str) -> str:
        """
            Method to get a reset password token for a user

            Args:
                email: the email of the user

            Returns:
                token: the reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
        except NoResultFound:
            raise ValueError('No user found') from NoResultFound
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
            Method to update the password of a user

            Args:
                reset_token: the reset password token
                password: the new password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=hashed_password,
                reset_token=None
            )
        except NoResultFound:
            raise ValueError('No user found')
