import lorem
from datetime import datetime


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

def init_table():
    sql_script = generate_product_insert_sql()
    with open("init_products.sql", "w") as file:
        file.write(sql_script)
