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
    ALLOWED_ORIGIN,
    RECAPTCHA_SECRET_KEY,
)
from database import (
    get_sqlite_cursor,
    insert_new_review,
    get_sqlite_conn,
    get_balance,
    update_balance,
)
from limiter import get_limiter
from send_email import send_email, clear_login_codes
from werkzeug.security import check_password_hash, generate_password_hash
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
origins = ALLOWED_ORIGIN
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


@app.route(f"{API_PREFIX}/v1/balance", methods=["POST"])
@limiter.limit("5 per second")
def update_user_balance():
    req = request.get_json()
    if not req:
        return (
            jsonify(
                {"status": RESPONSE_STATUS[1], "msg": "Bad request: No JSON body found"}
            ),
            400,
        )
    conn = get_sqlite_conn(USER_DATABASE_FILEPATH)
    amount = req.get("balance", 0)
    username = req.get("username", "")
    if amount == 0:
        return (
            jsonify(
                {
                    "status": RESPONSE_STATUS[1],
                    "msg": f"Bad request: Invalid amount: {amount}",
                }
            ),
            400,
        )
    is_success, err = update_balance(conn, amount, username)
    if not is_success:
        return (
            jsonify({"status": RESPONSE_STATUS[1], "msg": f"Bad request: {err}"}),
            400,
        )
    return jsonify({"status": RESPONSE_STATUS[0], "msg": "Balance updated!"}), 200


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
    review_date = req.get("review_date")
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


@app.route(f"{API_PREFIX}/v1/register", methods=["POST"])
@limiter.limit("5 per minute")  # Adjust rate limiting as appropriate
def register():
    req = request.get_json()
    if not req:
        return (
            jsonify(
                {"status": RESPONSE_STATUS[1], "msg": "Bad request: No JSON body found"}
            ),
            400,
        )

    username = req.get("username")
    password = req.get("password")
    email = req.get("email")

    if not username or not password or not email:
        return (
            jsonify({"status": RESPONSE_STATUS[1], "msg": "Missing required fields"}),
            400,
        )

    # Check if the username or email already exists
    conn = get_sqlite_conn(USER_DATABASE_FILEPATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = ? OR email = ?", (username, email)
    )
    if cur.fetchone():
        return (
            jsonify(
                {
                    "status": RESPONSE_STATUS[1],
                    "msg": "Username or email already exists",
                }
            ),
            409,
        )

    # Hash the password before storing it
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

    # Insert new user into the database
    try:
        cur.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hashed_password, email),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return (
            jsonify({"status": RESPONSE_STATUS[1], "msg": "Failed to register user"}),
            500,
        )

    # Send email notification
    email_subject = "Welcome to Our Platform!"
    email_body = f"Hello {username},\n\nThank you for registering at our site. We are glad to have you with us!"
    send_email(email, email_subject, email_body)

    return (
        jsonify({"status": RESPONSE_STATUS[0], "msg": "User registered successfully"}),
        201,
    )


@app.route(f"{API_PREFIX}/v1/login", methods=["POST"])
@limiter.limit("1 per second")
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

    if IS_SAFE:
        recaptcha_response = req.get("g-recaptcha-response")

        # verify reCAPTCHA response
        if recaptcha_response:
            secret = RECAPTCHA_SECRET_KEY
            payload = {"secret": secret, "response": recaptcha_response}
            recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
            try:
                verify_response = requests.post(recaptcha_verify_url, data=payload)
                verify_result = verify_response.json()
                print(
                    "reCAPTCHA API Response:", verify_result
                )  # Log the full API response
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
                        {
                            "status": RESPONSE_STATUS[1],
                            "msg": "Failed to verify reCAPTCHA",
                        }
                    ),
                    503,
                )

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
            payload = {"username": user["username"], "password": user["password"], "exp": exp}
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
            "data": {
                "user": {
                    "username": user["username"],
                    "email": user["email"],
                    "balance": user["balance"],
                }
            },
        }
    return jsonify(response), 200


@app.route("/update_user", methods=["POST"])
@limiter.limit("5 per minute")
def update_user():
    data = request.json
    username = data["username"]
    field = data["field"]
    new_value = data["new_value"]

    if field not in ["username", "email", "password"]:
        return jsonify({"msg": "Invalid field"}), 400

    conn = get_sqlite_conn(USER_DATABASE_FILEPATH)
    cur = conn.cursor()

    if field == "password":
        new_value = generate_password_hash(new_value, method="pbkdf2:sha256")

    cur.execute(
        f"UPDATE users SET {field} = ? WHERE username = ?", (new_value, username)
    )
    conn.commit()
    conn.close()

    return jsonify({"msg": "User updated successfully"}), 200


@app.route("/delete_user", methods=["POST"])
@limiter.limit("5 per minute")
def delete_user():
    username = request.json.get("username")
    if not username:
        return jsonify({"msg": "Username is required"}), 400

    conn = get_sqlite_conn(USER_DATABASE_FILEPATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()

    return jsonify({"msg": "User deleted successfully"}), 200


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
    username = req.get("username")  # Expecting a username to fetch associated email
    if not username:
        return jsonify({"status": "failed", "msg": "Username is required"}), 400

    # Fetch user's email from the database
    cur = get_sqlite_cursor(USER_DATABASE_FILEPATH)
    cur.execute("SELECT email FROM users WHERE username = ?", (username,))
    user_info = cur.fetchone()
    if not user_info or not user_info["email"]:
        return (
            jsonify({"status": "failed", "msg": "No such user or email missing"}),
            404,
        )

    email = user_info["email"]

    # Generate a 6-digit code for login
    code = random.randint(100000, 999999)
    send_email(email, "Your Login Code", f"Your Login Code is: {code}")

    # Store code in the database with expiration time
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

    code = req.get("code")
    if not code:
        return jsonify({"status": "failed", "msg": "Code is required"}), 400

    # Verify login code
    cur = get_sqlite_cursor(USER_DATABASE_FILEPATH)
    cur.execute(
        "SELECT * FROM login_codes WHERE code = ? AND expiration > datetime('now')",
        (code,),
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
