
background_tasks = [{
    'id': 'geo_calc_task',
    'func': 'application.tasks.geo_tasks:geo_tasks',
    'trigger': 'interval',
    'seconds': 15,
}]
