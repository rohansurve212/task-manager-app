import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.models import Task
from backend.app.database import Base

# Create an in-memory SQLite database for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        
    # Drop tables after test
    Base.metadata.drop_all(bind=engine)

def test_create_task(db_session):
    # Create a new task
    task = Task(
        title="Test Task",
        description="This is a test task",
        is_completed=False
    )
    
    db_session.add(task)
    db_session.commit()
    
    # Refresh the task to get the values from the database
    db_session.refresh(task)
    
    # Check if task was created correctly
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.is_completed is False
    assert task.created_at is not None
    assert task.updated_at is None

def test_update_task(db_session):
    # Create a new task
    task = Task(
        title="Original Title",
        description="Original Description",
        is_completed=False
    )
    
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    
    # Update the task
    task.title = "Updated Title"
    task.is_completed = True
    db_session.commit()
    db_session.refresh(task)
    
    # Check if task was updated correctly
    assert task.title == "Updated Title"
    assert task.description == "Original Description"  # Shouldn't change
    assert task.is_completed is True

def test_delete_task(db_session):
    # Create a new task
    task = Task(
        title="Task to delete",
        description="This task will be deleted",
        is_completed=False
    )
    
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    
    # Get the task id
    task_id = task.id
    
    # Delete the task
    db_session.delete(task)
    db_session.commit()
    
    # Try to fetch the deleted task
    deleted_task = db_session.query(Task).filter(Task.id == task_id).first()
    
    # Check if task was deleted
    assert deleted_task is None