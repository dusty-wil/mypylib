from flask import Flask
from Conf import Conf

app = Flask(__name__)
app.config.from_object(Conf)

from app import routes

if __name__ == "__main__":
    app.run(threaded=True, port=5000)