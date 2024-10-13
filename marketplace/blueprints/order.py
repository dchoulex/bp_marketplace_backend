from flask import (
    Blueprint, jsonify, make_response, request, current_app
)

from flask_jwt_extended import (
    set_access_cookies, unset_jwt_cookies, get_jwt_identity, jwt_required
)

import requests
import json

from marketplace.models import db_query
from marketplace.utilities import jwt, uuid

from werkzeug.exceptions import (
    Unauthorized, NotFound, BadRequest, InternalServerError
)

import traceback

order_bp = Blueprint('order', __name__)

@order_bp.route('/', methods = ['GET'])
@jwt_required()
def get_all_order_histories():
    try:
        if request.method == 'GET':
            input_page = int(request.args.get('page', 1))
            input_limit = int(request.args.get('limit', 10))

            order_data = db_query.fetch_all_orders(input_page, input_limit)

            repsonse_body = jsonify({
                "orders": order_data,
                "limit": input_limit,
                "page": input_page
            })

            jwt.refresh_expiring_jwts(repsonse_body)

            return make_response(repsonse_body, 200)

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        print(traceback.format_exc())
        raise

    except Exception as error:
        print(traceback.format_exc())
        raise InternalServerError('Internal server error.')
    
@order_bp.route('/<order_id>', methods = ['GET'])
@jwt_required()
def get_order_detail(order_id):
    try:
        if request.method == 'GET':
            order_data = db_query.fetch_order_detail(order_id)

            response_body = jsonify(order_data)

            jwt.refresh_expiring_jwts(response_body)

            return make_response(response_body, 200)

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        print(traceback.format_exc())
        raise

    except Exception as error:
        print(traceback.format_exc())
        raise InternalServerError('Internal server error.')
    
