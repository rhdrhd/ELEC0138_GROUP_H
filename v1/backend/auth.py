#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from constants import APP_SECRET_KEY, RESPONSE_STATUS

import jwt


def gen_jwt_token(payload: dict) -> str:
    # Generate the JWT token
    token = jwt.encode(payload, APP_SECRET_KEY, algorithm="HS256")
    # Since PyJWT v2.0.0, jwt.encode() returns a string
    return token


def validate_header(auth_header: str) -> tuple:
    """Return a jwt token from a request's authentication header."""
    err, token = None, ""
    if auth_header:
        # Split the header into 'Bearer' and the token part
        parts = auth_header.split(" ")
        if len(parts) == 1:
            err = (
                {
                    "status": RESPONSE_STATUS[1],
                    "msg": "Token not found. Authorization header must start with Bearer",
                },
                401,
            )
        elif parts[0].lower() != "bearer":
            err = (
                {
                    "status": RESPONSE_STATUS[1],
                    "msg": "Authorization header must start with Bearer",
                },
                401,
            )
        elif len(parts) > 2:
            err = (
                {
                    "status": RESPONSE_STATUS[1],
                    "msg": "Authorization header must be Bearer token",
                },
                401,
            )
        else:
            token = parts[1]
    else:
        err = (
            {
                "status": RESPONSE_STATUS[1],
                "msg": "Authorization header is missing",
            },
            401,
        )
    return err, token


def validate_and_decode_jwt(token: str, secret_key: str = APP_SECRET_KEY) -> tuple:
    """Validate and decode a JWT token using the provided secret key."""
    err, payload = None, {}
    try:
        # Decode the token
        # Note: Add verify=True to enforce verification
        payload = jwt.decode(
            token, secret_key, algorithms=["HS256"], options={"verify_signature": True}
        )
    except jwt.ExpiredSignatureError:
        err = (
            {
                "status": RESPONSE_STATUS[1],
                "msg": "The token has expired.",
            },
            401,
        )
    except jwt.InvalidTokenError:
        err = (
            {
                "status": RESPONSE_STATUS[1],
                "msg": "Invalid token.",
            },
            401,
        )
    except Exception as e:
        err = (
            {
                "status": RESPONSE_STATUS[1],
                "msg": f"An error occurred: {e}",
            },
            401,
        )
    return err, payload
