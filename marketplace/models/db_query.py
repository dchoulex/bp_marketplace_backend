import psycopg2

import traceback

from werkzeug.exceptions import (
    Unauthorized, NotFound, InternalServerError, BadRequest
)



from sqlalchemy import select, update, insert, func, text, or_, distinct, delete, exc

from marketplace.models.db import db
from marketplace.utilities import validation, uuid, utils

from .product_model import Product
from .account_model import Account
from .order_model import Order

import traceback

from datetime import datetime


def fetch_account_info(**kwargs):
    try:
        user = None

        if 'account_id' in kwargs:
            user = db.session.execute(select(Account).where(Account.account_id == kwargs['account_id'])).scalar()
        elif 'email' in kwargs:
            user = db.session.execute(select(Account).where(Account.email == kwargs['email'])).scalar() 
        elif 'username' in kwargs:
            user = db.session.execute(select(Account).where(Account.username == kwargs['username'])).scalar()

        return user
    
    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        traceback.format_exc()
        raise

    except (Exception, psycopg2.Error, exc.SQLAlchemyError) as error:
        raise InternalServerError(error)
    
    finally:
        db.session.close()

def create_account(new_user_data):
    try:
        user = fetch_account_info(email = new_user_data['email'])
        validation.validate_user(user, verify_already_exists = True)

        if user is None:
            account_id = uuid.generate_uuid()
            password_hash = utils.hash_password(new_user_data['password'])
            create_user_sql = insert(Account).values(
                account_id = account_id, 
                username = new_user_data['username'], 
                first_name = new_user_data['first_name'], 
                last_name = new_user_data['last_name'], 
                email = new_user_data['email'], 
                profile_picture_url = new_user_data['profile_picture_url'], 
                social_media_links = new_user_data['social_media_links'], 
                zid = new_user_data['zid'],
                password = password_hash,
                pay_id = new_user_data['pay_id']
            )

            db.session.execute(create_user_sql)
            db.session.commit()

            user = fetch_account_info(account_id = account_id)

            return user

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        traceback.format_exc()
        raise

    except (Exception, psycopg2.Error, exc.SQLAlchemyError) as error:
        raise InternalServerError(error)
    
    finally:
        db.session.close()

def update_account_info(account_id, new_data):
    try:
        user = fetch_account_info(email = new_data['email'])
        validation.validate_user(user, verify_user_exists = True)

        update_account_sql = update(Account).where(Account.account_id == account_id).values(
            username = new_data['username'],
            first_name = new_data['first_name'],
            last_name = new_data['last_name'],
            email = new_data['email'],
            profile_picture_url = new_data['profile_picture_url'],
            social_media_links = new_data['social_media_links'],
        )

        db.session.execute(update_account_sql)
        db.session.commit()

        new_data['account_id'] = account_id

        return new_data

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        traceback.format_exc()
        raise

    except (Exception, psycopg2.Error, exc.SQLAlchemyError) as error:
        raise InternalServerError(error)
    
    finally:
        db.session.close()


def create_product(account_id, data):
    try:
        user = fetch_account_info(account_id = account_id)
        validation.validate_user(user, verify_user_exists = True)

        product_id = uuid.generate_uuid()

        create_product_sql = insert(Product).values(
            product_id = product_id, 
            account_id = account_id, 
            title = data['title'], 
            price = data['price'], 
            photo_urls = data['photo_urls'],
            video_urls = data['video_urls'], 
            product_type = data['product_type'], 
            description = data['description'], 
            created_time = datetime.now()
        )
        
        db.session.execute(create_product_sql)
        db.session.commit()

        data['product_id'] = product_id

        return data

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        traceback.format_exc()
        raise

    except (Exception, psycopg2.Error, exc.SQLAlchemyError) as error:
        raise InternalServerError(error)
    
    finally:
        db.session.close()

