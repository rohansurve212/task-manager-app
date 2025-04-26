import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.database import Base, get_db
from backend.app.main import app
from fastapi.testclient import TestClient

# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    # Create engine with in-memory database
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Drop all tables after tests are done
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(engine):
    # Create a new SessionLocal
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create a new session for the test
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):
    # Override the get_db dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Override the get_db dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create a TestClient with the overridden dependency
    with TestClient(app) as client:
        yield client
    
    # Remove the override after testing
    app.dependency_overrides = {}

# Test data fixture
@pytest.fixture
def test_task():
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "is_completed": False
    }