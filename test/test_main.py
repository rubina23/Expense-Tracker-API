from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db, Base
from router.auth import get_current_user
import models

# ১. টেস্ট করার জন্য আলাদা একটি SQLite ডাটাবেস সেটআপ
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# টেস্ট ডাটাবেসে টেবিল তৈরি করা
Base.metadata.create_all(bind=engine)

# ডাটাবেস ডিপেন্ডেন্সি ওভাররাইড
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# অথেনটিকেশন ওভাররাইড (যাতে বারবার টোকেন জেনারেট করতে না হয়)
def override_get_current_user():
    return models.User(id=1, username="testuser", email="test@test.com", hashed_password="hashed")

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

# ==========================================
# 5 Test Cases (10 Marks)
# ==========================================

def test_create_transaction():
    # Create transaction test[cite: 1]
    response = client.post(
        "/transactions/",
        json={"title": "Test Income", "amount": 1000, "type": "income", "category": "Salary", "date": "2026-08-23"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Income"

def test_get_transactions():
    # Get transaction test (all transactions)[cite: 1]
    response = client.get("/transactions/")
    assert response.status_code == 200
    assert type(response.json()) == list

def test_get_specific_transaction():
    # Get specific transaction test[cite: 1]
    # প্রথমে ১ নম্বর আইডিতে রিকোয়েস্ট করে দেখব
    response = client.get("/transactions/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_transaction():
    # Update transaction test[cite: 1]
    response = client.put(
        "/transactions/1",
        json={"title": "Updated Income", "amount": 1500, "type": "income", "category": "Salary", "date": "2026-08-23"}
    )
    assert response.status_code == 200
    assert response.json()["amount"] == 1500

def test_delete_transaction():
    # Delete transaction test[cite: 1]
    response = client.delete("/transactions/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction deleted successfully"
    
    # ডিলিট করার পর চেক করে দেখা যে সত্যি ডিলিট হয়েছে কিনা (404 আসার কথা)
    check_response = client.get("/transactions/1")
    assert check_response.status_code == 404