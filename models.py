from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String, unique=True, index=True) 
    email = Column(String, unique=True, index=True) 
    hashed_password = Column(String) # Encrypted password

    transactions = relationship("Transaction", back_populates="owner")



class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String, index=True) 
    amount = Column(Float) 
    type = Column(String) # income or expense
    category = Column(String) 
    date = Column(Date) 
    owner_id = Column(Integer, ForeignKey("users.id")) 

    owner = relationship("User", back_populates="transactions")
    