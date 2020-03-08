from app import app

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.models.User import User
from app.forms.LoginForm import LoginForm
from app.forms.RegistrationForm import RegistrationForm

from app import db


@app.route("/")
@login_required
def index():
    return render_template(
        "index.html"
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))

        login_user(user, remember=form.remember.data)

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")

        return redirect(next_page)

    return render_template(
        "login.html",
        title="Log In",
        form=form
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Registration complete!")
        return redirect(url_for("login"))

    return render_template(
        "register.html",
        title="Register",
        form=form
    )


@app.route("/lib-summary")
@login_required
def summary():
    books = current_user.books

    return render_template(
        "lib-summary.html",
        title="Library Summary",
        books=books
    )
