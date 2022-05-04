from base import Base
from sqlalchemy import Column,Integer,String

#create a customers table
class Customer(Base):
    __tablename__='customers'

    id = Column(Integer , primary_key=True)
    name = Column(String)
    city = Column(String)
    age = Column(Integer)

    def __init__(self,name, city, age ):
        self.name = name
        self.city = city
        self.age = age