from flask_bcrypt import generate_password_hash

def hash_password(password):
    return generate_password_hash(password).decode('utf8')