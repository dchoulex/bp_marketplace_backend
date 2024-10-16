import lorem
import random
from datetime import datetime, timedelta


def generate_product_insert_sql():
    sql_statements = []
    for i in range(1, 11):
        product_id = f"p{i}"
        account_id = str(i)
        title = f"Product {i}"
        price = i * 10.0
        video_url = f"http://example.com/video{i}.mp4"
        photo_url = f"http://example.com/photo{i}.jpg"
        product_type = f"Type {chr(64+i)}"
        description = lorem.paragraph()
        created_time = datetime.now().isoformat()

        sql = f"INSERT INTO products (product_id, account_id, title, price, video_urls, photo_urls, product_type, description, created_time) " \
              f"VALUES ('{product_id}', '{account_id}', '{title}', {price}, '{{{video_url}}}', '{{{photo_url}}}', '{product_type}', '{description}', '{created_time}') ON CONFLICT (product_id) DO NOTHING;"
        
        sql_statements.append(sql)

    return "\n".join(sql_statements)

def generate_order_insert_sql():
    sql_statements = []
    location = [f'p{i}' for i in range(1, 11)]
    account_ids = [str(i) for i in range(1, 11)]
    for i in range(1, 11):
        order_id = f'o{i}'
        buyer_account_id = random.choice(account_ids)
        seller_account_id = random.choice(account_ids)
        product_id = f'p{seller_account_id}'
        purchased_date = datetime.now() - timedelta(random.randint(0, 30))
        booking_time = purchased_date + timedelta(hours=random.randint(1, 48))
        meetup_location = f"Location {i}"


        sql = f"INSERT INTO orders (order_id, buyer_account_id, seller_account_id, product_id, purchased_date, booking_time, meetup_location) VALUES " \
              f"('{order_id}', '{buyer_account_id}', '{seller_account_id}', '{product_id}', '{purchased_date.isoformat()}', '{booking_time.isoformat()}', '{meetup_location}') ON CONFLICT (order_id) DO NOTHING;"
        
        sql_statements.append(sql)
    
    return "\n".join(sql_statements)



def init_table():
    sql_script = (generate_product_insert_sql() + '\n' + generate_order_insert_sql())
    with open("init_products.sql", "w") as file:
        file.write(sql_script)
