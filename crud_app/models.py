from sqlalchemy import Boolean, Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import MONEY

from .database import Base

class books(Base):
    __tablename__ = 'book'

    id        = Column(Integer, primary_key=True)
    title     = Column(String)
    author    = Column(String)
    pages     = Column(Integer)
    published = Column(Date)
    price     = Column(MONEY)
