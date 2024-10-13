from flask import json, make_response, jsonify

def handle_app_error(e):
    response = e.get_response()

    response.data = json.dumps({
        'status_code': e.code,
        'msg': e.description
    })

    response.content_type = 'application/json'

    return response

def handle_http_error(error):
    description = error.response.text

    status_code = error.response.status_code

    response_data = jsonify({
        'status_code': error.response.status_code,
        'msg': description
    })

    return make_response(response_data, status_code)