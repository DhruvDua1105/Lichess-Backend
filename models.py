from database import Base
from sqlalchemy import  Column, Integer, String

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, index= True)
    email_ID = Column(String, unique=True) 
    hashed_password = Column(String)