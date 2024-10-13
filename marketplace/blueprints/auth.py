from flask import (
    Blueprint, jsonify, make_response, request, current_app
)

from flask_jwt_extended import (
    set_access_cookies, unset_jwt_cookies, get_jwt_identity, jwt_required
)

import requests
import json

from marketplace.models import db_query
from marketplace.utilities import jwt, validation, utils

from werkzeug.exceptions import (
    Unauthorized, NotFound, BadRequest, InternalServerError
)

import traceback

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods = ['POST'])
def login():
    try:
        if request.method == 'POST':
            input_username = request.json.get('username', None)
            input_password = request.json.get('password', None)

            user = db_query.fetch_account_info(username = input_username)
            validation.validate_user(user, verify_user_exists = True, check_password = True, password = input_password)

            account_id = user.account_id

            response_body = jsonify({
                'account_id': account_id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'profile_picture_url': user.profile_picture_url,
                'social_media_links': user.social_media_links,
                'zid': user.zid,
                'pay_id': user.pay_id
            })

            access_token = jwt.generate_jwt_token(account_id)
            
            set_access_cookies(response_body, access_token)

            return make_response(response_body, 200)

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        print(traceback.format_exc())
        raise

    except Exception as error:
        print(traceback.format_exc())
        raise InternalServerError('Internal server error.')

@auth_bp.route('/logout', methods = ['POST'])
def logout():
    try:
        if request.method == 'POST':
            response_body = jsonify(None)

            unset_jwt_cookies(response_body)
            return make_response(response_body, 204)

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        print(traceback.format_exc())
        raise

    except Exception as error:
        print(traceback.format_exc())
        raise InternalServerError('Internal server error.')


