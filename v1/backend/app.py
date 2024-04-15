#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import random

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
from database import get_sqlite_cursor, insert_new_review, get_sqlite_conn
from limiter import get_limiter
from send_email import send_email, clear_login_codes
from werkzeug.security import check_password_hash
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

import requests

CWD = os.getcwd()
USER_DATABASE_FILEPATH = os.path.join(CWD, USER_DATABASE_FILENAME)
USER_UNSAFE_DATABASE_FILEPATH = os.path.join(CWD, USER_UNSAFE_DATABASE_FILENAME)
VENUE_DATABASE_FILEPATH = os.path.join(CWD, VENUE_DATABASE_FILENAME)

# Website version: Safe or Unsafe
IS_SAFE = True if os.environ.get("MODE", "safe").lower() == "safe" else False

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


@app.route(f"{API_PREFIX}/v1/review", methods=["POST"])
@limiter.limit("5 per second")
def add_review():
    req = request.get_json()
    if not req:
        return (
            jsonify(
                {"status": RESPONSE_STATUS[1], "msg": "Bad request: No JSON body found"}
            ),
            400,
        )
    venue_id = req.get("venue_id", -1)
    review_text = req.get("review_text", "")
    date_today = datetime.datetime.today().strftime("%Y-%m-%d")
    review_date = req.get("review_date", date_today)
    rating = req.get("rating", 0)
    if venue_id == -1:
        return (
            jsonify({"status": RESPONSE_STATUS[1], "msg": f"venue_id is not set."}),
            401,
        )
    conn = get_sqlite_conn(VENUE_DATABASE_FILEPATH)
    insert_new_review(conn, venue_id, review_text, rating, review_date)
    return jsonify({"status": RESPONSE_STATUS[0], "msg": "A new review inserted!"}), 200


@app.route(f"{API_PREFIX}/v1/details", methods=["POST"])
@limiter.limit("5 per second")
def get_details():
    req = request.get_json()
    if not req:
        return (
            jsonify(
                {"status": RESPONSE_STATUS[1], "msg": "Bad request: No JSON body found"}
            ),
            400,
        )

    venue_id = req.get("id", -1)
    if venue_id == -1:
        return (
            jsonify({"status": RESPONSE_STATUS[1], "msg": f"id is not set."}),
            401,
        )
    cur = get_sqlite_cursor(VENUE_DATABASE_FILEPATH)
    cur.execute("SELECT * FROM venue WHERE id = ?", venue_id)
    row = cur.fetchone()
    venue = dict(row)
    cur.execute("SELECT * FROM reviews WHERE venue_id = ?", venue_id)
    rows = [dict(row) for row in cur.fetchall()]
    venue["reviews"] = rows
    # Convert the venues to a list of dictionaries to make them JSON serializable
    return jsonify({"status": RESPONSE_STATUS[0], "data": venue}), 200


