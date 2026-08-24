# Expense Tracker API

A robust and secure RESTful API built with **FastAPI** for managing personal expenses and incomes. This project features JWT-based authentication, full CRUD operations for transactions, advanced data filtering, and automated testing.

## Features

* **User Authentication:** Secure registration and login using JWT (JSON Web Tokens) and bcrypt password hashing.
* **Transaction Management:** Users can Create, Read, Update, and Delete their daily income and expense records.
* **Data Validation:** Automatic request validation using Pydantic models.
* **Advanced Filtering:** Filter transactions by type (income/expense), category, and amount range (min/max).
* **Database Integration:** Relational database management using SQLAlchemy and PostgreSQL (Supabase).
* **Automated Testing:** Comprehensive test suite written with Pytest using an isolated SQLite test database.

## Tech Stack

* **Framework:** FastAPI
* **Database:** PostgreSQL (Supabase) / SQLite (for testing)
* **ORM:** SQLAlchemy
* **Data Validation:** Pydantic
* **Authentication:** Passlib (Bcrypt), Python-Jose (JWT)
* **Testing:** Pytest
* **Deployment:** Render

## 🔗 Live Demo

* **Live API (Swagger UI):** https://expense-tracker-api-9x5u.onrender.com

## Local Setup & Installation

Follow these steps to run the project on your local machine.

### 1. Clone the repository
```bash
git clone https://github.com/rubina23/Expense-Tracker-API.git
cd Expense-Tracker-API

```
### 2. Create and activate a virtual environment
- Windows:
```
    python -m venv venv
    venv\Scripts\activate

```
- Mac/Linux:
```
    python3 -m venv venv
    source venv/bin/activate

```
### 3. Install dependencies
```
pip install -r requirements.txt

```
### 4. Database Configuration
Ensure your database.py file has the correct PostgreSQL/Supabase connection string for the live server, or configure it to use SQLite for local development.
``` 
```
### 5. Run the application
```
uvicorn main:app --reload

```
### Running Tests
To run the automated test suite with the isolated testing database, simply execute:
```
pytest -v
