from database import engine, Base
from models import User, Evaluation
import sys

def init_db():
    print("Connecting to database...")
    try:
        # Import models to ensure they are registered with Base
        print(f"Registered models: {list(Base.metadata.tables.keys())}")
        
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_db()
