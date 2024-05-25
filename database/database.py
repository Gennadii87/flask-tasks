from sqlalchemy.orm import DeclarativeBase
from config.config import DATABASE_URL, TEST_DATABASE_URL


class Base(DeclarativeBase):
    pass


class DataBaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'echo_pool': True,
        'pool_pre_ping': True
    }
    SQLALCHEMY_ECHO = False
    DEBUG = True


class BaseWork(DataBaseConfig):
    SQLALCHEMY_DATABASE_URI = DATABASE_URL


class BaseTest(DataBaseConfig):
    SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URL
    TESTING = True
