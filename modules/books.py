from datetime import date, datetime, timedelta

from flask import session
from base import Base
from sqlalchemy import Column, ForeignKey,Integer,String

#create a books table
class Book(Base):
    __tablename__='books'

    id = Column(Integer , primary_key=True)
    name = Column(String)
    author = Column(String)
    year = Column(Integer)
    type = Column(Integer)

    def __init__(self, name, author, year , type):
        self.name = name
        self.author = author
        self.year = year
        self.type = type