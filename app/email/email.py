from flask_mail import Message
from flask import render_template
from app import mail
from app import app

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


def send_mail(subject, sender, recipients, txt_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = txt_body
    msg.html = html_body
    mail.send(msg)


def send_activation_email(email):
    token = generate_activation_token(email)
    send_mail(
        subject="My Little Python Library: Activate Your Account",
        sender=app.config['ADMIN'],
        recipients=[email],
        txt_body=render_template("email/activation_email.txt", token=token),
        html_body=render_template("email/activation_email.html", token=token)
    )


def generate_activation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['PASSWORD_SALT'])


def confirm_activation_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['PASSWORD_SALT'], max_age=expiration)
    except BadSignature:
        return False
    except SignatureExpired:
        return False

    return email
