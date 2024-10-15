import os
import requests

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

from marketplace.blueprints import account, product, order, auth
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, Unauthorized

from .models.db import db

from marketplace import error_handling

def create_app():
    load_dotenv()

    app = Flask(__name__, instance_relative_config=False)
    jwt = JWTManager(app)
    cors = CORS(
        app,
        supports_credentials=True,
        resources={r"/*": {"origins": "*"}},
        methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST']
    )

    app.config.from_pyfile('config.py')

    db.init_app(app)

    with app.app_context():
        db.create_all()

      
        with open('init_table.sql', 'r') as sql_file:
            sql_statements = sql_file.read()
            
        for statement in sql_statements.split(';'):
            if statement.strip():
                db.session.execute(text(statement))
        db.session.commit()

    
    app.config.from_mapping(
        SECRET_KEY=app.config.get('SECRET_KEY'),
    )

    app.register_error_handler(NotFound, error_handling.handle_app_error)
    app.register_error_handler(Unauthorized, error_handling.handle_app_error)
    app.register_error_handler(InternalServerError, error_handling.handle_app_error)
    app.register_error_handler(BadRequest, error_handling.handle_app_error)
    app.register_error_handler(requests.exceptions.HTTPError, error_handling.handle_http_error)
    app.register_error_handler(requests.exceptions.RequestException, error_handling.handle_http_error)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    print(app.config.get('AUTH_API_PREFIX'))

    app.register_blueprint(auth.auth_bp, url_prefix = app.config.get('AUTH_API_PREFIX'))
    app.register_blueprint(account.account_bp, url_prefix = app.config.get('ACCOUNT_API_PREFIX'))
    app.register_blueprint(product.product_bp, url_prefix = app.config.get('PRODUCT_API_PREFIX'))
    app.register_blueprint(order.order_bp, url_prefix = app.config.get('ORDER_API_PREFIX'))

    return app
