from flask import request, jsonify
from flask_restful import Resource

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from flask_jwt_extended import create_access_token

from api.database import db
from api.models import User


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

    def generateJWT(self, username):
        access_token = create_access_token(identity=username)
        return access_token

    def login(self):
        try:
            username = request.json['username']

            db_user = User.query.filter_by(username=username).first()

            if not db_user:
                return {'message': 'User do not exists'}, 400

            password = request.json['password']

            # check_password_hash(<hashed_password>, <plain_password)
            if check_password_hash(db_user.password, password):
                # Return Token

                token = self.generateJWT(db_user.username)

                return {'message': 'Login successful',
                        'token': token,
                        }

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
                }, 200
