#!/usr/bin/env python3

import random
import time


def tarea_pesada_y_falible(secs):
    print(f"tarea_pesada_y_falible ({secs})", end=" ", flush=True)
    if random.randrange(5) == 0:
        raise ValueError("Hoy no me puedo levantar ♪♫")
    for _ in range(secs):
        print(".", end="", flush=True)
        time.sleep(1)
    print(" [OK]")
