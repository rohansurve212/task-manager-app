import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.database import get_db

# Override the database dependency
@pytest.fixture
def client(test_db_session):
    def override_get_db():
        try:
            yield test_db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    
    # Reset the override after the test
    app.dependency_overrides = {}

# Use the client fixture in your tests
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

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
    response = client.post("/tasks", json=test_task)
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
    response = client.get("/tasks")
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
        
    response = client.get("/tasks/{task_id}")
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
    
    response = client.put("/tasks/{task_id}", json=update_data)
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
    
    response = client.delete("/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get("/tasks/{task_id}")
    assert response.status_code == 404

def test_read_nonexistent_task():
    # Try to get a task with a non-existent ID
    response = client.get("/tasks/9999")
    assert response.status_code == 404