from flask_restx import fields
from flask_restx import Api

authorizations = {
    "Basic": {
        "type": "basic",
        "flow": "password",
    },
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    },
}

api = Api(
    title='Task API',
    version='1.0',
    description='A simple Task API',
    doc='/swagger/',
    authorizations=authorizations
)

TaskSchemaRestx = {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'title': fields.String(readOnly=True, description='The task title', default='Task'),
    'description': fields.String(readOnly=True, description='The task description', default='Description'),
    'created_at': fields.DateTime(description='The task creation time'),
    'updated_at': fields.DateTime(description='The task update time')
}

TaskCreateSchemaRestx = {
    'title': fields.String(required=True, description='The task title', default='New Task'),
    'description': fields.String(required=False, description='The task description', default='New Description'),
}

TaskUpdateSchemaRestx = {
    'title': fields.String(required=False, description='The task title', default='Update Task'),
    'description': fields.String(required=False, description='The task description', default='Update Description')

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
