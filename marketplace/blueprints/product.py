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

from datetime import datetime

import traceback

product_bp = Blueprint('product', __name__)

@product_bp.route('/create', methods = ['POST'])
@jwt_required()
def post_product():
    account_id = get_jwt_identity()

    try:
        if request.method == 'POST':
            data = request.get_json()
            product_data = db_query.create_product(account_id, data)

            jwt.refresh_expiring_jwts(product_data)

            return make_response(product_data, 200)

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        print(traceback.format_exc())
        raise

    except Exception as error:
        print(traceback.format_exc())
        raise InternalServerError('Internal server error.')

@product_bp.route('/', methods = ['GET'])
def get_all_products():
    try:
        if request.method == 'GET':
            input_page = int(request.args.get('page', 1))
            input_limit = int(request.args.get('limit', 10))

            product_data = db_query.fetch_all_products(input_page, input_limit)
            
            response_body = jsonify({
                'products': product_data,
                "page": input_page,
                'limit': input_limit
            })

            return make_response(response_body, 200)

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        print(traceback.print_exc())
        raise

    except Exception as error:
        print(traceback.format_exc())
        raise InternalServerError('Internal server error.')
    
@product_bp.route('/<product_id>', methods = ['GET'])
def get_product_detail(product_id):
    try:
        if request.method == 'GET':
            product_data = db_query.fetch_product_detail(product_id)

            response_body = jsonify(product_data)

            return make_response(response_body, 200)

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        print(traceback.format_exc())
        raise

    except Exception as error:
        print(traceback.format_exc())
        raise InternalServerError('Internal server error.')
    
@product_bp.route('/purchase', methods = ['POST'])
@jwt_required()
def purchase_product():
    account_id = get_jwt_identity()

    try:
        if request.method == 'POST':
            input_product_id = request.json.get('product_id', None)
            input_booking_time = request.json.get('booking_time', None)
            input_meetup_location = request.json.get('meetup_location', None)

            if input_product_id is None or input_booking_time is None or input_meetup_location is None:
                raise BadRequest('Invalid input.')
            
            data = {
                'booking_time': input_booking_time,
                'meetup_location': input_meetup_location
            }
            
            order = db_query.purchase_product(account_id, input_product_id, data)
            

            # data = request.get_json()
            # product_data = db_query.create_product(account_id, data)
            repsonse_body = jsonify(order)

            jwt.refresh_expiring_jwts(repsonse_body)

            return make_response(repsonse_body, 200)

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        print(traceback.format_exc())
        raise

    except Exception as error:
        print(traceback.format_exc())
        raise InternalServerError('Internal server error.')