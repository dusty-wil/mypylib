import os
base_dir = os.path.abspath(os.path.dirname(__file__))


class Conf:
    SECRET_KEY = os.environ.get("SECRET_KEY") \
        or "h0 ly h4n dgr 3n4d 3!"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") \
        or "sqlite:///" + os.path.join(base_dir, "mypylib.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
