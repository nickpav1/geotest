import os

from application.tasks import background_tasks

BASE_DIR = os.path.dirname(__file__)
CACHE_FOLDER = os.path.join(BASE_DIR, 'task_cache')


class Config:
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    SQLALCHEMY_DATABASE_URI = "sqlite:///%s/database.sqlite" % BASE_DIR
    JOBS = background_tasks
