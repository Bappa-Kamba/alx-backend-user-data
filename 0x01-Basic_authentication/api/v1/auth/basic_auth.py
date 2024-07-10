#!/usr/bin/env python3
""" Basic Auth Module """
from api.v1.auth.auth import Auth
import base64


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


a = BasicAuth()

print(a.decode_base64_authorization_header(None))
print(a.decode_base64_authorization_header(89))
print(a.decode_base64_authorization_header("Holberton School"))
print(a.decode_base64_authorization_header("SG9sYmVydG9u"))
print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))
print(a.decode_base64_authorization_header(
    a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA==")))
