from flask import request, make_response
from flask_restx import Resource, Namespace, fields, Api
from database.schemas import TaskCreateSchema, TaskUpdateSchema, TaskSchema, TaskDeleteSchema
from pydantic import ValidationError
from database.service import get_task_list, get_task_id, create_task_db, update_task_db, delete_task_db


api = Api(
    title='Task API',
    version='1.0',
    description='A simple Task API',
    doc='/swagger/',
)


router_api = Namespace('tasks', description='Operations related to tasks')

task_model = api.model('TaskSchema', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'title': fields.String(readOnly=True, description='The task title', pattern='Task'),
    'description': fields.String(readOnly=True, description='The task description', pattern='Description'),
    'created_at': fields.DateTime(description='The task creation time'),
    'updated_at': fields.DateTime(description='The task update time')
})

task_create_model = api.model('TaskCreateSchema', {
    'title': fields.String(required=True, description='The task title', pattern='New Task'),
    'description': fields.String(required=False, description='The task description', pattern='New Description'),
})

task_update_model = api.model('TaskUpdateSchema', {
    'title': fields.String(required=False, description='The task title', pattern='Update Task'),
    'description': fields.String(required=False, description='The task description', pattern='Update Description')

})

task_delete_model = api.model('TaskDeleteSchema', {
    'message': fields.String(readOnly=True, description='Task deleted successfully'),
})


@router_api.route('/')
class Tasks(Resource):
    @router_api.doc(
        description="Get list task",
        params={'title': 'The task title', 'description': 'The task description'},
        order=1
    )
    @router_api.response(200, 'Task list', task_model)
    def get(self):
        """Получение списка задач"""
        title_filter = request.args.get('title')
        description_filter = request.args.get('description')
        tasks = get_task_list(title_filter, description_filter)
        task_schemas = [TaskSchema.from_orm(task).to_dict() for task in tasks]
        response = make_response(task_schemas)
        response.status_code = 200
        return response

    @router_api.doc(description="Create a new task", order=3)
    @router_api.expect(task_create_model)
    @router_api.response(201, 'Task add', task_model)
    def post(self):
        """Создание новой задачи"""
        try:
            data = request.get_json()
            task_data = TaskCreateSchema(**data)
            new_task = create_task_db(task_data)
            task_schemas = TaskSchema.from_orm(new_task).to_dict()
            response = make_response(task_schemas)
            response.status_code = 201
            return response
        except ValidationError as e:
            return e.errors(), 400


@router_api.route('/<int:id>/')
class Task(Resource):
    @router_api.doc(description="Get task by ID", order=2)
    @router_api.response(200, 'Task to id', task_model)
    def get(self, *args, **kwargs):
        """Получение конкретной задачи"""
        task = get_task_id(*args, **kwargs)
        if task:
            task_schema = TaskSchema.from_orm(task).to_dict()
            response = make_response(task_schema)
            response.status_code = 200
            return response
        else:
            return {'message': 'Task not found'}, 404

    @router_api.doc(description="Update a specific task by ID", order=4, params={'id': 'Task ID'})
    @router_api.expect(task_update_model)
    @router_api.response(200, 'Task update', task_model)
    def put(self, *args, **kwargs):
        """Обновление задачи"""
        task = get_task_id(*args, **kwargs)
        if not task:
            return {'message': 'Task not found'}, 404

        try:
            data = request.get_json()
            task_data = TaskUpdateSchema(**data)
            updated_task = update_task_db(task, task_data)
            task_schema = TaskSchema.from_orm(updated_task).to_dict()
            response = make_response(task_schema)
            response.status_code = 200
            return response
        except ValidationError as e:
            return e.errors(), 400

    @router_api.doc(description="Delete task by ID", order=5)
    @router_api.response(204, 'Task deleted', task_delete_model)
    def delete(self, *args, **kwargs):
        """Удаление задачи"""
        task = get_task_id(*args, **kwargs)
        if task:
            task_name = delete_task_db(task)
            return {'message': f'Task `{task_name.title}` deleted successfully'}, 200
        else:
            return {'message': 'Task not found'}, 404
