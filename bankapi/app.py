#!/bin/python3
import secrets

from flask import Flask
from flask_restful import Api

from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

# Generate 32 bytes long Secret_Key
app.secret_key = secrets.token_hex(16)

# JWT
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)
jwt = JWTManager(app)


# Database Filename
DB_NAME = "bank.db"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"


# Local Database Config
db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    # Import Database Tables
    from .db import User

    db.create_all()

    # Import API
    from .users import UserApi
    from .accounts import AccountApi


'''
    POST /register
    POST /login


    # MUST BE LOGGED IN

    POST /accounts
    # Create bank account for logged user


    GET /accounts/{accounts id}/transactions

    POST /accounts/{account id}/transfer

'''

api.add_resource(UserApi, '/register/', '/login/')
api.add_resource(AccountApi, '/accounts/')
