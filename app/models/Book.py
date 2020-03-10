from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True, nullable=False)
    author = db.Column(db.String(64), index=True, nullable=False)
    isbn = db.Column(db.String(16), index=True, nullable=False, unique=True)

    # backref is used to declare a relationship on the second table as well.
    # users = db.relationship("User", secondary="user_books", backref=db.backref("Book"))
    # if relationships are being defined separately in each table, use back_populates instead
    # users = db.relationship("User", secondary="user_books", back_populates="books")
    # however, in this case the backrefs are defined using the association table
    users = db.relationship("User", secondary="user_books")

    def __repr__(self):
        return "<Book {}>".format(self.title)
