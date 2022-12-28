import random
import datetime
from redis import Redis
from rq import Queue
from constantes import (
    REDIS_SERVER,
    REDIS_PASSWORD,
    REDIS_PORT,
    REDIS_DB,
    )
import tareas


q = Queue('default', connection=Redis(
    host=REDIS_SERVER,
    password=REDIS_PASSWORD,
    port=REDIS_PORT,
    db=REDIS_DB,
    ))

print(f"q length: {len(q)}")
start = datetime.datetime.now()
for i in range(10):
    task_size = random.randrange(2, 7)
    job = q.enqueue(tareas.tarea_pesada_y_falible, task_size)
    print(f"q length: {len(q)}")
    print(i, job.id, 'queued')
delta = datetime.datetime.now() - start
print(f"He tardado {delta.seconds} segundos en total")
print(f"q length: {len(q)}")
