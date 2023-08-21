from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

from .config import Config


app = Flask(__name__)
app.config.from_object("application.config.Config")

db = SQLAlchemy(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


from .models import *
from .controllers import *
