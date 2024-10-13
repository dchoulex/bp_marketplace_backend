from flask import current_app
from datetime import datetime
from flask_jwt_extended import (
    create_access_token, get_jwt, set_access_cookies, get_jwt_identity
)

def refresh_expiring_jwts(response_body):
    try:
        exp_timestamp = get_jwt()['exp']
        now = int(round(datetime.now().timestamp()))

        if now > exp_timestamp - current_app.config.get('TOKEN_REFRESH_SECONDS'):
            access_token = create_access_token(identity = get_jwt_identity())
            set_access_cookies(response_body, access_token)
            print('Successfully update jwt token.')

    except (RuntimeError, KeyError) as error:
        print(error)

def generate_jwt_token(account_id):
    return create_access_token(identity = account_id)