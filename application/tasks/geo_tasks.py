from application import app
from application.services.tasks import TasksService, TaskStatus


def geo_tasks():
    with app.app_context():
        for task in TasksService.get_tasks(status=TaskStatus.RUNNING):
            TasksService.execute(task)
