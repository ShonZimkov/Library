from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#creating engine and sesion
engine = create_engine('sqlite:///library.sqlite3')
Session = sessionmaker(bind=engine)
Session2= sessionmaker(bind=engine)
Base = declarative_base()