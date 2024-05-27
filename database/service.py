from database.models import Task, db
from sqlalchemy import select


def get_task_list(title_filter=None, description_filter=None):
    """Get tasks list"""

    stmt = select(Task).order_by(Task.id)

    if title_filter:
        stmt = stmt.where(Task.title.like(f"%{title_filter}%"))

    if description_filter:
        stmt = stmt.where(Task.description.like(f"%{description_filter}%"))

    tasks = db.session.execute(stmt).scalars().all()

    return tasks


def get_task_id(id):
    """Get task to id"""
    task = db.session.execute(db.select(Task).filter_by(id=id)).scalar_one_or_none()
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
