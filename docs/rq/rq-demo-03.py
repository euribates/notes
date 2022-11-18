#!/usr/bin/env python3


from redis import Redis
from rq import Queue

from configuracion import REDIS_SERVER, REDIS_PASSWORD, REDIS_PORT, REDIS_DB


def get_queue(queue_name):
    return Queue(queue_name, connection=Redis(
        host=REDIS_SERVER,
        password=REDIS_PASSWORD,
        port=REDIS_PORT,
        db=REDIS_DB,
    ))


def main():
    for queue_name in ['default', 'low', 'high']:
        queue = get_queue(queue_name)
        print(f"{queue_name}: {len(queue)}")


if __name__ == "__main__":
    main()
