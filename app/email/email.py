from flask_mail import Message
from flask import render_template, current_app
from app import mail
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from threading import Thread


def send_mail(subject, sender, recipients, txt_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = txt_body
    msg.html = html_body
    # extract application instance from proxy object when passing to thread
    Thread(target=send_mail_async, args=(current_app._get_current_object(), msg)).start()


def send_mail_async(app, msg):
    with app.app_context():
        mail.send(msg)


def send_activation_email(email):
    token = generate_token(email)
    send_mail(
        subject="My Python Library: Activate Your Account",
        sender=current_app.config['ADMIN'],
        recipients=[email],
        txt_body=render_template("email/activation_email.txt", token=token),
        html_body=render_template("email/activation_email.html", token=token)
    )


def send_password_reset_email(user):
    token = generate_token(user.email)
    send_mail(
        subject="My Python Library: Reset Your Password",
        sender=current_app.config['ADMIN'],
        recipients=[user.email],
        txt_body=render_template("email/password_reset_email.txt", token=token),
        html_body=render_template("email/password_reset_email.html", token=token)
    )


def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['PASSWORD_SALT'], max_age=expiration)
    except BadSignature:
        return False
    except SignatureExpired:
        return False

    return email
