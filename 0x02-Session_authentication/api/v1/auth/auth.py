#!/usr/bin/env python3
""" Auth Module """
from flask import request
from typing import TypeVar
from os import getenv


class Auth:
    """ Auth class """

    def require_auth(self, path: str, excluded_paths: list = []) -> bool:
        """ Require auth """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure path ends with a slash for comparison
        if not path.endswith('/'):
            path += '/'
        # Check if the path is in the list of excluded paths
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar:
        """ Current user """
        return None

    def session_cookie(self, request=None):
        """ Session cookie """
        if not request:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
