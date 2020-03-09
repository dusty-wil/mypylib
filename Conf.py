import os
base_dir = os.path.abspath(os.path.dirname(__file__))


class Conf:
    SECRET_KEY = os.environ.get("SECRET_KEY") \
        or "h0 ly h4n dgr 3n4d 3!"

    PASSWORD_SALT = "s8dnjeRhsjdfYGjaasakj"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") \
        or "sqlite:///" + os.path.join(base_dir, "mypylib.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN = 'mypythonlibrary@gmail.com'

