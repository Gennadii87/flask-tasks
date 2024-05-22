import pytest
from app import app
from config import DATABASE_URL
from database.models import db, Task


@pytest.fixture
def app_test():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield


@pytest.fixture
def client(app_test):
    return app.test_client()


@pytest.fixture
def init_database():
    task1 = Task(title="Task 1", description="Description 1")
    task2 = Task(title="Task 2", description="Description 2")
    db.session.add(task1)
    db.session.add(task2)
    db.session.commit()
    yield db
    db.session.rollback()
    db.drop_all()


def test_get_tasks(client, init_database):
    response = client.get('/tasks/')
    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) == 2
    assert tasks[0]['title'] == 'Task 1'
    assert tasks[1]['title'] == 'Task 2'


def test_get_task(client, init_database):
    response = client.get('/tasks/1/')
    assert response.status_code == 200
    task = response.get_json()
    assert task['title'] == 'Task 1'
    assert 'created_at' in task
    assert 'updated_at' in task


def test_get_task_not_found(client):
    response = client.get('/tasks/999/')
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Task not found'


def test_create_task(client):
    new_task = {"title": "New Task", "description": "New Description"}
    response = client.post('/tasks/', json=new_task)
    assert response.status_code == 201
    task = response.get_json()
    assert task['title'] == 'New Task'
    assert 'created_at' in task
    assert 'updated_at' in task


def test_create_task_validation_error(client):
    invalid_task = {"title": ""}
    response = client.post('/tasks/', json=invalid_task)
    assert response.status_code == 400


def test_update_task(client, init_database):
    update_data = {"title": "Updated Task", "description": "Updated Description"}
    response = client.put('/tasks/1/', json=update_data)
    assert response.status_code == 200
    task = response.get_json()
    assert task['title'] == 'Updated Task'
    assert 'created_at' in task
    assert 'updated_at' in task
    assert task['description'] == 'Updated Description'


def test_update_task_not_found(client):
    update_data = {"title": "Updated Task"}
    response = client.put('/tasks/999/', json=update_data)
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Task not found'


def test_delete_task(client, init_database):
    response = client.delete('/tasks/1/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Task deleted successfully'
    response = client.get('/tasks/1/')
    assert response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete('/tasks/999/')
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Task not found'
