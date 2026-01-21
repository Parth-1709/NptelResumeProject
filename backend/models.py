from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    role = Column(String, default="user") # "admin" or "user"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    # We can link to User if we want, or just store email for loose coupling/simplicity
    user_email = Column(String, index=True, nullable=True) 
    final_score = Column(Integer)
    # For simple list storage, we can use JSON if the DB supports it, or just a string representation
    # Postgres supports JSON, but ensuring compat. String is safest for quick MVP.
    missing_skills = Column(String) # Stored as comma-separated string or JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
