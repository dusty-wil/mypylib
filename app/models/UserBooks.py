from app import db
from datetime import datetime

# user_books = db.Table(
#     "user_books",
#     db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
#     db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True)
# )


class UserBooks(db.Model):
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)
    book_id = db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True)
    purch_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    notes = db.Column(db.String(1024))
    book = db.relationship("Book", backref=db.backref("my_books"))
    user = db.relationship("User", backref=db.backref("owned_by"))

    def __repr__(self):
        return "<UserBooks {} {}>".format(self.user_id, self.book_id)
