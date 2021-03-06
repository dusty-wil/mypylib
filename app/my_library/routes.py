from app.my_library import bp
from app import db

from flask import render_template, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from datetime import datetime

from app.email.email import send_mail

from app.my_library.forms.BookLibForm import BookLibForm
from app.my_library.forms.LibEntryForm import LibEntryForm
from app.my_library.forms.BookForm import BookForm
from app.my_library.forms.ShareLibraryForm import ShareLibraryForm

from app.models.Book import Book
from app.models.UserBooks import UserBooks
from app.models.User import User


@bp.route("/")
def index():
    return render_template(
        "my_library/index.html",
        title="Welcome!"
    )


@bp.route("/library")
@login_required
def summary():
    lib = UserBooks.query.join(Book).join(User).filter_by(id=current_user.id).all()

    return render_template(
        "my_library/lib_summary.html",
        title="My Library",
        lib=lib
    )


@bp.route("/library/books/add", methods=["GET", "POST"])
@bp.route("/library/books/add/<int:book_id>", methods=["GET"])
@login_required
def add_book_to_lib(book_id=None):
    if book_id:
        book = Book.query.filter_by(id=book_id).first()

        if not book:
            flash("This book doesn't exist!", category="error")
            return redirect(url_for("my_library.summary"))

        if book in current_user.books:
            flash("This book is already in your library!", category="info")
            return redirect(url_for("my_library.book_list"))

        library_meta = UserBooks(
            purch_date=datetime.now(),
            book=book,
            user=current_user
        )

        db.session.add(library_meta)
        db.session.commit()

        return redirect(url_for("my_library.edit_lib_entry", book_id=book.id))

    form = BookLibForm()

    if form.validate_on_submit():
        add_msg = "{} has been added to your library!".format(form.title.data)

        book = Book.query.filter_by(isbn=form.isbn.data).first()
        if book is not None:
            add_msg = "A book matching ISBN {} was found. Adding it to your library!".format(form.isbn.data)
        else:
            book = Book(
                title=form.title.data,
                author=form.author.data,
                isbn=form.isbn.data
            )

        db.session.add(book)
        db.session.commit()

        library_meta = UserBooks.query.filter_by(user_id=current_user.id, book_id=book.id).first()
        if library_meta is None:
            library_meta = UserBooks(
                purch_date=form.purch_date.data,
                notes=form.notes.data,
                book=book,
                user=current_user
            )

            db.session.add(library_meta)
            db.session.commit()

            flash(add_msg, category="info")

        return redirect(url_for("my_library.summary"))

    return render_template(
        "my_library/add_book_to_lib.html",
        title="Add a Book to Your Library",
        form=form
    )


@bp.route("/library/books/delete/<int:book_id>", methods=["GET", "DELETE"])
@login_required
def del_book_from_lib(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book:
        current_user.books.remove(book)
        db.session.commit()
        flash("Entry for {} removed from your library!".format(book.title), category="info")

    return redirect(url_for("my_library.summary"))


@bp.route("/library/books/edit/<int:book_id>", methods=["GET", "POST"])
@login_required
def edit_lib_entry(book_id):
    book = Book.query.filter_by(id=book_id).first()
    lib_entry = UserBooks.query.filter_by(user_id=current_user.id, book_id=book_id).first()

    if lib_entry is None or book is None:
        return redirect(url_for("my_library.summary"))

    form = LibEntryForm()

    if form.validate_on_submit():
        lib_entry.purch_date = form.purch_date.data
        lib_entry.notes = form.notes.data
        db.session.commit()

        flash("Library entry for {} updated!".format(book.title), category="info")
        return redirect(url_for("my_library.summary"))

    form.purch_date.data = lib_entry.purch_date
    form.notes.data = lib_entry.notes

    return render_template(
        "my_library/edit_library_entry.html",
        title="Edit Your Library Entry",
        form=form,
        book=book
    )


@bp.route("/books")
@login_required
def book_list():
    books = Book.query.all()

    return render_template(
        "my_library/all_books.html",
        title="All Books",
        books=books
    )


@bp.route("/books/edit/<int:book_id>", methods=["GET", "POST"])
@login_required
def edit_book(book_id):
    book = Book.query.filter_by(id=book_id).first()

    if book is None:
        return redirect(url_for("my_library.summary"))

    form = BookForm()

    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        db.session.commit()

        flash("Book entry for ISBN {} updated!".format(book.isbn), category="info")
        return redirect(url_for("my_library.summary"))

    form.title.data = book.title
    form.author.data = book.author

    return render_template(
        "my_library/edit_book.html",
        title="Edit Book",
        form=form,
        book=book
    )


@bp.route("/library/share", methods=["GET", "POST"])
@login_required
def share_library():
    form = ShareLibraryForm()

    if form.validate_on_submit():
        lib = UserBooks.query.join(Book).join(User).filter_by(id=current_user.id).all()

        send_mail(
            subject="My Python Library: Shared Library",
            sender=current_app.config['ADMIN'],
            recipients=[form.email.data],
            txt_body=render_template(
                "email/share_library_email.txt",
                lib=lib,
                recipient=form.email.data,
                user_email=current_user.email
            ),
            html_body=render_template(
                "email/share_library_email.html",
                lib=lib,
                recipient=form.email.data,
                user_email=current_user.email
            )
        )

        flash("Your library has been shared with {}!".format(form.email.data), category="info")
        return redirect(url_for("my_library.summary"))

    return render_template(
        "my_library/share_library.html",
        title="Share Your Library",
        form=form
    )