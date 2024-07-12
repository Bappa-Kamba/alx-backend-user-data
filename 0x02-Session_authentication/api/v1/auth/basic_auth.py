#!/usr/bin/env python3
""" Basic Auth Module """
from api.v1.auth.auth import Auth
import base64
from typing import Tuple
from models.user import User


class BasicAuth(Auth):
    """ Basic Auth class """

    def __init__(self) -> None:
        super().__init__()

    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """ Extracts base64 authorization header """
        if not authorization_header or type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
    ) -> str:
        """ Decodes base64 authorization header """
        if not base64_authorization_header or \
                type(base64_authorization_header) != str:
            return None
        try:
            decoded_str = base64.b64decode(
                base64_authorization_header,
                validate=True
            )
        except Exception:
            return None

        return decoded_str.decode('UTF-8')

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        """
            Extracts user credentials from decoded base64 authorization header
        """
        if not decoded_base64_authorization_header or \
                type(decoded_base64_authorization_header) != str:
            return (None, None)

        colon_idx = decoded_base64_authorization_header.find(':')

        if colon_idx > 0:
            return tuple(decoded_base64_authorization_header.split(':'))
        else:
            return (None, None)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
    ) -> User:
        """ Creates user object from user credentials """
        u = User()
        if user_email is None or type(user_email) != str:
            return None

        if user_pwd is None or type(user_pwd) != str:
            return None
        curr_user = u.search({"email": user_email})
        if not curr_user or len(curr_user) == 0:
            return None
        user = curr_user[0]

        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> User:
        """
            Returns current user object
        """
        if request:
            auth_header = self.authorization_header(request)
            if not auth_header:
                return None
            base64_part = self.extract_base64_authorization_header(auth_header)
            if not base64_part:
                return None
            decoded_base64 = self.decode_base64_authorization_header(
                base64_part)
            if not decoded_base64:
                return None
            user_email, user_pwd = self.extract_user_credentials(
                decoded_base64)
            if not (user_email or user_pwd):
                return None
            user = self.user_object_from_credentials(user_email, user_pwd)
            if not user:
                return None
            return user
