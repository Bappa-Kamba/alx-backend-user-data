#!/usr/bin/env python3
""" Session Auth Module """
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session Auth Class """

    def __init__(self) -> None:
        super().__init__()
