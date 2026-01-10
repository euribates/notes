#!/usr/bin/env python3
#
# redis-subscriber.py

from redis import Redis


def main():
    redis = Redis(host='127.0.0.1', port=6379)
    pubsub = redis.pubsub()
    pubsub.subscribe('matraka')
    for msg in pubsub.listen():
        print(msg)


if __name__ == "__main__":
    main()
