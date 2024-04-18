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
VENUE_DATABASE_FILENAME = "venue.db"


# status for responses
RESPONSE_STATUS = [
    "SUCCESS",
    "FAILED",
]
