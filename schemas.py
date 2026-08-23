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
    # রিকোয়ারমেন্ট অনুযায়ী এখানে পাসওয়ার্ড ফিল্ড রাখা হয়নি 

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
    amount: float = Field(..., gt=0, description="Amount must be a positive number") # Amount > 0 ভ্যালিডেশন 
    type: Literal["income", "expense"] # শুধুমাত্র income বা expense ভ্যালিডেশন
    category: str
    date: date

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True