from backend.app.config import settings

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_task(client, test_task):
    response = client.post(f"{settings.API_PREFIX}/tasks", json=test_task)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == test_task["title"]
    assert "id" in data
    return data["id"]

def test_read_tasks(client):
    response = client.get(f"{settings.API_PREFIX}/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_task(client, test_task):
    # Create a task first
    task_id = test_create_task(client, test_task)
    
    # Test getting the task
    response = client.get(f"{settings.API_PREFIX}/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == test_task["title"]
    # Try to get a task with a non-existent ID
    response = client.get("/api/tasks/9999")
    assert response.status_code == 404