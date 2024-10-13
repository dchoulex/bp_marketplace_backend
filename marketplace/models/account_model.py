from sqlalchemy import Text
from sqlalchemy.orm import mapped_column
from .base import Base

class Account(Base):
    __tablename__ = 'accounts'

    account_id = mapped_column(Text, primary_key=True)
    username = mapped_column(Text)
    password = mapped_column(Text)
    first_name = mapped_column(Text)
    last_name = mapped_column(Text)
    email = mapped_column(Text)
    profile_picture_url = mapped_column(Text)
    social_media_links = mapped_column(Text)
    zid = mapped_column(Text)
    pay_id = mapped_column(Text)