#!/usr/bin/env python3


import random, datetime
from redis import Redis
from rq import Queue
from tareas import tarea_pesada_y_falible
from constantes.parlamento import *

def get_queue(queue_name):
    return Queue(queue_name, connection=Redis(
        host=REDIS_SERVER,
        password=REDIS_PASSWORD,
        port=REDIS_PORT,
        db=REDIS_DB,
    ))

for queue_name in ['default', 'low', 'high', 'enrique', 'default_dya', 'alex']:
    queue = get_queue(queue_name)
    print(f"{queue_name}: {len(queue)}")
