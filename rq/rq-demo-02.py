import random
import datetime

from redis import Redis
from rq import Queue

from tareas import tarea_pesada_y_falible


def main():
    REDIS_SERVER = 'localhost'
    queue = Queue(connection=Redis(REDIS_SERVER))
    start = datetime.datetime.now()
    for _ in range(10):
        task_size = random.randrange(2, 7)
        queue.enqueue(tarea_pesada_y_falible, task_size)
    delta = datetime.datetime.now() - start
    print(f"He tardado {delta.seconds} segundos en total")


if __name__ == "__main__":
    main()
