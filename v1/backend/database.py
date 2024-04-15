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


def insert_new_review(conn, venue_id, review_text, rating, review_date):
    try:
        conn.execute(
            """
            INSERT INTO reviews (venue_id, review_text, rating, review_date)
            VALUES (?, ?, ?, ?)
        """,
            (venue_id, review_text, rating, review_date),
        )
        conn.commit()
        print("Review added successfully!")
    except sqlite3.IntegrityError as e:
        print("Failed to add review:", e)
