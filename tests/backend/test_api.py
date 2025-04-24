import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.app.database import Base, get_db
from backend.app.config import settings

# Create an in-memory SQLite database for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Override the get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create a test client
client = TestClient(app)

# Test data
test_task = {
    "title": "Test Task",
    "description": "This is a test task",
    "is_completed": False
}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_task():
    response = client.post(f"{settings.API_PREFIX}/tasks", json=test_task)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == test_task["title"]
    assert data["description"] == test_task["description"]
    assert data["is_completed"] == test_task["is_completed"]
    assert "id" in data
    assert "created_at" in data
    
    # Save the task ID for later tests
    test_task["id"] = data["id"]
    return data["id"]

def test_read_tasks():
    response = client.get(f"{settings.API_PREFIX}/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # If we created a task earlier, check if it's in the list
    if "id" in test_task:
        task_ids = [task["id"] for task in response.json()]
        assert test_task["id"] in task_ids

def test_read_task():
    # First create a task if we don't have one
    if "id" not in test_task:
        task_id = test_create_task()
    else:
        task_id = test_task["id"]
        
    response = client.get(f"{settings.API_PREFIX}/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == test_task["title"]
    assert data["description"] == test_task["description"]

def test_update_task():
    # First create a task if we don't have one
    if "id" not in test_task:
        task_id = test_create_task()
    else:
        task_id = test_task["id"]
    
    update_data = {
        "title": "Updated Task",
        "is_completed": True
    }
    
    response = client.put(f"{settings.API_PREFIX}/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == update_data["title"]
    assert data["description"] == test_task["description"]
    assert data["is_completed"] == update_data["is_completed"]

def test_delete_task():
    # First create a task if we don't have one
    if "id" not in test_task:
        task_id = test_create_task()
    else:
        task_id = test_task["id"]
    
    response = client.delete(f"{settings.API_PREFIX}/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get(f"{settings.API_PREFIX}/tasks/{task_id}")
    assert response.status_code == 404

def test_read_nonexistent_task():
    # Try to get a task with a non-existent ID
    response = client.get(f"{settings.API_PREFIX}/tasks/9999")
    assert response.status_code == 404