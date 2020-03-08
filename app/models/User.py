from app import db

# user_books = db.Table(
#     "user_books",
#     db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
#     db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True)
# )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    books = db.relationship("Book", secondary="user_books", backref=db.backref("User"))

    def __repr__(self):
        return "<User {}>".format(self.email)
