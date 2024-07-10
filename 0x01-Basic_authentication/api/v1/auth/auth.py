#!/usr/bin/env python3
""" Auth Module """
from flask import request
from typing import TypeVar


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


a = Auth()

print(a.require_auth(None, None))
print(a.require_auth(None, []))
print(a.require_auth("/api/v1/status/", []))
print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/users", ["/api/v1/status/", "/api/v1/stats"]))
