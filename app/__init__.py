from flask import Flask
from Conf import Conf
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Conf)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"

from app import routes

from app.models.User import User
from app.models.Book import Book
from app.models.UserBooks import UserBooks

# if __name__ == "__main__":
#     app.run(threaded=True, port=5000)
