import os


class Conf:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "h0 ly h4n dgr 3n4d 3!"
