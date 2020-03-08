from app.my_library import bp

from flask import render_template
from flask_login import current_user, login_required


@bp.route("/library")
@login_required
def summary():
    books = current_user.books

    return render_template(
        "my_library/lib_summary.html",
        title="My Library",
        books=books
    )
