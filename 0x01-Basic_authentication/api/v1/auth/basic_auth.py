#!/usr/bin/env python3
""" Basic Auth Module """
from api.v1.auth.auth import Auth
import base64
from typing import Tuple


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
        """ Extracts user credentials from decoded base64 authorization header """
        if not decoded_base64_authorization_header or \
            type(decoded_base64_authorization_header) != str:
            return (None, None)
        
        colon_idx = decoded_base64_authorization_header.find(':')
        
        if colon_idx > 0:
            return tuple(decoded_base64_authorization_header.split(':'))
        else:
            return (None, None)
        

a = BasicAuth()

print(a.extract_user_credentials(None))
print(a.extract_user_credentials(89))
print(a.extract_user_credentials("Holberton School"))
print(a.extract_user_credentials("Holberton:School"))
print(a.extract_user_credentials("bob@gmail.com:toto1234"))
