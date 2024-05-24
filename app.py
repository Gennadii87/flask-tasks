from flask_migrate import Migrate
from config.config import ConfigApp
from database.database import BaseWork
from database.models import db
from routers.router import router_api, api


app_config = ConfigApp(BaseWork, db)
app = app_config.get_app()
migrate = Migrate(app, db)

# если убрать, создавать и применять миграции в ручную,
# flask db init, flask db migrate -m "Initial migration",  flask db upgrade
with app.app_context():
    db.create_all()


api.init_app(app)
api.add_namespace(router_api)

if __name__ == '__main__':
    app.run(debug=True, port=4000)
