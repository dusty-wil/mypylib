from flask import Blueprint

bp = Blueprint("my_library", __name__)

from app.my_library import routes
