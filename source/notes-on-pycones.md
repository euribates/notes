---
title: Notas sobre la PyConEs
tags:
  - python
---

## Katas

- Codewars
- Advent of code
- Projet Euler
- Hacktober


## Mocks

Test external systeme (filesystem, web request, etc...)

Parchear correctamente
ejemplo mymodule, etcc/...

Side effect

Puede ser una secuencia, entonces devuelve sucesivamente los valores de la secuencia

Spec and autospec

Mock vs MAgicMock
 
 MogicMOck tiene implementecion por defecto de todos los dunder

 Corres el riesgo de que el test pases when it should fail.

## Desing Patterns

Spaguetti code 

Inject dependency for free

Creational design patterns

Structural design patterns

__wrapped__ (if you use wraps from decor utilities) gives you the wrapper functions to test

Facade

Behavioral Design patterns

 - Pipeline

 - Pytoolz
 
 Antipatters

 - Lava flow
 
 https://pycones19.sched.com/event/VdOK/game-of-patterns?iframe=yes&w=100%&sidebar=yes&bg=no#

## Apache Airflow

Ejecutar tareas de fomra coordinada

Las tareas se pueden incluir en un grafo dirigido para especificars delependendcia DAG

Las tareas pueden ser codigo Python

Implementación en Python

Alta acoplación a Airflow

Python 

### Recomendaciones

Las tareas deben ser idempotentes

Dividir tareas grandes en pequeñas y especificar las dependencias

No user XCom

### Cosas que se hicieron bien / Para aprender Alicante

- La guardería y la ludoteca para niños mayores

- No hubo colas interminables para la comida. Meritorio porque habia apuntadas
  mas de 800 personas

- La botella de agua de regalo. Práctica y ecológica 

- Las salas estaban todas cerca, no hacia falta usar escaleras. La única excepcion las
  sesiones de inicio y fin. La Universidad de Alicante es enorme y muy bonita

- Bastantes tomas de corriente en las salas/áulas

- La app de Sched para el programa
