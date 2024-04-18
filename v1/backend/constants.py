#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Flask app
APP_SECRET_KEY = "0138"
# api
API_PREFIX = "/api"

# jwt token expiration
DEFAULT_TOKEN_EXPIRATION_MINUTES = 5

# Database for users
# Assuming you have a SQLite DB named 'users.db' with a table 'users' (id, username, password)
USER_DATABASE_FILENAME = "user.db"
USER_UNSAFE_DATABASE_FILENAME = "user_unsafe.db"
VENUE_DATABASE_FILENAME = "venue.db"

# Origin for CORS
ALLOWED_ORIGIN = ["http://127.0.0.1:5173", "http://localhost:5173"]

# ReCaptcha secret key
RECAPTCHA_SECRET_KEY = "6Lczk7kpAAAAALmq7-J9ZIiEPuSz1Ko5CC-oKG03"

# status for responses
RESPONSE_STATUS = [
    "SUCCESS",
    "FAILED",
]
