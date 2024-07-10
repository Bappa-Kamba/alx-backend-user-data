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
