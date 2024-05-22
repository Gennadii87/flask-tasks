from database.models import Task, db
from database.schemas import TaskCreateSchema, TaskUpdateSchema, TaskSchema
from pydantic import ValidationError
from flask import request, jsonify, Blueprint


router = Blueprint('router', __name__)


# Получение списка задач
@router.route('/tasks/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_schemas = [TaskSchema.from_orm(task).dict() for task in tasks]
    return jsonify(task_schemas), 200


# Получение конкретной задачи
@router.route('/tasks/<int:id>/', methods=['GET'])
def get_task(id: int):
    task = Task.query.filter(Task.id == id).first()
    if task:
        task_schema = TaskSchema.from_orm(task).dict()
        return jsonify(task_schema), 200
    else:
        return jsonify({'message': 'Task not found'}), 404


# Создание задачи
@router.route('/tasks/', methods=['POST'])
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


# Обновление задачи
@router.route('/tasks/<int:id>/', methods=['PUT'])
def update_task(id: int):
    task = Task.query.filter(Task.id == id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
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


# Удаление задачи
@router.route('/tasks/<int:id>/', methods=['DELETE'])
def delete_task(id):
    task = Task.query.filter(Task.id == id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404
