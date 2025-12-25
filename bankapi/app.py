#!/bin/python3
import secrets

from flask import Flask
from flask_restful import Api

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from datetime import timedelta

from gunicorn.app.base import BaseApplication

from api.config import Config
from api.database import db

from api.users import UserApi
from api.accounts import AccountApi, AdminApi
from api.transactions import TransactionApi


class GunicornApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.app = app
        super().__init__()

    def load(self):
        return self.app

    def load_config(self):
        config = {
            'bind': '0.0.0.0:5000',
            'workers': 4,
        }
        for key, value in config.items():
            self.cfg.set(key, value)


app = Flask(__name__)
api = Api(app)

# Load Config
app.config.from_object(Config)

# Config JWT
jwt = JWTManager(app)

# Set JWT Token Duration
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=10)

# Local Database Config
db.init_app(app)


with app.app_context():
    from api.models import User
    db.create_all()


api.add_resource(UserApi, '/register/', '/login/')
api.add_resource(AccountApi, '/accounts/')

api.add_resource(TransactionApi, '/transactions/')

# Dev only
if app.config["ENV"] == "development":
    # Allow /admin endpoint during development
    api.add_resource(AdminApi, "/admin")


if __name__ == '__main__':
    app_instance = GunicornApplication(app)
    app_instance.run()