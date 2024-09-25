from flask import request, jsonify
from flask_restful import Resource

from flask_jwt_extended import jwt_required, \
    get_jwt_identity

from .app import db
from .db import User
from .db import Account


class AccountApi(Resource):
    @jwt_required()
    def get(self):
        # Return User Accounts
        user = get_jwt_identity()

        # Get User Model
        db_user = User.query.filter_by(username=user).first()

        # Get all Accounts associated with User
        accounts = Account.query.filter_by(uid=db_user.id)

        # Accounts in JSON format
        user_accounts = jsonify([account.to_dict() for account in accounts])

        return user_accounts


    @jwt_required()
    def post(self):
        # Create Accounts
        username = get_jwt_identity()

        user = User.query.filter_by(username=username).first()

        account = Account()
        account.uid = user.id
        account.account_type = "Savings"
        account.balance = 0

        # Write to Database
        db.session.add(account)
        db.session.commit()

        return {'message': 'Account created'}
