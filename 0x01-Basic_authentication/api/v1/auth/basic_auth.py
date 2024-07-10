#!/usr/bin/env python3
""" Basic Auth Module """
from api.v1.auth.auth import Auth


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
    

a = BasicAuth()

print(a.extract_base64_authorization_header(None))
print(a.extract_base64_authorization_header(89))
print(a.extract_base64_authorization_header("Holberton School"))
print(a.extract_base64_authorization_header("Basic Holberton"))
print(a.extract_base64_authorization_header("Basic SG9sYmVydG9u"))
print(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA=="))
print(a.extract_base64_authorization_header("Basic1234"))
        