#!/usr/bin/env python3
""" Flask Module """
from flask import jsonify, Flask, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
