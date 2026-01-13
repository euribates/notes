Typer
========================================================================

.. tags:: python,cli


Sobre Typer
------------------------------------------------------------------------

`Typer <https://typer.tiangolo.com/>`__ es una librería para la creación
de utilidades de línea de comandos o aplicaciones **CLI**, basada en los
*type hints* incorporados a partir de Pytohn 3.6 en adelante. Está
desarrollada por el creador de
`FastAPI <https://fastapi.tiangolo.com/>`__.

Instalación de Typer
------------------------------------------------------------------------

Hay que hacer:

.. code:: shell

    pip install typer[all]

Esto instala también `Rich <https://rich.readthedocs.io/>`__.

El hola, mundo de Typer
-----------------------

.. code:: python

    import typer

    def main(name: str):
        print(f"Hello {name}")

    if __name__ == "__main__":
        typer.run(main)
