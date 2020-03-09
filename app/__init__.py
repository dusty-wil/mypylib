from flask import Flask
from Conf import Conf
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

login = LoginManager()
login.login_view = "auth.login"
login.login_message = "Please log in to access this page."


def create_app(config_class=Conf):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.my_library import bp as mylib_bp
    app.register_blueprint(mylib_bp)

    from app.email import bp as email_bp
    app.register_blueprint(email_bp)

    return app


from app.models import Book, UserBooks, User