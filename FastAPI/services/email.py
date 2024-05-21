# services/email.py
import os
import secrets
import smtplib
import string
from email.mime.text import MIMEText


def send_recovery_email(to_email, recovery_code):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    msg = MIMEText(f"Tu código de recuperación es: {recovery_code}")
    msg["Subject"] = "Recuperación de contraseña"
    msg["From"] = smtp_username
    msg["To"] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()  # Para conexiones seguras
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(msg)

def generate_recovery_code():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))