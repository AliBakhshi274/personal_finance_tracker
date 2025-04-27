import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

sender_email = os.getenv("SENDER_EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")
SMTP_PORT = 587

def send_email(receiver_email, subject, body):

    html = f"""\
    <html>
        <body>
            Hi, <br>
            {body}
        </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP('smtp.gmail.com', SMTP_PORT) as connection:
        connection.starttls()
        connection.login(sender_email, email_password)
        connection.sendmail(sender_email, receiver_email, msg.as_string())

    print("Email sent!")

























