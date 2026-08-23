from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db, Base
from router.auth import get_current_user
import models

# 1. Setup a separate SQLite database for testing
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the test database
Base.metadata.create_all(bind=engine)

# Override database dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override authentication to avoid repeated token generation
def override_get_current_user():
    return models.User(id=1, username="testuser", email="test@test.com", hashed_password="hashed")

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

# ==========================================
# 5 Test Cases (10 Marks)
# ==========================================

def test_create_transaction():
    # Create transaction test
    response = client.post(
        "/transactions/",
        json={"title": "Test Income", "amount": 1000, "type": "income", "category": "Salary", "date": "2026-08-23"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Income"

def test_get_transactions():
    # Get transaction test (all transactions)
    response = client.get("/transactions/")
    assert response.status_code == 200
    assert type(response.json()) == list

def test_get_specific_transaction():
    # Get specific transaction test
    # First, I'll try requesting ID 1
    response = client.get("/transactions/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_transaction():
    # Update transaction test
    response = client.put(
        "/transactions/1",
        json={"title": "Updated Income", "amount": 1500, "type": "income", "category": "Salary", "date": "2026-08-23"}
    )
    assert response.status_code == 200
    assert response.json()["amount"] == 1500

def test_delete_transaction():
    # Delete transaction test
    response = client.delete("/transactions/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction deleted successfully"
    
    # Verify deletion by checking for a 404 response
    check_response = client.get("/transactions/1")
    assert check_response.status_code == 404

    