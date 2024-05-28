from fixture import client, init_database, app_test
from routers.router import url_prefix

url = url_prefix
test = app_test


def test_get_tasks(client, init_database):
    response = client.get(f'{url}/')
    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) == 2
    assert tasks[0]['title'] == 'Task 1'
    assert tasks[1]['title'] == 'Task 2'


def test_get_task_id(client, init_database):
    response = client.get(f'{url}/1/')
    assert response.status_code == 200
    task = response.get_json()
    assert task['title'] == 'Task 1'
    assert 'created_at' in task
    assert 'updated_at' in task


def test_get_task_not_found(client):
    response = client.get(f'{url}/999/')
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Task not found'


def test_create_task(client):
    new_task = {"title": "New Task", "description": "New Description"}
    response = client.post(f'{url}/', json=new_task)
    assert response.status_code == 201
    task = response.get_json()
    assert task['title'] == 'New Task'
    assert 'created_at' in task
    assert 'updated_at' in task


def test_create_task_validation_error(client):
    invalid_task = {"title": ""}
    response = client.post(f'{url}/', json=invalid_task)
    assert response.status_code == 400


def test_update_task(client, init_database):
    update_data = {"title": "Updated Task", "description": "Updated Description"}
    response = client.put(f'{url}/1/', json=update_data)
    assert response.status_code == 200
    task = response.get_json()
    assert task['title'] == 'Updated Task'
    assert 'created_at' in task
    assert 'updated_at' in task
    assert task['description'] == 'Updated Description'


def test_update_task_not_found(client):
    update_data = {"title": "Updated Task"}
    response = client.put(f'{url}/999/', json=update_data)
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Task not found'


def test_delete_task(client, init_database):
    response = client.delete(f'{url}/1/')
    assert response.status_code == 200
    data = response.get_json()
    title = data.get('task', {}).get("title")
    assert data['message'] == f'Task `{title}` deleted successfully'
    response = client.get('/tasks/1/')
    assert response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete(f'{url}/999/')
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Task not found'
