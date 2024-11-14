from flask import request, jsonify
from flask_restful import Resource

from flask_jwt_extended import jwt_required, \
    get_jwt_identity

from api.database import db
from api.models import User, Account, Transaction


class TransactionApi(Resource):
    def get(self):
        return {'msg': 'ok'}

    @jwt_required()
    def post(self):
        # Return User Accounts
        user = get_jwt_identity()

        # Get User Model
        db_user = User.query.filter_by(username=user).first()

        # Get all Accounts associated with User
        accounts = Account.query.filter_by(uid=db_user.id)

        # GPT
        # Verificar se o usuário possui contas
        if not accounts:
            return {'msg': 'No accounts found for this user'}, 404

        # Obter dados da transação do corpo da requisição
        data = request.get_json()
        account_sender = data.get('account_sender')
        account_receiver = data.get('account_receiver')
        amount = data.get('amount')

        # Validar os dados da transação
        if not account_sender or not account_receiver or not amount:
            return {'msg': 'Missing data'}, 400

        # Verificar se as contas existem
        sender_account = Account.query.filter_by(
            id=account_sender, uid=db_user.id).first()
        receiver_account = Account.query.filter_by(
            id=account_receiver, uid=db_user.id).first()

        if not sender_account or not receiver_account:
            return {'msg': 'Invalid accounts'}, 400

        # Criar uma nova transação
        new_transaction = Transaction(
            user_uid=db_user.id,
            account_sender=account_sender,
            account_receiver=account_receiver,
            amount=amount
        )

        # Adicionar a transação ao banco de dados
        db.session.add(new_transaction)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'msg': 'Transaction could not be completed'}, 500

        return {'msg': 'Transaction created successfully', 'transaction_id': new_transaction.id}, 201
