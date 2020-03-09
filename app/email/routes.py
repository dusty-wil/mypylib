from app.email import bp
from app.email.email import confirm_activation_token
from app import db

from flask import render_template, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from datetime import datetime

from app.models.User import User
from app.email.email import send_activation_email, send_mail
from app.email.forms.ResendActivationForm import ResendActivationForm
from app.email.forms.ShareLibraryForm import ShareLibraryForm

from app.models.UserBooks import UserBooks
from app.models.Book import Book


@bp.route("/activate/<token>")
def activate_email(token):
    if current_user.is_authenticated:
        return redirect(url_for("my_library.summary"))

    email = confirm_activation_token(token)
    if not email:
        flash("The activation link is invalid or expired. Please request another activation email", category="error")
        return redirect(url_for("email.resend_activate_email"))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("The activation link is invalid or expired. Please request another activation email", category="error")
        return redirect(url_for("email.resend_activate_email"))

    if user.verified_date is None:
        user.verified_date = datetime.now()
        db.session.commit()

    flash("Account has been activated. You can log in!", category="info")
    return redirect(url_for("auth.login"))


@bp.route("/activate/resend", methods=["GET", "POST"])
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
        "email/resend_link.html",
        title="Resend Activation Link",
        form=form
    )


@bp.route("/library/share", methods=["GET", "POST"])
@login_required
def share_library():
    form = ShareLibraryForm()

    if form.validate_on_submit():
        lib = UserBooks.query.join(Book).join(User).filter_by(id=current_user.id).all()

        send_mail(
            subject="My Little Python Library: Shared Library",
            sender=current_app.config['ADMIN'],
            recipients=[form.email.data],
            txt_body=render_template(
                "email/share_library.txt",
                lib=lib,
                recipient=form.email.data,
                user_email=current_user.email
            ),
            html_body=render_template(
                "email/share_library.html",
                lib=lib,
                recipient=form.email.data,
                user_email=current_user.email
            )
        )

        flash("Your library has been shared with {}!".format(form.email.data), category="info")
        return redirect(url_for("my_library.summary"))

    return render_template(
        "email/share_library_with.html",
        title="Share Your Library",
        form=form
    )
