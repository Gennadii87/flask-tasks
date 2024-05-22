from config import DATABASE_URL
from flask import Flask
from flask_migrate import Migrate
from database.models import db
from routers.router import router

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# если убрать, создавать и применять миграции в ручную,
# flask db init, flask db migrate -m "Initial migration",  flask db upgrade
with app.app_context():
    db.create_all()

app.register_blueprint(router)

if __name__ == '__main__':
    app.run(debug=True, port=4000)
