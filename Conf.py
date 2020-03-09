import os
from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, ".env"))


class Conf:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    PASSWORD_SALT = os.environ.get("PASSWORD_SALT")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") \
        or "sqlite:///" + os.path.join(base_dir, "mypylib.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    ADMIN = 'mypythonlibrary@gmail.com'
