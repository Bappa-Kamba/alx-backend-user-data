#!/usr/bin/env python3
""" Auth Module """
from flask import request
from typing import Type
from models.user import User

class Auth:
    """ Auth class """
    def require_auth(self, path: str, excluded_paths: list = []) -> bool:
        """ Require auth """
        return False
    
    def authorization_header(self, request=None) -> str:
        """ Authorization header """
        return None

    def current_user(self, request=None) -> Type['User']:
        """ Current user """
        return None
    

a = Auth()

print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.authorization_header())
print(a.current_user())
