import smtplib
from email.message import EmailMessage
from flask import current_app

def send_email(to_email: str, subject: str, body: str) -> None:
    cfg = current_app.config

    host = cfg.get("MAIL_HOST")
    port = cfg.get("MAIL_PORT")
    username = cfg.get("MAIL_USERNAME")
    password = cfg.get("MAIL_PASSWORD")
    sender = cfg.get("MAIL_DEFAULT_SENDER")
    use_tls = cfg.get("MAIL_USE_TLS", True)

    if not all([host, port, username, password, sender]):
        raise RuntimeError("MAIL config missing (provjeri .env i config.py)")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(host, port) as server:
        server.ehlo()
        if use_tls:
            server.starttls()
            server.ehlo()
        server.login(username, password)
        server.send_message(msg)
