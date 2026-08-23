from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # Primary key[cite: 1]
    username = Column(String, unique=True, index=True) # Unique username[cite: 1]
    email = Column(String, unique=True, index=True) # User email[cite: 1]
    hashed_password = Column(String) # Encrypted password[cite: 1]

    transactions = relationship("Transaction", back_populates="owner")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True) # Primary key[cite: 1]
    title = Column(String, index=True) # Transaction title[cite: 1]
    amount = Column(Float) # Transaction amount[cite: 1]
    type = Column(String) # "income" or "expense"[cite: 1]
    category = Column(String) # Transaction category[cite: 1]
    date = Column(Date) # Transaction date[cite: 1]
    owner_id = Column(Integer, ForeignKey("users.id")) # Foreign key[cite: 1]

    owner = relationship("User", back_populates="transactions")
    