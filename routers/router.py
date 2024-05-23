# from database.service import get_task_list, get_task_id, create_task_db, update_task_db, delete_task_db
# from database.schemas import TaskCreateSchema, TaskUpdateSchema, TaskSchema
# from pydantic import ValidationError
# from flask import request, jsonify, Blueprint
#
#
# router = Blueprint('router', __name__)
#
#
# # Получение списка задач
# @router.route('/tasks/', methods=['GET'])
# def get_tasks():
#     tasks = get_task_list()
#     task_schemas = [TaskSchema.from_orm(task).dict() for task in tasks]
#     return jsonify(task_schemas), 200
#
#
# # Получение конкретной задачи
# @router.route('/tasks/<int:id>/', methods=['GET'])
# def get_task(id: int):
#     task = get_task_id(id)
#     if task:
#         task_schema = TaskSchema.from_orm(task).dict()
#         return jsonify(task_schema), 200
#     else:
#         return jsonify({'message': 'Task not found'}), 404
#
#
# # Создание задачи
# @router.route('/tasks/', methods=['POST'])
# def create_task():
#     try:
#         data = request.get_json()
#         task_data = TaskCreateSchema(**data)
#         new_task = create_task_db(task_data)
#         task_schemas = TaskSchema.from_orm(new_task).dict()
#         return jsonify(task_schemas), 201
#     except ValidationError as e:
#         return jsonify(e.errors()), 400
#
#
# # Обновление задачи
# @router.route('/tasks/<int:id>/', methods=['PUT'])
# def update_task(id: int):
#     task = get_task_id(id)
#     if not task:
#         return jsonify({'message': 'Task not found'}), 404
#
#     try:
#         data = request.get_json()
#         task_data = TaskUpdateSchema(**data)
#         updated_task = update_task_db(task, task_data)
#         task_schema = TaskSchema.from_orm(updated_task).dict()
#         return jsonify(task_schema), 200
#     except ValidationError as e:
#         return jsonify(e.errors()), 400
#
#
# # Удаление задачи
# @router.route('/tasks/<int:id>/', methods=['DELETE'])
# def delete_task(id):
#     task = get_task_id(id)
#     if task:
#         delete_task_db(task)
#         return jsonify({'message': 'Task deleted successfully'}), 200
#     else:
#         return jsonify({'message': 'Task not found'}), 404

