from pydantic import BaseModel, Field
from datetime import date
from typing import Literal

# ==========================
# User Schemas
# ==========================
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    # Password field is omitted as per requirements.

    class Config:
        from_attributes = True

# ==========================
# Token Schema
# ==========================
class Token(BaseModel):
    access_token: str
    token_type: str

# ==========================
# Transaction Schemas
# ==========================
class TransactionBase(BaseModel):
    title: str
    amount: float = Field(..., gt=0, description="Amount must be a positive number") # Amount > 0 validation 
    type: Literal["income", "expense"] # income or expense validation
    category: str
    date: date

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

