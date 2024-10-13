CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    profile_picture_url TEXT,
    social_media_links TEXT,
    zid TEXT,
    pay_id TEXT,
    password TEXT
)

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT,
    account_id TEXT,
    title TEXT,
    price DOUBLE PRECISION,
    video_urls TEXT[],
    photo_urls TEXT[],
    product_type TEXT,
    description TEXT,
    created_time TIMESTAMPTZ
)

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT,
    buyer_account_id TEXT,
    seller_account_id TEXT,
    product_id TEXT,
    purchased_date TIMESTAMPTZ,
    booking_time TIMESTAMPTZ,
    meetup_location TEXT
)