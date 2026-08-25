from fastapi import FastAPI
from database import engine
import models
from router import auth, transactions



# create DB tables if not exist 
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API"
)

# Connecting the routers to the app
app.include_router(auth.router)
app.include_router(transactions.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Expense Tracker API!"}
