from app import db
from datetime import datetime


class UserBooks(db.Model):
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)
    book_id = db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True)
    purch_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    notes = db.Column(db.String(1024))

    # backref is used to declare a relationship on the second table as well.
    # This sets up a structure like:
    # UserBooks.book.owned_by
    # UserBooks.user.my_books
    # and enables lookups like:
    # (UserBooks)library_meta.user.my_books[0].book.title
    book = db.relationship("Book", backref=db.backref("owned_by"))
    user = db.relationship("User", backref=db.backref("my_books"))

    def __repr__(self):
        return "<UserBooks {} {}>".format(self.user_id, self.book_id)
