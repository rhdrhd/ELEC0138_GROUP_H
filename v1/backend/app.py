#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os

from auth import gen_jwt_token, validate_header, validate_and_decode_jwt
from constants import (
    APP_SECRET_KEY,
    API_PREFIX,
    USER_DATABASE_FILENAME,
    VENUE_DATABASE_FILENAME,
    DEFAULT_TOKEN_EXPIRATION_MINUTES,
    RESPONSE_STATUS,
)
from database import get_sqlite_cursor

from flask import Flask, request, jsonify
from flask_cors import CORS

CWD = os.getcwd()
USER_DATABASE_FILEPATH = os.path.join(CWD, USER_DATABASE_FILENAME)
VENUE_DATABASE_FILEPATH = os.path.join(CWD, VENUE_DATABASE_FILENAME)

# Website version: Safe or Unsafe
IS_SAFE = True if os.environ.get("MODE", "safe").lower() == "safe" else False

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
CORS(app)


@app.route(f"{API_PREFIX}/v1/venues", methods=["GET"])
def get_venues():
    cur = get_sqlite_cursor(VENUE_DATABASE_FILEPATH)
    cur.execute("SELECT * FROM venue")
    venues = cur.fetchall()
    # Convert the venues to a list of dictionaries to make them JSON serializable
    venues_list = [dict(venue) for venue in venues]
    return jsonify({"status": RESPONSE_STATUS[0], "data": venues_list}), 200


# TODO(xss, optional): comments
# @app.route(f"{API_PREFIX}/v1/comments", methods=["POST"])


@app.route(f"{API_PREFIX}/v1/login", methods=["POST"])
def login():
    req = request.get_json()
    username = req.get("username", "Unknown")
    password = req.get("password", "")

    if IS_SAFE:
        from werkzeug.security import check_password_hash

        cur = get_sqlite_cursor(USER_DATABASE_FILEPATH)
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user["password"], password):
            # Payload data that you want to encode within the JWT.
            # Include claims like the user ID, expiration time, etc.
            exp = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=DEFAULT_TOKEN_EXPIRATION_MINUTES
            )
            payload = {"username": username, "password": user["password"], "exp": exp}
            token = gen_jwt_token(payload)

            response = {
                "status": RESPONSE_STATUS[0],
                "msg": "User logged in successfully.",
                "data": {"user": {"username": username}, "token": token},
            }
            return jsonify(response), 200
        else:
            response = {
                "status": RESPONSE_STATUS[1],
                "msg": "Login failed. Invalid username or password.",
            }
            return jsonify(response), 401
    else:
        # weak version of sql injection
        cur = get_sqlite_cursor(USER_DATABASE_FILEPATH)
        cur.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
        user = cur.fetchone()
        # raise NotImplementedError
        if user:
            # Payload data that you want to encode within the JWT.
            # Include claims like the user ID, expiration time, etc.
            exp = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=DEFAULT_TOKEN_EXPIRATION_MINUTES
            )
            payload = {"username": username, "password": user["password"], "exp": exp}
            token = gen_jwt_token(payload)

            response = {
                "status": RESPONSE_STATUS[0],
                "msg": "User logged in successfully.",
                "data": {"user": {"username": username}, "token": token},
            }
            return jsonify(response), 200
        else:
            response = {
                "status": RESPONSE_STATUS[1],
                "msg": "Login failed. Invalid username or password.",
            }
            return jsonify(response), 401


@app.route(f"{API_PREFIX}/v1/dashboard", methods=["POST"])
def dashboard():
    # Get the Authorization header from the incoming request
    auth_header = request.headers.get("Authorization")
    err, token = validate_header(auth_header)
    if err:
        return jsonify(err)
    err, payload = validate_and_decode_jwt(token)
    if err:
        return jsonify(err)

    # check username and password
    # USER_DATABASE_FILEPATH = os.path.join(CWD, USER_DATABASE_FILENAME)
    cur = get_sqlite_cursor(USER_DATABASE_FILEPATH)
    cur.execute("SELECT * FROM users WHERE username = ?", (payload["username"],))
    user = cur.fetchone()
    if user and user["password"] != payload["password"]:
        response = {
            "status": RESPONSE_STATUS[1],
            "msg": f"Invalid username or password. Please login again.",
        }
        return jsonify(response), 401
    else:
        response = {
            "status": RESPONSE_STATUS[0],
            "msg": "Dashboard",
            "data": {"user": {"username": payload["username"]}},
        }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)
