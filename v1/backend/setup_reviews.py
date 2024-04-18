import sqlite3

from .database import insert_new_review

# Path to where you want to create the SQLite DB file
database_path = "venue.db"

# Connect to the SQLite database (this will create the file if it doesn't exist)
conn = sqlite3.connect(database_path)


# Create the 'users' table
def create_reviews_table():
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venue_id INTEGER,
            review_text TEXT NOT NULL,
            rating INTEGER NOT NULL,
            review_date DATE NOT NULL,
            FOREIGN KEY (venue_id) REFERENCES venue(id)
        );
    """
    )
    conn.commit()


create_reviews_table()
conn.execute("PRAGMA foreign_keys = ON")

# Example usage
insert_new_review(conn, 1, "Great!", 5, "2021-08-15")

# Commit changes and close the connection
conn.commit()
conn.close()
