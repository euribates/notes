---
title: Notas sobre pyinfra
tags:
    - python
    - sysadmin
    - devops
---

## Notas sobre pyintra

pyinfra automates infrastructure using Python. It’s fast and scales from one
server to thousands. Great for ad-hoc command execution, service deployment,
configuration management and more. Here's why you should try pyinfra:

## Para empezar con pyinfra

Para empezar con pyinfra se necesitan dos cosas:

- El **Inventario**: Aqui definimos los _hosts_, grupos y datos. Los _hosts_ son
  los objetivos sobre los que se ejecutan los comandos o los cambios de estado
  de pyinfra. (Si es un serifor físico, mediante `ssh`, si es un contendero,
  usando docker, etc.). Los _hosts_ pueden ser asignados a **grupos**, y les
  elementos de datos se pueden asignar indixtintamente a _hosts_ o a grupos.

  By default pyinfra assumes hosts can be reached over SSH. pyinfra can connect to other systems using connectors, for example: a Docker container or the local machine.

- Las **Operaciones**: Ordenes o nuevos estados que hay que aplicar a uno o más
  _hosts_, ya sea directamente o usando grupos. Estas odenes pueden ser simples
  comandos de shell como "Ejecuta el comando `uptime`" o cambios de estado como
  "Asegurate de que el paquete `apt` `iftop` esté instalado".

