from flask import Flask
from Conf import Conf
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_manager

app = Flask(__name__)
app.config.from_object(Conf)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
from app.models import User, Book, UserBooks


# if __name__ == "__main__":
#     app.run(threaded=True, port=5000)
