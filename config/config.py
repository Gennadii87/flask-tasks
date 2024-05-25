import os
import logging
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


DATABASE_URL = {
    'sql_1': f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    'sql_2': 'sqlite:///sqlite.db'
}

TEST_DATABASE_URL = {
    'sql_1': 'sqlite:///test.db'
}


# class ConfigApp:
#     def __init__(self, cls_config=None, db=None):
#         self.app = Flask(__name__)
#         self.app.config.from_object(cls_config)
#         db.init_app(self.app)


class ConfigApp:
    def __init__(self, cls_config=None, db=None):
        self.app = Flask(__name__)

        if not hasattr(cls_config, 'SQLALCHEMY_DATABASE_URI'):
            raise AttributeError("Configuration must contain SQLALCHEMY_DATABASE_URI")

        for key in dir(cls_config):
            if not key.startswith('__'):
                self.app.config[key] = getattr(cls_config, key)

        sql_1 = cls_config.SQLALCHEMY_DATABASE_URI.get('sql_1')
        sql_2 = cls_config.SQLALCHEMY_DATABASE_URI.get('sql_2')

        try:
            engine = create_engine(sql_1)
            with engine.connect():
                pass
            self.app.config['SQLALCHEMY_DATABASE_URI'] = sql_1
        except OperationalError:
            print("Не удалось подключиться к базе данных MySQL")
            if sql_2:
                print("Переключение на базу данных SQLite.")
                self.app.config['SQLALCHEMY_DATABASE_URI'] = sql_2
            else:
                raise RuntimeError("Резервная база данных SQLite не настроена.")
        self.app.config['DEBUG'] = cls_config.DEBUG
        db.init_app(self.app)

    def get_app(self):
        return self.app


class LoggerConfig:
    _instance = None
    LOG_LEVELS = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }

    def __new__(cls, level, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoggerConfig, cls).__new__(cls, *args, **kwargs)
            # Устанавливаем уровень для библиотеки Werkzeug
            logging.getLogger('werkzeug').setLevel(logging.INFO)

            # Создаем объект для SQLAlchemy
            cls._instance.logger = logging.getLogger('sqlalchemy.engine')
            cls._instance.logger.setLevel(level)  # Устанавливаем уровень

            # Создаем форматер для добавления даты и времени к сообщениям
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            # Создаем обработчик для записи в файл
            handler = logging.FileHandler('log_sql.txt', encoding='utf-8')
            handler.setLevel(level)  # Устанавливаем уровень для обработчика
            handler.setFormatter(formatter)

            # Добавляем обработчик к объекту SQLAlchemy
            cls._instance.logger.addHandler(handler)

        return cls._instance
