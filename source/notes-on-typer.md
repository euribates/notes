---
title: Notas sobre Typer
tags:
  - python
  - cli
---

## Sobre Typer

**[Typer](https://typer.tiangolo.com/)** es una librería para la creación de utilidades de
línea de comandos o aplicaciones **CLI**, basada en los _type hints_ incorporados a partir
de Pytohn 3.6 en adelante. Está desarrollada por el creador de
[FastAPI](https://fastapi.tiangolo.com/).

## Instalación de Typer

Hay que hacer:

```
pip install typer[all]
```

Esto instala también [Rich](https://rich.readthedocs.io/).


## El hola, mundo de Typer

```
import typer


def main(name: str):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
```


