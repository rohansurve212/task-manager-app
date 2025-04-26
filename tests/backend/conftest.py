# In tests/backend/conftest.py or a testing utilities file
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.database import Base
from backend.app.config import settings

# Override the database URL for testing
@pytest.fixture(scope="session")
def test_db_engine():
    # Use an in-memory SQLite database for testing
    TEST_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_db_session(test_db_engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()