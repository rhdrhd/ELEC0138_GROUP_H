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


def get_balance(conn, username):
    sql = "SELECT balance FROM users WHERE username = ?;"
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        if result is not None:
            balance = result[0]
            print(f"Balance for {username} is: ${balance:.2f}")
        else:
            print("No user found with the specified username.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    return balance


def update_balance(conn, amount_to_add, username):
    sql = """
    UPDATE users
    SET balance = balance + ?
    WHERE username = ? AND balance + ? >= 0;
    """
    cursor = conn.cursor()

    try:
        cursor.execute(sql, (amount_to_add, username, amount_to_add))
        if cursor.rowcount == 0:
            return False, Exception(
                f"No such user:{username} or their balance is not enough."
            )
        else:
            conn.commit()
            print("User balance updated successfully.")
            return True, None
    except sqlite3.Error as e:
        conn.rollback()
        print(f"An error occurred: {e}")
        return False, e
