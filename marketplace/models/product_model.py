from sqlalchemy import Text, Time, DOUBLE_PRECISION, ARRAY
from sqlalchemy.orm import mapped_column
from .base import Base

class Product(Base):
    __tablename__ = 'products'

    product_id = mapped_column(Text, primary_key=True)
    account_id = mapped_column(Text)
    title = mapped_column(Text)
    price = mapped_column(DOUBLE_PRECISION)
    video_urls = mapped_column(ARRAY(Text))
    photo_urls = mapped_column(ARRAY(Text))
    product_type = mapped_column(Text)
    description = mapped_column(Text)
    created_time = mapped_column(Time)
