from sqlalchemy.orm import DeclarativeBase
from config.config import DATABASE_URL, TEST_DATABASE_URL


class Base(DeclarativeBase):
    pass


class BaseWork:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL


class BaseTest:
    SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URL
    TESTING = True