def fetch_all_products(page, limit):
    try:
        offset = (page - 1) * limit

        fetch_all_products_sql = f'SELECT * FROM PRODUCTS LIMIT {str(limit)} OFFSET {str(offset)}'

        products = db.session.execute(text(fetch_all_products_sql))

        filtered_products = list(map(lambda product: {
            'product_id': product.product_id,
            'account_id': product.account_id,
            'title': product.title,
            'price': product.price,
            'video_urls': product.video_urls,
            'photo_urls': product.photo_urls,
            'product_type': product.product_type,
            'description': product.description,
        }, products))

        return filtered_products

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        traceback.format_exc()
        raise

    except (Exception, psycopg2.Error, exc.SQLAlchemyError) as error:
        raise InternalServerError(error)
    
    finally:
        db.session.close()

def fetch_product_detail(product_id):
    try:
        fetch_product_detail_sql = select(Product).where(Product.product_id == product_id)

        product = db.session.execute(fetch_product_detail_sql).scalar()

        if product is None:
            raise NotFound('Product not found.')

        product_data = {
            'product_id': product.product_id,
            'account_id': product.account_id,
            'title': product.title,
            'price': product.price,
            'video_urls': product.video_urls,
            'photo_urls': product.photo_urls,
            'product_type': product.product_type,
            'description': product.description,
        }

        return product_data

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        traceback.format_exc()
        raise

    except (Exception, psycopg2.Error, exc.SQLAlchemyError) as error:
        traceback.format_exc()
        raise InternalServerError(error)
    
    finally:
        db.session.close()

def fetch_all_orders(page, limit):
    try:
        offset = (page - 1) * limit

        fetch_all_orders_sql = f'SELECT * FROM ORDERS LIMIT {str(limit)} OFFSET {str(offset)}'

        orders = db.session.execute(text(fetch_all_orders_sql))

        filtered_orders = list(map(lambda order: {
            'order_id': order.order_id,
            'buyer_account_id': order.buyer_account_id,
            'seller_account_id': order.seller_account_id,
            'product_id': order.product_id,
            'purchased_date': order.purchased_date,
            'booking_time': order.booking_time,
            'meetup_location': order.meetup_location,
        }, orders))

        return filtered_orders

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        traceback.format_exc()
        raise

    except (Exception, psycopg2.Error, exc.SQLAlchemyError) as error:
        raise InternalServerError(error)
    
    finally:
        db.session.close()


def fetch_order_detail(order_id):
    try:
        fetch_order_detail_sql = select(Order).where(Order.order_id == order_id)

        order = db.session.execute(fetch_order_detail_sql).scalar()

        if order is None:
            raise NotFound('Order not found.')
        
        order_data = {
            'order_id' : order.order_id,
            'buyer_account_id' : order.buyer_account_id,
            'seller_account_id' : order.seller_account_id,
            'product_id' : order.product_id,
            'purchased_date' : order.purchased_date,
            'booking_time' : order.booking_time,
            'meetup_location' : order.meetup_location
        }

        return order_data

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        traceback.format_exc()
        raise

    except (Exception, psycopg2.Error, exc.SQLAlchemyError) as error:
        raise InternalServerError(error)
    
    finally:
        db.session.close()

def purchase_product(account_id, product_id, data):
    try:
        product = fetch_product_detail(product_id)
        order_id = uuid.generate_uuid()

        create_order_sql = insert(Order).values(
            order_id = order_id,
            buyer_account_id = account_id,
            seller_account_id = product['account_id'],
            product_id = product['product_id'],
            purchased_date = datetime.now(),
            booking_time = data['booking_time'],
            meetup_location = data['meetup_location']
        )

        db.session.execute(create_order_sql)
        db.session.commit()

        order = fetch_order_detail(order_id)

        return order

    except (Unauthorized, NotFound, BadRequest, InternalServerError) as error:
        traceback.format_exc()
        raise

    except (Exception, psycopg2.Error, exc.SQLAlchemyError) as error:
        raise InternalServerError(error)
    
    finally:
        db.session.close()