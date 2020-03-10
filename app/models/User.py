from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registration_date = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    verified_date = db.Column(db.DateTime, index=True, nullable=True)

    # backref is used to declare a relationship on the second table as well.
    # books = db.relationship("Book", secondary="user_books", backref=db.backref("User"))
    # if relationships are being defined separately in each table, use back_populates instead
    # users = db.relationship("Book", secondary="user_books", back_populates="users")
    # however, in this case the backrefs are defined using the association table
    books = db.relationship("Book", secondary="user_books")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

