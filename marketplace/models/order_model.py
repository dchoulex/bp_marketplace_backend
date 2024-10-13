from sqlalchemy import Text, Time, DOUBLE_PRECISION, ARRAY
from sqlalchemy.orm import mapped_column
from .base import Base

class Order(Base):
    __tablename__ = 'orders'

    order_id = mapped_column(Text, primary_key=True)
    buyer_account_id = mapped_column(Text)
    seller_account_id = mapped_column(Text)
    product_id = mapped_column(Text)
    purchased_date = mapped_column(Time)
    booking_time = mapped_column(Time)
    meetup_location = mapped_column(Text)
