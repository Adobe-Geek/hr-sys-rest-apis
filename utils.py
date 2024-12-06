import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_with_smtp(subject, recipient, body):
    smtp_server = "smtp.mailgun.org"
    smtp_port = 587
    smtp_username = "postmaster@sandbox2f22328d2e8048e3addced2bad58ca95.mailgun.org"
    smtp_password = ***
    sender_email = smtp_username

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient, msg.as_string())
