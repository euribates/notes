---
title: Notas sobre GitHub y el cliente GH
tags:
    git
    cli
---

## Sobre GitHub


## Autenticación con Git/ssh

Sistemas de seguridad en GitHub

De menor a mayor complejidad:

- ssh agent forwarding
- Usando HTTPS con Auth tokens
- Claves de despliegue

### Usando claves de despliegue

Hay que generar una nueva pareja de claves. Con el sistema de Clades de
despliegue, hay que tener **una clave de despliegue por cada repositorio**, no se pueden
compartir las claves entre repos.

Eso no nos dara mucho problema si un servidor solo necesita acceso
a un repositorio, pero si necesita acceder a más, ya no puede confiar en usar
simplemente la clave publica por defecto (normalmente `~/.ssh/id_rsa.pub`, sino
que
** hay que indicar en cada repo que clave publica debe usar*.

