from database.models import Task, db


def get_task_list():
    """Get all tasks"""
    tasks = Task.query.all()
    return tasks


def get_task_id(id):
    """Get task to id"""
    task = Task.query.filter(Task.id == id).first()
    return task


def create_task_db(task_data):
    """Create task"""
    new_task = Task(title=task_data.title, description=task_data.description)
    db.session.add(new_task)
    db.session.commit()
    return new_task


def update_task_db(task, task_data):
    """Update task"""
    if task_data.title:
        task.title = task_data.title
    if task_data.description:
        task.description = task_data.description
    db.session.commit()
    return task


def delete_task_db(task):
    """Delete task"""
    if task:
        db.session.delete(task)
        db.session.commit()
        return task