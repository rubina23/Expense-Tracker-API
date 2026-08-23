from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# আপনার অনলাইন PostgreSQL URL এখানে দিন
SQLALCHEMY_DATABASE_URL = "postgresql://postgres.pvdlkwejindlnwxdvklx:[YOUR-PASSWORD]@aws-0-ap-southeast-2.pooler.supabase.com:6543/postgres"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# etapi2026forex
