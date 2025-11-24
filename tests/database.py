# tests/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base 

SQLALCHEMY_TEST_URL = "sqlite:///./test.db" 

engine_test = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={ "check_same_thread": False },
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test,
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
