from base import Base
from sqlalchemy import Column, Date, ForeignKey,Integer,String ,DateTime

#create loans table
class Loan(Base):
    __tablename__='loans'

    id = Column(Integer , primary_key=True)
    book_id = Column(Integer , ForeignKey("books.id"))
    cust_id = Column(Integer,ForeignKey("customers.id"))
    loan_date = Column(Date)
    return_date = Column(Date)
    status = Column(String,default="Not Returned")

        
    def __init__(self,book_id, cust_id, loan_date):
        self.book_id = book_id
        self.cust_id = cust_id
        self.loan_date = loan_date