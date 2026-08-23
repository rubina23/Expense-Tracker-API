from fastapi import FastAPI
from database import engine
import models
from router import auth, transactions

# ডাটাবেসের টেবিলগুলো তৈরি করা (যদি আগে থেকে না থাকে)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="A Personal Expense Tracker API built with FastAPI",
    version="1.0.0"
)

# রাউটারগুলো অ্যাপের সাথে যুক্ত করা
app.include_router(auth.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Expense Tracker API!"}