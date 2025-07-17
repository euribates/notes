---
title: Notas sobre uv (Python)
tags:
    - python
    - venv
    - tests
    - rust
---

## Qué es uv

[UV](https://docs.astral.sh/uv/) es un gestor e instalador de paquetes Python de
alto rendimiento escrito en Rust. Sirve como sustituto de las herramientas
tradicionales de gestión de paquetes de Python, como pip, y ofrece mejoras
significativas en velocidad, fiabilidad y resolución de dependencias.

## Ver las instalaciones de Python, instaladas o disponibles

Para ver las versiones de pYthon dispoonibles o instaladas:

```shell
uv python list
````

## Crear un entorno virtual con uv

Para crrear un entorno virtual en el directorio ``.venv``:

```shell
uv venv
```

Se puede especificar un nombr, por ejemplo para crear el entorno
virtual en ``myname``:

```shell
uv venv my-name
```

También se puede especificar una versión cncreta de Python:

```shell
uv venv --python 3.11
```

Esto requiere que la versión indicada esté instalada en el sistema. En caso de
no estar instalado, uv descargará e instalará esa versión por nosotros.

