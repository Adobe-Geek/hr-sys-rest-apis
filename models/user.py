from db import db
from flask import request, url_for
from passlib.hash import pbkdf2_sha256
from requests import Response

# from libs.mailgun import Mailgun
from utils import send_email_with_smtp


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_password(hashed_password, plain_password):
        return pbkdf2_sha256.verify(plain_password, hashed_password)

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, user_id: int) -> "UserModel":
        return cls.query.get(user_id)

    # def send_confirmation_email(self) -> Response:
    #     link = request.url_root[:-1] + url_for("users.UserConfirm", user_id=self.id)
    #     subject = "Registration confirmation"
    #     text = f"Please click link to confirm your registration: {link}"
    #     html = f'<html>Please click link tco confirm your registration: <a href="{link}">{link}</a></html>'
    #     return Mailgun.send_email([self.email], subject, text, html)

    def send_confirmation_email(self):
        confirmation_link = url_for(
            "users.UserConfirm", user_id=self.id, _external=True
        )
        subject = "Confirm Your Registration"
        html_body = f"""
        <html>
            <body>
                <h1>Welcome to Our App!</h1>
                <p>Click the link below to confirm your registration:</p>
                <a href="{confirmation_link}">Confirm Registration</a>
            </body>
        </html>
        """
        send_email_with_smtp(subject=subject, recipient=self.email, body=html_body)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
