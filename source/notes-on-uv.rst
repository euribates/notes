uv
========================================================================

.. tags:: python,venv,tests,rust


Qué es uv
---------

`UV <https://docs.astral.sh/uv/>`__ es un gestor e instalador de
paquetes Python de alto rendimiento escrito en Rust. Sirve como
sustituto de las herramientas tradicionales de gestión de paquetes de
Python, como pip, y ofrece mejoras significativas en velocidad,
fiabilidad y resolución de dependencias.

Ver las instalaciones de Python, instaladas o disponibles
---------------------------------------------------------

Para ver las versiones de pYthon dispoonibles o instaladas:

.. code:: shell

uv python list

Crear un entorno virtual con uv
-------------------------------

Para crrear un entorno virtual en el directorio ``.venv``:

.. code:: shell

uv venv

Se puede especificar un nombr, por ejemplo para crear el entorno virtual
en ``myname``:

.. code:: shell

uv venv my-name

También se puede especificar una versión cncreta de Python:

.. code:: shell

uv venv --python 3.11

Esto requiere que la versión indicada esté instalada en el sistema. En
caso de no estar instalado, uv descargará e instalará esa versión por
nosotros.

Cómo añadir dependencias usando UV
------------------------------------------------------------------------

Para añadir una dependencia uasmos el subcomendo ``add``,  por ejemplo, 
para incluir la librería ``requests`` como dependicia, hariemos:

.. code:: shell

   uv add requests


Este comando agregar ``requests`` a las dependencias del proyecto y
también instala la biblioteca en el entorno virtual. Se puede ver la dependencia en el fichero ``pyproject.toml``:

.. code::

   [project]
   name = "rpcats"
   version = "0.1.0"
   description = "Mostrar información del gato para la raza especificada."
   readme = "README.md"
   required-python = ">=3.13"
   dependencies = [
       "requests>=2.32.3",
   ]

La orden ``uv add`` actualiza automáticamente la lista de dependencias en
el archivo ``pyproject.toml``. En el ejempl, se indica que la la versión
instalada debe ser mayor o igual a 2.32.3.

Si está trabajando en un proyecto existente y desea migrar desde un
archivo ``requirements.txt``, se puede ejecutar el siguiente comando:

.. code:: shell

   uv add -r requirements.txt

Esta orden instala e importa las dependencias declaradas en el archivo ``requirements.txt``
dentro de la UV.

Además, actualiza el archivo ``uv.lock`` con la siguiente información:

- **Dependencias directas**: Paquetes de los que depende el proyecto
  directamente. En el ejemplo, ``requests``.

- **Dependencias transitivas**: Paquetes que soportan las dependencias
  directas del proyecto. Por ejemplo, la biblioteca ``requests`` depende
  de ``urllib3``, y por tanto se instala como una dependencia transitiva.

No hay que preocuparse por el contenido uv.lock y no debería editarse. Es
UV el que debe encargarse de su mantenimiento.

.. warning:: 

   A pesar de que uv tiene una interfaz alternativa que imita a pip, no
   debe usarla para instalar dependencias porque estos comandos **no
   actualizarán el archivo uv.lock o pyproject.toml** automáticamente como
   si lo hace uv add.

Fuente: https://realpython.com/python-uv/