@app.route(f"{API_PREFIX}/v1/login", methods=["POST"])
@limiter.limit("5 per second")
def login():
    req = request.get_json()
    if not req:
        return (
            jsonify(
                {"status": RESPONSE_STATUS[1], "msg": "Bad request: No JSON body found"}
            ),
            400,
        )

    username = req.get("username", "Unknown")
    password = req.get("password", "")
    recaptcha_response = req.get("g-recaptcha-response")

    # verify reCAPTCHA response
    if recaptcha_response:
        secret = "6Lczk7kpAAAAALmq7-J9ZIiEPuSz1Ko5CC-oKG03"
        payload = {"secret": secret, "response": recaptcha_response}
        recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
        try:
            verify_response = requests.post(recaptcha_verify_url, data=payload)
            verify_result = verify_response.json()
            print("reCAPTCHA API Response:", verify_result)  # Log the full API response
            if not verify_result.get("success", False):
                return (
                    jsonify(
                        {
                            "status": RESPONSE_STATUS[1],
                            "msg": "reCAPTCHA verification failed",
                        }
                    ),
                    401,
                )
        except requests.RequestException as e:
            return (
                jsonify(
                    {"status": RESPONSE_STATUS[1], "msg": "Failed to verify reCAPTCHA"}
                ),
                503,
            )

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
            email = user["email"]
            response = make_response(
                jsonify(
                    {
                        "status": RESPONSE_STATUS[0],
                        "msg": "User logged in successfully.",
                        "data": {
                            "user": {"username": username},
                            "token": token,
                            "email": email,
                        },
                    }
                )
            )
            return response, 200
        else:
            response = {
                "status": RESPONSE_STATUS[1],
                "msg": "Login failed. Invalid username or password.",
            }
            return jsonify(response), 401
    else:
        cur = get_sqlite_cursor(USER_UNSAFE_DATABASE_FILEPATH)
        cur.execute(
            f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        )
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

            response = make_response(
                jsonify(
                    {
                        "status": RESPONSE_STATUS[0],
                        "msg": "User logged in successfully.",
                        "data": {"user": {"username": username}, "token": token},
                    }
                )
            )
            response.set_cookie(
                "auth_token",
                token,
                httponly=True,
                samesite="None",
                secure=True,
                path="/",
            )
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
        token = request.cookies.get("auth_token")
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


@app.route("/api/v1/update-profile", methods=["POST"])
def update_profile():
    # get jwt token from cookie
    token = request.cookies.get("auth_token")
    if not token:
        return (
            jsonify(
                {
                    "status": RESPONSE_STATUS[1],
                    "msg": "Unauthorized. No token provided.",
                }
            ),
            401,
        )

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
    new_email = request.form.get("email")
    cur.execute(
        "UPDATE users SET email = ? WHERE username = ?",
        (new_email, payload["username"]),
    )
    cur.connection.commit()

    return (
        jsonify(
            {
                "status": RESPONSE_STATUS[0],
                "msg": "Profile updated successfully.",
                "data": {"username": payload["username"], "email": new_email},
            }
        ),
        200,
    )


# send login code to email
@app.route(f"{API_PREFIX}/v1/send-login-code", methods=["POST"])
@limiter.limit("2 per minute", key_func=lambda: request.remote_addr)
def send_login_code():
    req = request.get_json()
    email = req.get("email")
    if not email:
        return jsonify({"status": "failed", "msg": "Email is required"}), 400

    # Generate a 6-digit code for login
    code = random.randint(100000, 999999)
    send_email(email, "Your Login Code", f"Your Login Code is: {code}")

    # Store code in the database with expiration time
    cur = get_sqlite_cursor(USER_DATABASE_FILEPATH)
    cur.execute(
        "INSERT INTO login_codes (email, code, expiration) VALUES (?, ?, datetime('now', '+5 minutes'))",
        (email, code),
    )
    cur.connection.commit()

    return jsonify({"status": "success", "msg": "Login code sent successfully"}), 200


# verify email and login code
@app.route(f"{API_PREFIX}/v1/verify-login-code", methods=["POST"])
@limiter.limit("5 per second")
def verify_login_code():
    req = request.get_json()
    if not req:
        return (
            jsonify({"status": "failed", "msg": "Bad request: No JSON body found"}),
            400,
        )

    email = req.get("email")
    code = req.get("code")

    if not email or not code:
        return jsonify({"status": "failed", "msg": "Email and code are required"}), 400

    # verify login code
    cur = get_sqlite_cursor(USER_DATABASE_FILEPATH)
    cur.execute(
        "SELECT * FROM login_codes WHERE email = ? AND code = ? AND expiration > datetime('now')",
        (email, code),
    )
    code_valid = cur.fetchone()

    if not code_valid:
        return (
            jsonify({"status": "failed", "msg": "Invalid or expired login code"}),
            401,
        )

    return (
        jsonify({"status": "success", "msg": "Login code verified successfully"}),
        200,
    )


if __name__ == "__main__":
    clear_login_codes()
    app.run(host="0.0.0.0", debug=True)
