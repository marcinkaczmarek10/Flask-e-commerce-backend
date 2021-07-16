from flask import Flask, Blueprint
from .config import Config
from .database.DB import db
from .OAuth.OAuth import oauth


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    oauth.init_app(app)

    #app.register_blueprint()
    return app
