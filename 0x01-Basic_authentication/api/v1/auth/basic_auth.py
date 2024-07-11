#!/usr/bin/env python3
""" Basic Auth Module """
import uuid
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
        if user_email is None or type(user_email) != str:
            return None

        if user_pwd is None or type(user_pwd) != str:
            return None
        curr_user = User.search({"email": user_email})
        print(curr_user)
        if not curr_user or len(curr_user) == 0:
            return None
        valid_password = curr_user[0].is_valid_password(user_pwd)

        if not valid_password:
            return None
        return curr_user[0]


user_email = str(uuid.uuid4())
user_clear_pwd = str(uuid.uuid4())
user = User()
user.email = user_email
user.first_name = "Bob"
user.last_name = "Dylan"
user.password = user_clear_pwd
print("New user: {}".format(user.display_name()))
user.save()
# ba = BasicAuth()
# res = ba.user_object_from_credentials("u1@gmail.com", "pwd")
# if res is not None:
#     print("user_object_from_credentials must return None if 'user_email' is not linked to any user")
a = BasicAuth()


u = a.user_object_from_credentials("u1@gmail.com", "pwd")
print(u.display_name() if u is not None else "None")


u = a.user_object_from_credentials(user_email, user_clear_pwd)
print(u.display_name() if u is not None else "None")
