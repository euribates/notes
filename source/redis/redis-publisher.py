#!/usr/bin/env python3
#
# redis-publisher.py

import random
from time import sleep
from datetime import datetime as DateTime

from redis import Redis


def main():
    redis = Redis(host='127.0.0.1', port=6379)
    while True:
        redis.publish('matraka', f'Now is: {DateTime.now()}')
        waiting_for = random.randrange(1, 11)
        sleep(waiting_for)


if __name__ == "__main__":
    main()
