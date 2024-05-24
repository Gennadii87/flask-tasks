import pytest
from database.models import db, Task
from config.config import ConfigApp
from database.database import BaseTest
from routers.router import router_api, api

app = ConfigApp(BaseTest, db).get_app()
api.init_app(app)
api.add_namespace(router_api)


@pytest.fixture
def app_test():
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app


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
    yield db
    db.session.rollback()
    db.drop_all()
