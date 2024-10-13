import os
from datetime import timedelta

API_VERSION = os.getenv('API_VERSION')

AUTH_API_PREFIX = f'/api/{API_VERSION}/auth'
ACCOUNT_API_PREFIX = f'/api/{API_VERSION}/accounts'
PRODUCT_API_PREFIX = f'/api/{API_VERSION}/products'
ORDER_API_PREFIX = f'/api/{API_VERSION}/orders'

DB_NAME = 'postgres'
DB_USERNAME = 'postgres'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_PORT = '5432'

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
JWT_TOKEN_LOCATION = os.getenv('JWT_TOKEN_LOCATION').split(" ")
JWT_COOKIE_SECURE = True if os.getenv('JWT_COOKIE_SECURE').lower().strip() == 'true' else False
JWT_COOKIE_CSRF_PROTECT = True if os.getenv('JWT_COOKIE_CSRF_PROTECT').lower().strip() == 'true' else False
JWT_COOKIE_SAMESITE = os.getenv('JWT_COOKIE_SAMESITE')

SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'max_overflow': 20,
    'pool_timeout': 30,
    'echo_pool': True,
    'pool_pre_ping': True
}

TOKEN_REFRESH_SECONDS = int(os.getenv('TOKEN_REFRESH_SECONDS'))