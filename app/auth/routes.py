from app.auth import bp
from app import db

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app.models.User import User
from app.auth.forms.LoginForm import LoginForm
from app.auth.forms.RegistrationForm import RegistrationForm
from app.auth.forms.RequestPasswordResetForm import RequestPasswordResetForm
from app.auth.forms.ResendActivationForm import ResendActivationForm

from app.email.email import send_activation_email, send_password_reset_email


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("my_library.summary"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.", category="error")
            return redirect(url_for("auth.login"))

        if user.verified_date is None:
            send_activation_email(form.email.data)
            flash("Please activate your account to log in. " +
                  "An activation link has been re-sent to {}".format(form.email.data), category="info")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember.data)

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("my_library.summary")

        flash("Logged in as {}".format(user.email), category="info")
        return redirect(next_page)

    return render_template(
        "auth/login.html",
        title="Log In",
        form=form
    )


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("my_library.index"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("my_library.summary"))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        send_activation_email(form.email.data)

        flash("Check your inbox, we've sent an activation link to {}. ".format(form.email.data) +
              "Please follow the instructions in the email in order to log in.", category="info")

        return redirect(url_for("my_library.index"))

    return render_template(
        "auth/register.html",
        title="Register",
        form=form
    )


@bp.route("/forgot", methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for("my_library.summary"))

    form = RequestPasswordResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for the next steps to reset your password!", category="info")
        return redirect(url_for("auth.login"))

    return render_template(
        "auth/request_password_reset.html",
        title="Forgot Your Password?",
        form=form
    )


@bp.route("/activate/resend", methods=['GET', 'POST'])
def resend_activate_email():
    if current_user.is_authenticated:
        return redirect(url_for("my_library.summary"))

    form = ResendActivationForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verified_date is not None:
            flash("User is already activated. You can log in!", category="info")
            return redirect(url_for("auth.login"))

        flash("An activation link has been re-sent to {}".format(form.email.data), category="info")

        if user is None:
            return redirect(url_for("auth.login"))

        send_activation_email(form.email.data)
        return redirect(url_for("auth.login"))

    return render_template(
        "auth/resend_activation.html",
        title="Resend Activation Link",
        form=form
    )
