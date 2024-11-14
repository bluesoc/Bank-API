import secrets
import os
from os import getenv
from dotenv import load_dotenv

# Load .env
load_dotenv()


# Generate SECRET_KEY
def generate_secret_key():
    return secrets.token_hex()


def return_db_config():
    DB_URL = getenv('DATABASE_URL')

    if None == DB_URL:
        DB_URL = 'sqlite:///bank.db'

    return DB_URL


class Config:
    # Setup SECRET_KEY
    SECRET_KEY = getenv('SECRET_KEY', generate_secret_key())
    JWT_SECRET_KEY = generate_secret_key()

    SQLALCHEMY_DATABASE_URI = return_db_config()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    SECRET_KEY = generate_secret_key()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
