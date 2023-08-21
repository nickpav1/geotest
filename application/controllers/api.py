import io
import csv
from typing import List
from datetime import datetime

from flask import request
from pydantic import BaseModel, RootModel, ValidationError

from application import app, scheduler
from application.services.distance import DistanceService
from application.services.tasks import TasksService


class CoordinateRecord(BaseModel):
    point: str
    latitude: float
    longitude: float


class Coordinates(RootModel):
    root: List[CoordinateRecord]


@app.route('/api/calculateDistance', methods=["POST"])
def calc_distance():
    data = []
    try:
        for file in request.files:
            content = request.files[file].read().decode()
            data += list(csv.DictReader(io.StringIO(content), delimiter=','))
    except csv.Error:
        return {'error': 'Wrong CSV file'}, 400

    if not data:
        return {'error': 'Wrong CSV file'}, 400

    try:
        data = Coordinates(data).model_dump()
    except ValidationError:
        return {'error': 'Wrong CSV file'}, 400

    task_id, status = TasksService.create(DistanceService.calc_distinct_links, data)
    scheduler.modify_job('geo_calc_task', next_run_time=datetime.now())
    return {'task_id': task_id, 'status': status.value}


@app.route('/api/getResults', methods=["GET"])
def get_results():
    task_id = request.args['task_id']

    status, resp = TasksService.get_result(task_id)
    if status is None:
        return {'error': 'Task not found'}, 404
    data = [{'link': "".join(link), 'distance': d} for link, d in resp.items()]if resp else None
    return {
        'task_id': task_id,
        'status': status.value,
        'data': data
    }
