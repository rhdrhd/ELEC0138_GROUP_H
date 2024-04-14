import sqlite3
from werkzeug.security import generate_password_hash

# Path to where you want to create the SQLite DB file
database_path = "user.db"

# Connect to the SQLite database (this will create the file if it doesn't exist)
conn = sqlite3.connect(database_path)

# Create the 'users' table
conn.execute(
    """CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                );"""
)

# Create the 'login_codes' table
conn.execute('''
CREATE TABLE IF NOT EXISTS login_codes (
    email TEXT,
    code TEXT,
    expiration DATETIME
);
''')

# Insert a sample user (replace 'your_username' and 'your_password' with your desired values)
username = "elec0138"
password = generate_password_hash("8964", method='pbkdf2:sha256')  # Hash the password
email = "elec0138h@gmail.com"

conn.execute(
    "INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email)
)

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"Database and sample user created at {database_path}")
