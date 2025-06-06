from flask import request, jsonify
from flask_restful import Resource

from flask_jwt_extended import jwt_required, \
    get_jwt_identity

from api.database import db
from api.models import User, Account


class AdminApi(Resource):
    def get(self):
        accounts = Account.query.all()
        user_accounts = jsonify([account.to_dict() for account in accounts])
        return user_accounts


class AccountApi(Resource):
    @jwt_required()
    def get(self, id=None):
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
        # Create Account
        username = get_jwt_identity()

        user = User.query.filter_by(username=username).first()

        # Check if a initial balance was requested
        try:
            initial_balance = request.json['initial_balance']
        except Exception as ERR:
            print("Exception ", ERR)
            initial_balance = 0

        account = Account.query.filter_by(uid=user.id).first()

        if not account:
            account = Account()
            account.uid = user.id
            account.account_type = "Debit"

        account.balance = initial_balance

        # Write to Database
        db.session.add(account)
        db.session.commit()

        return {'msg': 'Account Updated',
                'id': account.id,
                'uid': account.uid,
                'balance': account.balance,
                }, 200
