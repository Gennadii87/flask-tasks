from flask_restx import fields
from flask_restx import Api

api = Api(
    title='Task API',
    version='1.0',
    description='A simple Task API',
    doc='/swagger/',
)

TaskSchemaRestx = {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'title': fields.String(readOnly=True, description='The task title', pattern='Task'),
    'description': fields.String(readOnly=True, description='The task description', pattern='Description'),
    'created_at': fields.DateTime(description='The task creation time'),
    'updated_at': fields.DateTime(description='The task update time')
}

TaskCreateSchemaRestx = {
    'title': fields.String(required=True, description='The task title', pattern='New Task'),
    'description': fields.String(required=False, description='The task description', pattern='New Description'),
}

TaskUpdateSchemaRestx = {
    'title': fields.String(required=False, description='The task title', pattern='Update Task'),
    'description': fields.String(required=False, description='The task description', pattern='Update Description')

}

TaskDeleteRestx = {
    'id': fields.Integer(required=True, description='The task ID'),
    'title': fields.String(required=True, description='The task title'),
    'delete_at': fields.DateTime(description='The deletion timestamp')
}


task_model_remove = api.model('TaskRemove', TaskDeleteRestx)

TaskDelete = {
    'message': fields.String(readOnly=True, description='Task deleted successfully'),
    'task': fields.Nested(task_model_remove)
}
