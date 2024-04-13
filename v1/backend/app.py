#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os

from auth import gen_jwt_token, validate_header, validate_and_decode_jwt
from constants import (
    APP_SECRET_KEY,
    API_PREFIX,
    USER_DATABASE_FILENAME,
    USER_UNSAFE_DATABASE_FILENAME,
    VENUE_DATABASE_FILENAME,
    DEFAULT_TOKEN_EXPIRATION_MINUTES,
    RESPONSE_STATUS,
)
from database import get_sqlite_cursor
from limiter import get_limiter
from werkzeug.security import check_password_hash
import sqlite3
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import jwt

import requests

CWD = os.getcwd()
USER_DATABASE_FILEPATH = os.path.join(CWD, USER_DATABASE_FILENAME)
USER_UNSAFE_DATABASE_FILEPATH = os.path.join(CWD, USER_UNSAFE_DATABASE_FILENAME)
VENUE_DATABASE_FILEPATH = os.path.join(CWD, VENUE_DATABASE_FILENAME)

# Website version: Safe or Unsafe
IS_SAFE = True if os.environ.get("MODE", "safe").lower() == "safe" else False
print(IS_SAFE)

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
origins = ["http://localhost:5173"]
CORS(app, supports_credentials=True, origins=origins)
limiter = get_limiter(is_safe=IS_SAFE, app=app)


@app.route(f"{API_PREFIX}/v1/venues", methods=["GET"])
@limiter.limit("5 per second")
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
@limiter.limit("5 per second")
def login():
    req = request.get_json()
    if not req:
        return jsonify({'status': 'failed', 'msg': 'Bad request: No JSON body found'}), 400

    username = req.get("username", "Unknown")
    password = req.get("password", "")
    recaptcha_response = req.get('g-recaptcha-response')

    if recaptcha_response:
        secret = "6Lczk7kpAAAAALmq7-J9ZIiEPuSz1Ko5CC-oKG03"
        payload = {'secret': secret, 'response': recaptcha_response}
        recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
        try:
            verify_response = requests.post(recaptcha_verify_url, data=payload)
            verify_result = verify_response.json()
            print("reCAPTCHA API Response:", verify_result)  # Log the full API response
            if not verify_result.get('success', False):
                return jsonify({'status': 'failed', 'msg': 'reCAPTCHA verification failed'}), 401
        except requests.RequestException as e:
            return jsonify({'status': 'failed', 'msg': 'Failed to verify reCAPTCHA'}), 503

    if IS_SAFE:
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
        cur = get_sqlite_cursor(USER_UNSAFE_DATABASE_FILEPATH)
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

            response = make_response(jsonify({"status": RESPONSE_STATUS[0], "msg": "User logged in successfully.", "data": {"user": {"username": username}, "token": token}}))
            response.set_cookie('auth_token', token, httponly=True, samesite='None', secure=True, path='/')
            return response
        else:
            response = {
                "status": RESPONSE_STATUS[1],
                "msg": "Login failed. Invalid username or password.",
            }
            return jsonify(response), 401


@app.route(f"{API_PREFIX}/v1/dashboard", methods=["POST"])
@limiter.limit("5 per second")
def dashboard():
    if IS_SAFE:
        # Get the Authorization header from the incoming request
        auth_header = request.headers.get("Authorization")
        err, token = validate_header(auth_header)
        if err:
            return jsonify(err)
    else:
        token = request.cookies.get('auth_token')
        print(token)
    err, payload = validate_and_decode_jwt(token)
    if err:
        return jsonify(err)

    # check username and password
    # USER_DATABASE_FILEPATH = os.path.join(CWD, USER_DATABASE_FILENAME)
    if IS_SAFE:
        cur = get_sqlite_cursor(USER_DATABASE_FILEPATH)
    else:
        cur = get_sqlite_cursor(USER_UNSAFE_DATABASE_FILEPATH)
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


@app.route('/api/v1/update-profile', methods=['POST'])
def update_profile():
    # get jwt token from cookie
    token = request.cookies.get('auth_token')
    if not token:
        return jsonify({"status": "error", "msg": "Unauthorized. No token provided."}), 401
    
    # validate and decode jwt token
    err, payload = validate_and_decode_jwt(token)
    if err:
        return jsonify(err), 401
    
    # check username and password
    if IS_SAFE:
        cur = get_sqlite_cursor(USER_DATABASE_FILEPATH)
    else:
        cur = get_sqlite_cursor(USER_UNSAFE_DATABASE_FILEPATH)
    cur.execute("SELECT * FROM users WHERE username = ?", (payload["username"],))
    user = cur.fetchone()
    if user and user["password"] != payload["password"]:
        print(user["password"])
        print(payload["password"])
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

    # update user profile in database
    new_email = request.form.get('email')
    cur.execute("UPDATE users SET email = ? WHERE username = ?",
                (new_email, payload["username"]))
    cur.connection.commit()

    return jsonify({
        'status': 'success',
        'msg': 'Profile updated successfully.',
        'data': {
            'username': payload["username"],
            'email': new_email
        }
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
