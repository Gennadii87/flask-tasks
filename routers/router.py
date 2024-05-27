import routers.schemas_api as sch
from flask import request, make_response
from flask_restx import Resource, Namespace

from database.schemas import TaskCreateSchema, TaskUpdateSchema, TaskSchema, TaskDeleteSchema
from database.service import get_task_list, get_task_id, create_task_db, update_task_db, delete_task_db
from pydantic import ValidationError

api = sch.api

router_api = Namespace('tasks', description='Operations related to tasks')

task_model = api.model('TaskSchema', sch.TaskSchemaRestx)

task_create_model = api.model('TaskCreate', sch.TaskCreateSchemaRestx)

task_update_model = api.model('TaskUpdate', sch.TaskUpdateSchemaRestx)

task_delete_model = api.model('TaskDelete', sch.TaskDelete)


@router_api.route('/')
class Tasks(Resource):
    @router_api.doc(
        description="Get list task",
        params={'title': 'The task title', 'description': 'The task description'},
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

    @router_api.doc(description="Create a new task")
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
    @router_api.doc(description="Get task by ID")
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

    @router_api.doc(description="Update a specific task by ID", params={'id': 'Task ID'})
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

    @router_api.doc(description="Delete task by ID")
    @router_api.response(204, 'Task deleted', task_delete_model)
    def delete(self, *args, **kwargs):
        """Удаление задачи"""
        task = get_task_id(*args, **kwargs)
        if task:
            task_data = TaskDeleteSchema.to_dict(task)
            task_name = delete_task_db(task)
            return {'message': f'Task `{task_name.title}` deleted successfully', "task": task_data}, 200
        else:
            return {'message': 'Task not found'}, 404
