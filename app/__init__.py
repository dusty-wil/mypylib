from flask import Flask
from Conf import Conf
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Conf)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "auth.login"

mail = Mail(app)

from app import routes

from app.models.User import User
from app.models.Book import Book
from app.models.UserBooks import UserBooks

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.my_library import bp as mylib_bp
app.register_blueprint(mylib_bp)

from app.email import bp as email_bp
app.register_blueprint(email_bp)

# if __name__ == "__main__":
#     app.run(threaded=True, port=5000)
