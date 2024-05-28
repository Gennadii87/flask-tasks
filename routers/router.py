import subprocess
import re
import json

import routers.schemas_api as sch
from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace

from database.schemas import TaskCreateSchema, TaskUpdateSchema, TaskSchema, TaskDeleteSchema
from database.service import get_task_list, get_task_id, create_task_db, update_task_db, delete_task_db
from pydantic import ValidationError

api = sch.api
url_prefix = '/api/v1/tasks'

router_api = Namespace(name='tasks', description='Operations related to tasks')
router_api_test = Namespace(name='tasks-test', description='Test api')

api.add_namespace(router_api, path=url_prefix)

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


@router_api_test.route('/')
class RunTests(Resource):
    @api.doc(description="Run tests and return the results",
             params={'test_name': 'example `test_get_tasks`'}
             )
    @api.param(name='count', type='int', description='count test (integer)')
    def get(self):
        """Запуск тестов и получение результатов"""
        test_name = request.args.get('test_name')
        count = request.args.get('count', 1, type=int)
        test_results = []

        if test_name:
            pytest_command = ['pytest',
                              f'tests/test_task.py::{test_name}',
                              '--maxfail=10',
                              '-q',
                              f'--count={count}'
                              ]
            total_tests = 1
            passed_tests = 0
        else:
            pytest_command = ['pytest',
                              '--maxfail=10',
                              '-q', f'--count={count}'
                              ]
            total_tests = 9
            passed_tests = 0

        result = subprocess.run(pytest_command, capture_output=True, text=True)
        output_lines = result.stdout.strip().split('\n')

        error_info_pattern = re.compile(r"FAILED\s(.*?)\s-\sassert\s(.*)\s==\s(.*)$")

        for line in output_lines:
            if 'FAILED' in line:
                match = error_info_pattern.search(line)
                if match:
                    match = line.split()
                    test_name = match[1]
                    test_result = 'FAILED'
                    info = f"ERROR: {' '.join(match[3:8])}"
                    passed_tests += 1
                    test_progress = f"{min((passed_tests / total_tests) * 100, 100):.0f}%"
                    test_results.append({
                        'test': test_name.split("::")[-1],
                        'result': test_result,
                        'progress': test_progress,
                        'info': info
                    })
            elif 'PASSED' in line:
                parts = line.split()
                test_name = parts[0]
                test_result = 'PASSED'
                passed_tests += 1
                test_progress = f"{min((passed_tests / total_tests) * 100, 100):.0f}%"
                test_results.append({
                    'test': test_name.split("::")[-1],
                    'result': test_result,
                    'progress': test_progress,
                    'info': 'OK'
                })

        summary = output_lines[-1] if output_lines else "No tests found"
        failed_tests_count = sum(1 for result in test_results if result['result'] == 'FAILED')

        response = {
            'test_results': test_results,
            'summary': summary,
        }

        if failed_tests_count > 0:
            response['FAILED'] = f"{failed_tests_count} TEST"

        with open("response.json", "w", encoding="utf-8") as file:
            json.dump(response, file, indent=4, ensure_ascii=False)

        return jsonify(response)
