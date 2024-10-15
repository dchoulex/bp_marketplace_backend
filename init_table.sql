CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    profile_picture_url TEXT,
    social_media_links TEXT,
    zid TEXT,
    pay_id TEXT,
    password TEXT
);

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
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT,
    buyer_account_id TEXT,
    seller_account_id TEXT,
    product_id TEXT,
    purchased_date TIMESTAMPTZ,
    booking_time TIMESTAMPTZ,
    meetup_location TEXT
);

INSERT INTO accounts (account_id, username, first_name, last_name, email, profile_picture_url, social_media_links, zid, pay_id, password) VALUES
('1', 'user1', 'aaa', '1', 'user1@user.com', 'http://user.com/profile1.jpg', 'http://twitter.com/user1', 'z001', 'PAY001', 'password1'),
('2', 'user2', 'bbb', '2', 'user2@user.com', 'http://user.com/profile2.jpg', 'http://twitter.com/user2', 'z002', 'PAY002', 'password2'),
('3', 'user3', 'ccc', '3', 'user3@user.com', 'http://user.com/profile3.jpg', 'http://twitter.com/user3', 'z003', 'PAY003', 'password3'),
('4', 'user4', 'ddd', '4', 'user4@user.com', 'http://user.com/profile4.jpg', 'http://twitter.com/user4', 'z004', 'PAY004', 'password4'),
('5', 'user5', 'eee', '5', 'user5@user.com', 'http://user.com/profile5.jpg', 'http://twitter.com/user5', 'z005', 'PAY005', 'password5'),
('6', 'user6', 'fff', '6', 'user6@user.com', 'http://user.com/profile6.jpg', 'http://twitter.com/user6', 'z006', 'PAY006', 'password6'),
('7', 'user7', 'ggg', '7', 'user7@user.com', 'http://user.com/profile7.jpg', 'http://twitter.com/user7', 'z007', 'PAY007', 'password7'),
('8', 'user8', 'hhh', '8', 'user8@user.com', 'http://user.com/profile8.jpg', 'http://twitter.com/user8', 'z008', 'PAY008', 'password8'),
('9', 'user9', 'iii', '9', 'user9@user.com', 'http://user.com/profile9.jpg', 'http://twitter.com/user9', 'z009', 'PAY009', 'password9'),
('10', 'user10', 'jjj', '10', 'user10@user.com', 'http://user.com/profile10.jpg', 'http://twitter.com/user10', 'z010', 'PAY010', 'password10')
ON CONFLICT (account_id) DO NOTHING;
