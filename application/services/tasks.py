import os
import logging
import pickle
import traceback

from sqlalchemy import func

from application import app, db
from application.config import CACHE_FOLDER
from application.models import Task, TaskStatus


logger = logging.getLogger(__name__)


class TasksService:
    _results: dict[str, any] = {}

    @classmethod
    def create(cls, func, *args) -> tuple:
        task = Task(TaskStatus.RUNNING)
        with open(os.path.join(CACHE_FOLDER, task.task_id), 'bw') as fh:
            pickle.dump([func, args], fh)
        db.session.add(task)
        db.session.commit()
        return task.task_id, task.status

    @classmethod
    def execute(cls, task: Task):
        filename = os.path.join(CACHE_FOLDER, task.task_id)
        try:
            func, args = pickle.load(open(filename, 'br'))
            result = func(*args)
            cls._results[task.task_id] = result
            task.status = TaskStatus.DONE
        except Exception as ex:
            print(ex)
            traceback.print_exc()
            task.status = TaskStatus.ERROR
            logger.error(f"Error until process task: {task.task_id}")
        finally:
            os.remove(filename)
            db.session.add(task)
            db.session.commit()

    @classmethod
    def get_status(cls, task_id: str) -> TaskStatus | None:
        task = Task.query.filter(Task.task_id==task_id).one()
        if task is not None:
            return task.status

    @classmethod
    def get_result(cls, task_id: str) -> tuple:
        status = cls.get_status(task_id)
        data = None
        if status == TaskStatus.DONE:
            data = cls._results.pop(task_id, None)
        return status, data

    @classmethod
    def get_tasks(cls, status: TaskStatus) -> list[Task]:
        return list(Task.query.filter(Task.status==status).all())

    @classmethod
    def get_summary(cls):
        distribution = db.session.query(Task.status, func.count(Task.id)).group_by(Task.status).all()

        return {
            'total': Task.query.count(),
            'distribution': distribution,
            'tasks': list(Task.query.all())
        }

    @classmethod
    def cleanup(cls):
        db.session.query(Task).delete()
        db.session.commit()
