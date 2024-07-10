#!/usr/bin/env python3
""" Basic Auth Module """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Auth class """
    def __init__(self) -> None:
        super().__init__()