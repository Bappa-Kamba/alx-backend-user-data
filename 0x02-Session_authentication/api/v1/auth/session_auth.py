#!/usr/bin/env python3
""" Session Auth Module """
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ Session Auth Class """

    user_id_by_session_id = {}

    def __init__(self) -> None:
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id """
        if not user_id and type(user_id) != str:
            return None
        sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id
