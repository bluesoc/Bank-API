from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import mapped_column

from .app import db

class User(db.Model):
    id = mapped_column(db.Integer, primary_key=True)
    username = mapped_column(db.String, nullable=False)
    password = mapped_column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
        }


class Account(db.Model):
    id = mapped_column(db.Integer, primary_key=True)
    uid = mapped_column(db.Integer, nullable=False)

    account_type = mapped_column(db.String, nullable=False)
    balance = mapped_column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'account_type': self.username,
            'balance': self.password,
        }