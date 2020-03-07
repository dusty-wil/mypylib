from app import app
from flask import render_template, flash, redirect, url_for

from app.LoginForm import LoginForm


@app.route("/")
def index():
    return render_template(
        "index.html"
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash("Login requested for user {}, remember = {}".format(form.email.data, form.remember.data))
        return redirect(url_for("index"))

    return render_template(
        "login.html",
        title="Log In",
        form=form
    )


@app.route("/lib-summary")
def summary():
    books = [
        {
            'title': "Abbadon's Gate",
            'author': "James S. A. Corey",
            'purch_date': "2020-01-12 15:43:25",
            'notes': "Cool"
        },
        {
            'title': "Abbadon's Gate 2, The Gatening",
            'author': "James S. A. Corey"
        }
    ]

    return render_template(
        "lib-summary.html",
        title="Library Summary",
        books=books
    )
