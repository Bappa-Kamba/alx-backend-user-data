#!/usr/bin/env python3
""" Flask Module """
from flask import (
    jsonify,
    Flask,
    request,
    abort,
    redirect,
    url_for
)
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def index():
    """ index route """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"])
def users():
    """ users route """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({
            "email": f"{user.email}", "message": "user created"
        }), 200


@app.route('/profile')
def profile():
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": f"{user.email}"})


@app.route('/sessions', methods=["POST"])
def login():
    """ login route """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    resp = jsonify({"email": f"{email}", "message": "logged in"})
    resp.set_cookie('session_id', session_id)
    return resp


@app.route('/sessions', methods=["DELETE"])
def logout():
    """ logout route """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('index'))


@app.route('/reset_password', methods=["POST"])
def get_reset_password_token():
    """ get reset password token """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    else:
        return jsonify({
            "email": f"{email}", "reset_token": f"{token}"
        }), 200


@app.route('/reset_password', methods=["PUT"])
def update_password():
    """ update password route """
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    reset_token = request.form.get('reset_token')

    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)
    return jsonify({
        "email": f"{email}",
        "message": "Password updated"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
