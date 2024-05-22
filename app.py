from config import DATABASE_URL
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Task
from schemas import TaskCreateSchema, TaskUpdateSchema, TaskSchema
from pydantic import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL


db.init_app(app)
migrate = Migrate(app, db)


@app.route('/tasks/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_schemas = [TaskSchema.from_orm(task).dict() for task in tasks]
    return jsonify(task_schemas), 200


@app.route('/task/<int:id>/', methods=['GET'])
def get_task(id: int):
    task = Task.query.filter(Task.id == id).first()
    if task:
        task_schema = TaskSchema.from_orm(task).dict()
        return jsonify(task_schema), 200
    else:
        return jsonify({'message': 'Task not found'}), 404


@app.route('/tasks/', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        task_data = TaskCreateSchema(**data)
        new_task = Task(title=task_data.title, description=task_data.description)
        db.session.add(new_task)
        db.session.commit()
        task_schemas = TaskSchema.from_orm(new_task).dict()
        return jsonify(task_schemas), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400


@app.route('/task/<int:id>', methods=['PUT'])
def update_task(id: int):
    task = Task.query.filter(Task.id == id).first()
    try:
        data = request.get_json()
        task_data = TaskUpdateSchema(**data)
        if task_data.title:
            task.title = task_data.title
        if task_data.description:
            task.description = task_data.description
        db.session.commit()
        task_schema = TaskSchema.from_orm(task).dict()
        return jsonify(task_schema), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400


@app.route('/task/<int:id>/', methods=['DELETE'])
def delete_task(id):
    task = Task.query.filter(Task.id == id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
