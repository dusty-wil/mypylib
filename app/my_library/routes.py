from app.my_library import bp
from app import db

from flask import render_template
from flask_login import current_user, login_required

from app.my_library.forms.BookForm import BookForm
from app.models.Book import Book
from app.models.UserBooks import UserBooks


@bp.route("/library")
@login_required
def summary():
    books = current_user.books

    return render_template(
        "my_library/lib_summary.html",
        title="My Library",
        books=books
    )


@bp.route("/books/add", methods=["GET", "POST"])
@login_required
def add_book():
    form = BookForm()

    if form.validate_on_submit():
        book = Book.query.filter_by(isbn=form.isbn.data).first() or Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data
        )
        db.session.add(book)
        db.session.commit()

        book_meta = UserBooks(
            purch_date=form.purch_date.data,
            notes=form.notes.data,
            book=book,
            user=current_user
        )
        db.session.add(book_meta)
        db.session.commit()

    return render_template(
        "my_library/add_edit_book.html",
        title="Add/Edit Book",
        form=form
    )
