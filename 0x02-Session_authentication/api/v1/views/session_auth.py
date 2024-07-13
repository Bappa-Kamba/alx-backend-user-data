#!/usr/bin/env python3
""" Session View Module """
from api.v1.views import app_views
from flask import (
    jsonify,
    request,
    abort,
    make_response
)
from os import getenv
from models.user import User

SESSION_NAME = getenv('SESSION_NAME')


@app_views.route(
    '/auth_session/login', methods=["POST"],
    strict_slashes=False
)
def login():
    """
        POST /auth_session/login 

        JSON body:
            - email
            - password

        Return:
            - User object JSON represented
            - 400 if can't create the new User

    """
    user_email = request.form.get('email')
    password = request.form.get('password')
    u = User()

    if not user_email:
        return jsonify({
            "error": "email missing"
        }), 400
    if not password:
        return jsonify({
            "error": "password missing"
        }), 400
    user_results = u.search({'email': user_email})
    if not user_results or len(user_results) == 0:
        return jsonify({
            "error": "no user found for this email"
        }), 404
    user = user_results[0]
    if not user.is_valid_password(password):
        return jsonify({
            "error": "wrong password"
        }), 401
    from api.v1.app import auth
    user_sess_id = auth.create_session(user.id)

    response = make_response(jsonify(user.to_json()))
    response.set_cookie(SESSION_NAME, user_sess_id)

    return response


@app_views.route(
    '/auth_session/logout', methods=['DELETE'],
    strict_slashes=False
)
def logout():
    """
    DELETE /api/v1/auth_session/logout

    Return:
        - Empty JSON dictionary with status code 200
            if session is successfully destroyed
        - 404 error if session destruction fails
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
