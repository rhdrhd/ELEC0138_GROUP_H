#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

from auth import get_jwt_payload, get_jwt_token
from constants import (
    APP_SECRET_KEY,
    DATABASE_FILENAME,
    DEFAULT_TOKEN_EXPIRATION_MINUTES,
    RESPONSE_STATUS,
)

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import check_password_hash
import sqlite3
from jwt.exceptions import ExpiredSignatureError

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
CORS(app)


@app.route("/login", methods=["POST"])
def login():
    req = request.get_json()
    username = req.get("username", "Unknown")
    password = req.get("password", "")
    conn = sqlite3.connect(DATABASE_FILENAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    if user and check_password_hash(user["password"], password):
        # Payload data that you want to encode within the JWT.
        # Include claims like the user ID, expiration time, etc.
        exp = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=DEFAULT_TOKEN_EXPIRATION_MINUTES
        )
        payload = {
            "username": username,
            "exp": exp,
        }
        token = get_jwt_token(payload)

        response = {
            "status": RESPONSE_STATUS[0],
            "msg": "User logged in successfully.",
            "data": {
                "user": {
                    "username": username,
                },
                "token": token,
            },
        }
        return jsonify(response), 200
    else:
        response = {
            "status": RESPONSE_STATUS[1],
            "msg": "Login failed. Invalid username or password.",
        }
        return jsonify(response), 401


@app.route("/dashboard", methods=["POST"])
def dashboard():
    req = request.get_json()
    token = req.get("token", "")
    if token == "":
        response = {
            "status": RESPONSE_STATUS[1],
            "msg": "No token provided. Please provide a valid token to access this resource.",
        }
        return jsonify(response), 401
    else:
        try:
            payload = get_jwt_payload(token)
        except ExpiredSignatureError:
            print("Token has expired.")
            response = {
                "status": RESPONSE_STATUS[1],
                "msg": "Your session has expired. Please log in again.",
            }
            return jsonify(response), 401
        except Exception:
            response = {
                "status": RESPONSE_STATUS[1],
                "msg": "token invalid. Please provide a valid token to access this resource.",
            }
            return jsonify(response), 401
        else:
            username = payload["username"]
            conn = sqlite3.connect(DATABASE_FILENAME)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cur.fetchone()
            username = user["username"]

            response = {
                "status": RESPONSE_STATUS[0],
                "msg": "Dashboard",
                "data": {
                    "user": {
                        "username": username,
                    },
                },
            }
        return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)