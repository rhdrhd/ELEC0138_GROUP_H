import smtplib
import sqlite3
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from constants import (
    USER_DATABASE_FILENAME,
    USER_UNSAFE_DATABASE_FILENAME,
)
CWD = os.getcwd()
USER_DATABASE_FILEPATH = os.path.join(CWD, USER_DATABASE_FILENAME)
USER_UNSAFE_DATABASE_FILEPATH = os.path.join(CWD, USER_UNSAFE_DATABASE_FILENAME)


def send_email(receiver_email, subject, body):
    sender_email = "elec0138h@gmail.com"
    password = "klgr zefv vrzx zojz"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

def clear_login_codes():
    databases = [USER_DATABASE_FILEPATH, USER_UNSAFE_DATABASE_FILEPATH]
    for db_path in databases:
        conn = sqlite3.connect(db_path)
        with conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM login_codes")
            conn.commit()
