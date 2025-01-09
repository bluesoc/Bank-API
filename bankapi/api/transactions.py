from flask import request, jsonify
from flask_restful import Resource

from flask_jwt_extended import jwt_required, \
    get_jwt_identity

from api.database import db
from api.models import User, Account, Transaction


class TransactionApi(Resource):
    @jwt_required()
    def post(self):
        # Get User Identity
        user_name = get_jwt_identity()
        sender_user = User.query.filter_by(username=user_name).first()

        if not sender_user:
            return {'msg': 'User not found'}, 404

        # Get Account associated with sender_user
        sender_account = Account.query.filter_by(uid=sender_user.id).first()

        if not sender_account:
            return {'msg': 'No accounts found for this user'}, 404

        #
        # Get data from request
        #
        data = request.get_json()
        account_receiver_id = data.get('account_receiver')
        amount = data.get('amount')

        #
        # Check if data is valid
        #
        if not sender_account.id or not account_receiver_id or not amount:
            print(f"{sender_account.id} -> {account_receiver_id} R$ {amount}")
            return {'msg': 'Missing data'}, 400

        if sender_account.balance <= 0:
            return {'msg': 'Error: Account has negative debit.'}, 403

        if (sender_account.balance - amount) < 0:
            return {'msg': 'Insufficient balance to complete the transaction'}, 403

        receiver_account = Account.query.filter_by(
            id=account_receiver_id).first()

        if not sender_account or not receiver_account:
            return {'msg': 'Invalid accounts'}, 400

        # Create new transaction
        new_transaction = Transaction(
            user_uid=sender_user.id,
            account_sender=sender_account.id,
            account_receiver=account_receiver_id,
            amount=amount
        )

        sender_account.balance -= amount
        receiver_account.balance += amount

        # Add new information to be commited
        db.session.add(receiver_account)
        db.session.add(sender_account)

        db.session.add(new_transaction)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'msg': 'Transaction could not be completed'}, 500

        return {'msg': 'Transaction created successfully', 'transaction_id': new_transaction.id}, 200
