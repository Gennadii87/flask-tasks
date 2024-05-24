import pytest
from app import app
from config.config import DATABASE_URL
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
