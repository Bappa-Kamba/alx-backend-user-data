#!/usr/bin/env python3
""" Session Auth Module """
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ Session Auth Class """

    user_id_by_session_id = {}

    def __init__(self) -> None:
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id """
        if not user_id or type(user_id) != str:
            return None
        sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID """
        if not session_id or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Returns a Request user ID """
        session_name = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_name)
        if not user_id:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
            Funtion that destroy the session of the user
            Args:
                request (request): request object
            Returns:
                bool: True if the session was successfully destroyed,
                    False otherwise
        """
        if not request:
            return False
        sess_id = self.session_cookie(request)
        if not sess_id:
            return False
        user_id = self.user_id_for_session_id(sess_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[sess_id]
        return True
