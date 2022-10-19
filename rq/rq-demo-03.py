#!/usr/bin/env python3

from redis import Redis
from rq import Queue

def main():
    REDIS_SERVER = 'localhost'
    redis_server = Redis(REDIS_SERVER)
    for queue_name in ['default', 'low', 'high']:
        queue = Queue(queue_name, connection=redis_server)
        print(f"{queue_name}: {len(queue)}")


if __name__ == "__main__":
    main()
