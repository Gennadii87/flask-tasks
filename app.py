import os
from flask_migrate import Migrate
from config.config import ConfigApp, LoggerConfig
from database.database import BaseWork
from database.models import db
from routers.router import router_api, api, router_api_test

app_config = ConfigApp(BaseWork, db)
app = app_config.get_app()

migrate = Migrate(app, db)

log_config = LoggerConfig('INFO')


def print_config(app_):
    """Печать конфигурации приложения в режиме отладки."""
    # if app.config['DEBUG']:
    for key, value in app_.config.items():
        print(f"{key}: {value}")


# создавать и применять миграции в ручную
# flask db init, flask db migrate -m "Initial migration",  flask db upgrade
with app.app_context():
    # db.drop_all()
    db.create_all()


api.init_app(app)
api.add_namespace(router_api)
api.add_namespace(router_api_test)

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        print_config(app)
    app.run(port=4000)
