#!/usr/bin/env python3

import random
import datetime

import tareas


def main():
    start = datetime.datetime.now()
    for _ in range(10):
        task_size = random.randrange(2, 7)
        try:
            tareas.tarea_pesada_y_falible(task_size)
        except Exception as err:
            print(err)
    delta = datetime.datetime.now() - start
    print(f"He tardado {delta.seconds} segundos en total")


if __name__ == "__main__":
    main()
