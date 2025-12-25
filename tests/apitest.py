#!/bin/python3
import os
import sys

import unittest

# Configure source folder
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../bankapi')))

from api.config import TestConfig  # noqa # This comment prevent autopep8
from bankapi.app import app        # noqa
from api.database import db        # noqa


# Clear Database Config
app.config.pop('SQLALCHEMY_DATABASE_URI', None)

# Load Testconfig
app.config.from_object(TestConfig)


IP = "127.0.0.1"
PORT = 5000

URL = f"{IP}:{PORT}"


# TEST USER
userdata = {
    "username": "dev@backend",
    "password": "4dm1nB4ck3ndTEST"
}

SECRET_TOKEN = ""


# TEST AUTHENTICATION
class TestAuth(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.token = ''

        # Create user and store login token
        self.test_register_and_login()

        # self.test_accounts()

    def test_register_and_login(self):
        response = self.app.post('/register/', json=userdata)

        print("[RESPONSE] REGISTER/")
        print(response.data)

        response = self.app.post('/login/', json=userdata)

        print("[RESPONSE] LOGIN/")
        print(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'token', response.data)

        # SAVE TOKEN
        self.token = response.json.get('token')

        return self.token

    def test_accounts(self):
        print("\nMY TOKEN IS:", self.token)

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        print("Headers:", headers)

        response = self.app.get('/accounts/', headers=headers)


if __name__ == '__main__':
    unittest.main()
