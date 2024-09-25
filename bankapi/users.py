from flask import request
from flask_restful import Resource

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from .app import db
from .db import User


class UserApi(Resource):
    def get(self):
        return "OK"

    def post(self):
        if request.path == "/login/":
            return self.login()
        elif request.path == "/register/":
            return self.register()


    def userExist(self, username):
        db_user = User.query.filter_by(username=username).first()

        if db_user:
            return True
        return False


    def login(self):
        print("Login...")

        try:
            username = request.json['username']

            db_user = User.query.filter_by(username=username).first()
            
            if not db_user:
                return {'message': 'User do not exists'}, 400

            password = request.json['password']


            # check_password_hash(<hashed_password>, <plain_password)
            if check_password_hash(db_user.password, password):
                # Return Token
                return {'message': 'Login successful'}


            return {'message': 'Invalid username or password'}

        except Exception as ERR:
            print("EXCEPTION: ", ERR)


    def register(self):
        print("registering...")
        try:
            username = request.json['username']

            if self.userExist(username):
                return {'message': 'User already exists'}, 400

            password = generate_password_hash(request.json['password'])

            # PRINT TEST
            print(username, password)

            user = User()
            user.username = username
            user.password = password

            # Write to Database
            db.session.add(user)
            db.session.commit()

        except Exception as ERR:
            print("EXCEPTION:", ERR)

        # Return User Id
        return {'message': "User registered",
                'id': user.id,
                'username': user.username,
        }
