from flask import request, jsonify
from flask_restx import Resource, Namespace, fields, Api

from database.schemas import TaskCreateSchema, TaskUpdateSchema, TaskSchema, TaskDeleteSchema
from pydantic import ValidationError
from database.service import get_task_list, get_task_id, create_task_db, update_task_db, delete_task_db


api = Api(
    title='Task API',
    version='1.0',
    description='A simple Task API'
)


router_api = Namespace('tasks', description='Operations related to tasks')

task_model = api.model('TaskSchema', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'title': fields.String(readOnly=True, description='The task title'),
    'description': fields.String(readOnly=True, description='The task description')
})

task_create_model = api.model('TaskCreateSchema', {
    'title': fields.String(required=True, description='The task title'),
    'description': fields.String(required=False, description='The task description'),
})

task_update_model = api.model('TaskUpdateSchema', {
    'title': fields.String(required=False, description='The task title'),
    'description': fields.String(required=False, description='The task description')

})

task_delete_model = api.model('TaskDeleteSchema', {
    'message': fields.String(readOnly=True, description='Task deleted successfully'),
})


@router_api.route('/')
class Tasks(Resource):
    @router_api.doc(description="Get list task")
    @router_api.response(200, 'Task list', task_model)
    def get(self):
        """Получение списка задач"""
        tasks = get_task_list()
        task_schemas = [TaskSchema.from_orm(task).dict() for task in tasks]
        return jsonify(task_schemas)

    @router_api.doc(description="Create a new task")
    @router_api.expect(task_create_model)
    @router_api.response(204, 'Task add', task_model)
    def post(self):
        """Создание новой задачи"""
        try:
            data = request.get_json()
            task_data = TaskCreateSchema(**data)
            new_task = create_task_db(task_data)
            task_schemas = TaskSchema.from_orm(new_task).dict()
            return jsonify(task_schemas)
        except ValidationError as e:
            return jsonify(e.errors())


@router_api.route('/<int:id>/')
class Task(Resource):
    @router_api.doc(description="Get task by ID")
    @router_api.response(200, 'Task to id', task_model)
    def get(self, id):
        """Получение конкретной задачи"""
        task = get_task_id(id)
        if task:
            task_schema = TaskSchema.from_orm(task).dict()
            return jsonify(task_schema)
        else:
            return jsonify({'message': 'Task not found'})

    @router_api.doc(description="Update a specific task by ID")
    @router_api.expect(task_update_model)
    @router_api.response(200, 'Task update')
    def put(self, id):
        """Обновление задачи"""
        task = get_task_id(id)
        if not task:
            return jsonify({'message': 'Task not found'})

        try:
            data = request.get_json()
            task_data = TaskUpdateSchema(**data)
            updated_task = update_task_db(task, task_data)
            task_schema = TaskSchema.from_orm(updated_task).dict()
            return jsonify(task_schema)
        except ValidationError as e:
            return jsonify(e.errors())

    @router_api.doc(description="Delete task by ID")
    @router_api.response(204, 'Task deleted', task_delete_model)
    def delete(self, id):
        """Удаление задачи"""
        task = get_task_id(id)
        if task:
            delete_task_db(task)
            return jsonify({'message': 'Task deleted successfully'})
        else:
            return jsonify({'message': 'Task not found'})
