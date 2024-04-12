#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


# Setup limiter based on configuration
class DummyLimiter:
    def limit(self, *args, **kwargs):
        def decorator(f):
            return f

        return decorator


def get_limiter(is_safe: bool, app):
    if is_safe:
        limiter = Limiter(
            app=app, key_func=get_remote_address, default_limits=["1 per second"]
        )
    else:
        limiter = DummyLimiter()
    return limiter
