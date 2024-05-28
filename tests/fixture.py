import pytest
from database.models import db, Task
from config.config import ConfigApp, LoggerConfig
from database.database import BaseTest
from routers.router import api

app = ConfigApp(BaseTest, db).get_app()
api.init_app(app)
log_config = LoggerConfig('INFO')


@pytest.fixture(scope='session')
def app_test():
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app_test):
    return app_test.test_client()


@pytest.fixture
def init_database():
    task1 = Task(title="Task 1", description="Description 1")
    task2 = Task(title="Task 2", description="Description 2")
    db.session.add(task1)
    db.session.add(task2)
    db.session.commit()
