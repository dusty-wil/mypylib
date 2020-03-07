from app import app
from flask import render_template


@app.route("/")
def index():
    return render_template(
        "index.html"
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
