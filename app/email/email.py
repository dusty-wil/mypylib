from flask_mail import Message
from flask import render_template, current_app
from app import mail
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
        sender=current_app.config['ADMIN'],
        recipients=[email],
        txt_body=render_template("email/activation_email.txt", token=token),
        html_body=render_template("email/activation_email.html", token=token)
    )


def generate_activation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['PASSWORD_SALT'])


def confirm_activation_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['PASSWORD_SALT'], max_age=expiration)
    except BadSignature:
        return False
    except SignatureExpired:
        return False

    return email
