import enum
import uuid

from application import db


class TaskStatus(enum.Enum):
    RUNNING = 'running'
    DONE = 'done'
    ERROR = 'error'


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(33), nullable=False)
    status = db.Column(db.Enum(TaskStatus), nullable=False)

    def __init__(self, status: TaskStatus):
        self.task_id = uuid.uuid4().hex
        self.status = status

    def __repr__(self):
        return "<Task id={task_id} with {status}>".format(**self.__dict__)
