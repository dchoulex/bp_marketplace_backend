from werkzeug.exceptions import (
    Unauthorized, NotFound, BadRequest, InternalServerError
)

from flask_bcrypt import check_password_hash


def validate_user(user, **kwargs):
    try:
        if 'verify_user_exists' in kwargs and kwargs['verify_user_exists']:
            if user is None:
                raise NotFound("User does not exist.")
            
        if 'verify_already_exists' in kwargs and kwargs['verify_already_exists']:
            if user is not None:
                raise BadRequest('User with that email address already exists.')
        
        if 'check_password' in kwargs:
            if 'password' not in kwargs:
                raise BadRequest('Please input password.')
            
            if not check_password_hash(user.password, kwargs['password']):
                raise Unauthorized('Username or password is incorrect.')

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        raise

    except Exception as error:
        raise InternalServerError('Internal server error.')
