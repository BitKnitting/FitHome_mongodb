#!/home/pi/projects/FitHome_mongodb/venv/bin/python3
# See https://youtu.be/3ZS7LEH_XBg?t=290
from flask import Flask

from .extensions import mongo
from .main import main


def create_app(config_object='flask_readings.settings'):
    app = Flask(__name__)

    app.config.from_object(config_object)

    mongo.init_app(app)

    app.register_blueprint(main)

    return app