#
# from flask import request, jsonify
# from flask_restx import Resource, Namespace, Api, fields
# from database.service import get_task_list, get_task_id, create_task_db, update_task_db, delete_task_db
# from database.schemas import TaskCreateSchema, TaskUpdateSchema, TaskSchema
# from pydantic import ValidationError
#
# api = Api(
#     title='Task API',
#     version='1.0',
#     description='A simple Task API'
# )
#
# ns = Namespace('tasks', description='Task operations')
#
# task_model = ns.model('TaskSchema', {
#     'id': fields.Integer(readOnly=True, description='The task unique identifier'),
#     'title': fields.String(required=True, description='The task title'),
#     'description': fields.String(required=True, description='The task description')
# })
#
# task_create_model = ns.model('TaskCreate', {
#     'title': fields.String(required=True, description='The task title'),
#     'description': fields.String(required=True, description='The task description')
# })
#
# task_update_model = ns.model('TaskUpdate', {
#     'title': fields.String(description='The task title'),
#     'description': fields.String(description='The task description')
# })
#
# @ns.route('/')
# class TaskList(Resource):
#     @ns.doc('list_tasks')
#     @ns.marshal_list_with(task_model)
#     def get(self):
#         tasks = get_task_list()
#         task_schemas = [TaskSchema.from_orm(task).dict() for task in tasks]
#         return jsonify(task_schemas), 200
#
#     @ns.doc('create_task')
#     @ns.expect(task_create_model)
#     @ns.marshal_with(task_model, code=201)
#     def post(self):
#         try:
#             data = request.get_json()
#             task_data = TaskCreateSchema(**data)
#             new_task = Task(title=task_data.title, description=task_data.description)
#             db.session.add(new_task)
#             db.session.commit()
#             return TaskSchema.from_orm(new_task).dict(), 201
#         except ValidationError as e:
#             return jsonify(e.errors()), 400
#
# @ns.route('/<int:id>/')
# @ns.response(404, 'Task not found')
# @ns.param('id', 'The task identifier')
# class Task(Resource):
#     @ns.doc('get_task')
#     @ns.marshal_with(task_model)
#     def get(self, id):
#         task = Task.query.filter(Task.id == id).first()
#         if task:
#             return TaskSchema.from_orm(task).dict(), 200
#         else:
#             return {'message': 'Task not found'}, 404
#
#     @ns.doc('update_task')
#     @ns.expect(task_update_model)
#     @ns.marshal_with(task_model)
#     def put(self, id):
#         task = Task.query.filter(Task.id == id).first()
#         if not task:
#             return {'message': 'Task not found'}, 404
#         try:
#             data = request.get_json()
#             task_data = TaskUpdateSchema(**data)
#             if task_data.title:
#                 task.title = task_data.title
#             if task_data.description:
#                 task.description = task_data.description
#             db.session.commit()
#             return TaskSchema.from_orm(task).dict(), 200
#         except ValidationError as e:
#             return jsonify(e.errors()), 400
#
#     @ns.doc('delete_task')
#     @ns.response(204, 'Task deleted')
#     def delete(self, id):
#         task = Task.query.filter(Task.id == id).first()
#         if task:
#             db.session.delete(task)
#             db.session.commit()
#             return {'message': 'Task deleted successfully'}, 204
#         else:
#             return {'message': 'Task not found'}, 404
#
# api.add_namespace(ns)
# from flask import request, jsonify, Blueprint
# from flask_restx import Api, Resource, fields
# from database.service import get_task_list, get_task_id, create_task_db, update_task_db, delete_task_db
# from database.schemas import TaskCreateSchema, TaskUpdateSchema, TaskSchema
# from pydantic import ValidationError
#
#
#
# # Создание Blueprint
# router = Blueprint('router', __name__)
#
# # Создание экземпляра Api
# api = Api(router, version='1.0', title='Task API', description='A simple Task API')
#
# # Пространство имен (Namespace) для задач
# ns = api.namespace('tasks', description='Task operations')
#
# # Определение моделей данных для использования в документации
# task_model = api.model('TaskSchema', {
#     'id': fields.Integer(readOnly=True, description='The task unique identifier'),
#     'title': fields.String(required=True, description='The task title'),
#     'description': fields.String(required=True, description='The task description')
# })
#
# task_create_model = api.model('TaskCreateSchema', {
#     'title': fields.String(required=True, description='The task title'),
#     'description': fields.String(required=True, description='The task description')
# })
#
# task_update_model = api.model('TaskUpdateSchema', {
#     'title': fields.String(description='The task title'),
#     'description': fields.String(description='The task description')
# })
#
# # Ресурсы для обработки запросов
# @ns.route('/')
# class TaskList(Resource):
#     @ns.doc('list_tasks')
#     @ns.marshal_list_with(task_model)
#     def get(self):
#         """Получение списка задач"""
#         tasks = get_task_list()
#         task_schemas = [TaskSchema.from_orm(task).dict() for task in tasks]
#         return jsonify(task_schemas)
#
#     @ns.doc('create_task')
#     @ns.expect(task_create_model)
#     @ns.marshal_with(task_model, code=201)
#     def post(self):
#         """Создание новой задачи"""
#         try:
#             data = request.get_json()
#             task_data = TaskCreateSchema(**data)
#             new_task = create_task_db(task_data)
#             task_schemas = TaskSchema.from_orm(new_task).dict()
#             return jsonify(task_schemas), 201
#         except ValidationError as e:
#             return jsonify(e.errors()), 400
#
# @ns.route('/<int:id>/')
# @ns.response(404, 'Task not found')
# @ns.param('id', 'The task identifier')
# class Task(Resource):
#     @ns.doc('get_task')
#     @ns.marshal_with(task_model)
#     def get(self, id):
#         """Получение конкретной задачи"""
#         task = get_task_id(id)
#         if task:
#             task_schema = TaskSchema.from_orm(task).dict()
#             return jsonify(task_schema), 200
#         else:
#             return jsonify({'message': 'Task not found'}), 404
#
#     @ns.doc('update_task')
#     @ns.expect(task_update_model)
#     @ns.marshal_with(task_model)
#     def put(self, id):
#         """Обновление задачи"""
#         task = get_task_id(id)
#         if not task:
#             return jsonify({'message': 'Task not found'}), 404
#
#         try:
#             data = request.get_json()
#             task_data = TaskUpdateSchema(**data)
#             updated_task = update_task_db(task, task_data)
#             task_schema = TaskSchema.from_orm(updated_task).dict()
#             return jsonify(task_schema), 200
#         except ValidationError as e:
#             return jsonify(e.errors()), 400
#
#     @ns.doc('delete_task')
#     @ns.response(204, 'Task deleted')
#     def delete(self, id):
#         """Удаление задачи"""
#         task = get_task_id(id)
#         if task:
#             delete_task_db(task)
#             return jsonify({'message': 'Task deleted successfully'}), 200
#         else:
#             return jsonify({'message': 'Task not found'}), 404


from flask import request, jsonify
from flask_restx import Resource, Namespace

from database.schemas import TaskCreateSchema, TaskUpdateSchema, TaskSchema
from pydantic import ValidationError
from database.service import get_task_list, get_task_id, create_task_db, update_task_db, delete_task_db
from database.models import Task


router_api = Namespace('tasks', description='Operations related to tasks')


@router_api.route('/')
class Tasks(Resource):
    @router_api.doc(description="Get all tasks")
    def get(self):
        """Get list task"""
        tasks = get_task_list()
        task_schemas = [TaskSchema.from_orm(task).dict() for task in tasks]
        return jsonify(task_schemas)

    @router_api.doc(description="Create a new task")
    @router_api.expect(TaskCreateSchema)
    def post(self):
        """Create a new task"""
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
    @router_api.doc(description="Get a specific task by ID")
    def get(self, id):
        """Get a specific task by ID"""
        task = get_task_id(id)
        if task:
            task_schema = TaskSchema.from_orm(task).dict()
            return jsonify(task_schema)
        else:
            return jsonify({'message': 'Task not found'})

    @router_api.doc(description="Update a specific task by ID")
    @router_api.expect(TaskUpdateSchema)
    def put(self, id):
        """Update a specific task by ID"""
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

    @router_api.doc(description="Delete a specific task by ID")
    def delete(self, id):
        """Delete a specific task by ID"""
        task = get_task_id(id)
        if task:
            delete_task_db(task)
            return jsonify({'message': 'Task deleted successfully'})
        else:
            return jsonify({'message': 'Task not found'})