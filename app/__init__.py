import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # suppress SQLAlchemy error
    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app