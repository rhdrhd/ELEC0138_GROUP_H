#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3


def get_sqlite_conn(database_filepath: str) -> sqlite3.Connection:
    """Return a sqlite connection from a database path."""
    conn = sqlite3.connect(database_filepath)
    return conn


def get_sqlite_cursor(database_filepath: str) -> sqlite3.Cursor:
    """Return a sqlite cursor from a database path."""
    conn = get_sqlite_conn(database_filepath)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return cur
