from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Use the environment variable or a default (which will fail if not set, prompting user)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
# connect_args={"check_same_thread": False} is needed only for SQLite. 
# For Postgres, we don't need it.
if not SQLALCHEMY_DATABASE_URL:
    print("WARNING: DATABASE_URL not found in .env. Please set it.")
    # Fallback to a clear error or a dummy sqlite for dev if really needed, 
    # but strictly requested Postgres.
    SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/ats_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
