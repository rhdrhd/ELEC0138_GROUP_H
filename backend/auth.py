#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from constants import APP_SECRET_KEY

import jwt


def get_jwt_token(payload: dict) -> str:
    # Generate the JWT token
    token = jwt.encode(payload, APP_SECRET_KEY, algorithm="HS256")
    # Since PyJWT v2.0.0, jwt.encode() returns a string
    return token


def get_jwt_payload(token: str) -> dict:
    payload = jwt.decode(token, APP_SECRET_KEY, algorithms=["HS256"])
    return payload
