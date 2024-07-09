#!/usr/bin/env python3
""" Auth Module """
from flask import request
from typing import TypeVar


class Auth:
    """ Auth class """

    def require_auth(self, path: str, excluded_paths: list = []) -> bool:
        """ Require auth """
        return False

    def authorization_header(self, request=None) -> str:
        """ Authorization header """
        return None

    def current_user(self, request=None) -> TypeVar:
        """ Current user """
        return None
