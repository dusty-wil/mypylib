from app.email import bp
from app.email.email import confirm_token
from app import db

from flask import flash, redirect, url_for, render_template
from flask_login import current_user
from datetime import datetime

from app.models.User import User
from app.auth.forms.ResetPasswordForm import ResetPasswordForm


@bp.route("/activate/<token>")
def activate_email(token):
    if current_user.is_authenticated:
        return redirect(url_for("my_library.summary"))

    email = confirm_token(token)
    if not email:
        flash("The activation link is invalid or expired. Please request another activation email", category="error")
        return redirect(url_for("auth.resend_activate_email"))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("The activation link is invalid or expired. Please request another activation email", category="error")
        return redirect(url_for("auth.resend_activate_email"))

    if user.verified_date is None:
        user.verified_date = datetime.now()
        db.session.commit()

    flash("Account has been activated. You can log in!", category="info")
    return redirect(url_for("auth.login"))


@bp.route("/reset/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("my_library.summary"))

    email = confirm_token(token, expiration=1800)
    if not email:
        flash("The password reset link is invalid or expired. Please log in or send another request.", category="error")
        return redirect(url_for("my_library.index"))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("The password reset link is invalid or expired. Please log in or send another request.", category="error")
        return redirect(url_for("my_library.index"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Password has been reset. You can log in!", category="info")
        return redirect(url_for("auth.login"))

    return render_template(
        "auth/reset_password.html",
        title="Reset Your Password",
        form=form
    )
