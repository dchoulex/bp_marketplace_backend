from flask import (
    Blueprint, jsonify, make_response, request, current_app
)

from flask_jwt_extended import (
    set_access_cookies, unset_jwt_cookies, get_jwt_identity, jwt_required
)

import requests
import json

from marketplace.models import db_query
from marketplace.utilities import jwt

from werkzeug.exceptions import (
    Unauthorized, NotFound, BadRequest, InternalServerError
)

import traceback

account_bp = Blueprint('account', __name__)

@account_bp.route('/create', methods = ['POST'])
def create_account():
    try:
        if request.method == 'POST':
            input_username = request.json.get('username', None)
            input_password = request.json.get('password', None)
            input_first_name = request.json.get('first_name', None)
            input_last_name = request.json.get('last_name', None)
            input_email = request.json.get('email', None)
            input_profile_picture_url = request.json.get('profile_picture_url', None)
            input_social_media_links = request.json.get('social_media_links', {})
            input_zid = request.json.get('zid', None)
            input_pay_id = request.json.get('pay_id', None)

            new_user_data = {
                'username': input_username,
                'password': input_password,
                'first_name': input_first_name,
                'last_name': input_last_name,
                'email': input_email,
                'profile_picture_url': input_profile_picture_url,
                'social_media_links': input_social_media_links,
                'zid': input_zid,
                'pay_id': input_pay_id
            }

            user = db_query.create_account(new_user_data)
            access_token = jwt.generate_jwt_token(user.account_id)

            response_body = jsonify({
                'account_id': user.account_id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'profile_picture_url': user.profile_picture_url,
                'social_media_links': user.social_media_links,
            })

            set_access_cookies(response_body, access_token)

            return make_response(response_body, 200)

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        print(traceback.format_exc())
        raise

    except Exception as error:
        print(traceback.format_exc())
        raise InternalServerError('Internal server error.')

@account_bp.route('/info', methods = ['GET', 'PUT'])
@jwt_required()
def get_account_info():
    try:
        account_id = get_jwt_identity()

        if request.method == 'GET':
            account = db_query.fetch_account_info(account_id = account_id)

            account_info = {
                'account_id': account_id,
                'username': account.username,
                'first_name': account.first_name,
                'last_name': account.last_name,
                'email': account.email,
                'profile_picture_url': account.profile_picture_url,
                'social_media_links': account.social_media_links,
                'zid': account.zid,
                'pay_id': account.pay_id
            }

            response_body = jsonify(account_info)

            jwt.refresh_expiring_jwts(response_body)

            return make_response(response_body, 200)
        
        if request.method == 'PUT':
            new_data = request.get_json()

            response_body = db_query.update_account_info(account_id, new_data)

            jwt.refresh_expiring_jwts(response_body)

            return make_response(response_body, 200)

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        print(traceback.format_exc())
        raise

    except Exception as error:
        print(traceback.format_exc())
        raise InternalServerError('Internal server error.')


