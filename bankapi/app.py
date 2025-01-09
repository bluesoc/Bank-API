#!/bin/python3
import secrets

from flask import Flask
from flask_restful import Api

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from api.config import Config
from api.database import db

from api.users import UserApi
# from api.transactions import TransactionApi
from api.accounts import AccountApi, AdminApi
from api.transactions import TransactionApi


app = Flask(__name__)
api = Api(app)

# Load Config
app.config.from_object(Config)

# Config JWT
jwt = JWTManager(app)

# Local Database Config
db.init_app(app)


with app.app_context():
    from api.models import User
    db.create_all()


api.add_resource(UserApi, '/register/', '/login/')
api.add_resource(AccountApi, '/accounts/')

api.add_resource(TransactionApi, '/transactions/')

# For tests only
# api.add_resource(AdminApi, "/admin")
