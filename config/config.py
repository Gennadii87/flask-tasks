import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL = 'sqlite:///sqlite.db'

TEST_DATABASE_URL = 'sqlite:///test.db'


class ConfigApp:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self, cls_config=None, db=None):
        self.app = Flask(__name__)
        self.app.config.from_object(cls_config)
        db.init_app(self.app)

    def get_app(self):
        return self.app
