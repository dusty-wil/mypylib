from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True, nullable=False)
    author = db.Column(db.String(64), index=True, nullable=False)
    isbn = db.Column(db.String(16), index=True, nullable=False, unique=True)
    users = db.relationship("User", secondary="user_books", backref=db.backref("Book"))

    def __repr__(self):
        return "<Book {}>".format(self.title)
