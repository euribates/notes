---
title: Notas sobre CHIP-8
tags:
    hardware
    cpu
    learning
---

## Arquitectura de la máquina virtual

Normalmente se considera que un sistema CHIP-8 consta de una memoria RAM
de 4KB (4096 bytes de 8 bits). El interprete de CHIP-8 ocupa los
primeras 512 bytes. Por ewa razón, la mayoria de los programas empiezan
en la direccion 500 (0x200) y nunca acceden a direccions por debajo de
512.

Las 256 direcciones más altas (0xF00-0xFFF) se reservan para la memoria
de refresco de la pantalla, y los 96 bytes anteriores (0xEA0-oxEFF) se
reservan para la pila de llamadas, usos internos y otras variables.

## Registros

CHIP-8 dispone de 16 registros de 8 bits, nombrados desde `V0` a `VF`.
El registro 'VF' sirve como registro de _flags_ para determinadas
operaciones, por lo que debe evitarse su uso de forma directa. Por
ejemplo, en una operación de suma, `VF` es el _flag_ de acarreo, en las
operaciones de dibujo en pantalla, sirve para detectar colisiones.

## La pila

La pila o _stack_ solo se usa para almacenar las direcciones de regreso
de las subrutinas, cuando son llamadas.

subrurinas
