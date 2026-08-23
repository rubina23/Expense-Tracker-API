from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# PostgreSQL URL from Supabase
SQLALCHEMY_DATABASE_URL = "postgresql://postgres.pvdlkwejindlnwxdvklx:etapi2026forex@aws-0-ap-southeast-2.pooler.supabase.com:5432/postgres"

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
