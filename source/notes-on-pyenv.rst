pyenv
========================================================================

.. tags:: python,virtualization


Sobre pyenv
------------------------------------------------------------------------

`Pyenv <https://github.com/pyenv/pyenv#readme>`__ es una utilidad que te
permite conmutar fácilmente entre versiones de Python. Sigue la
filosofía Unix de hacer solo una cosa pero hacerla bien.

Una ventaja que tiene es que **no depende de Python**, es un conjunto de
*scripts* de *shell*.

Instalar pyenv
------------------------------------------------------------------------

Lo mejor es instalarlo acompañado de
`virtualenv <https://virtualenv.pypa.io/en/latest/>`__, para ello hay
que instalar tanto ``pyenv`` como ``pyenv-virtualenv``.

En Mac:
~~~~~~~

.. code:: shell

    brew install pyenv
    brew install pyenv-virtualenv

Y luego añadir esto en el fichero ``.bashrc``:

.. code:: bash

    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"

En linux:
~~~~~~~~~

Primero instalamos algunas librerías que nos harán falta:

.. code:: shell

    sudo apt install build-essential build-dep make python3-dev
    \ lib1g-dev libffi-dev libssl-dev zlib1g-dev
    \ libbz2-dev libedit-dev libreadline-dev libsqlite3-dev liblzma-dev
    \ libncurses-dev tk-dev openssl-dev llvm xz-utils python-openssl
    sudo apt install curl
    sudo apt install make

Luego instalamos el pyenv:

.. code:: shell

    curl https://pyenv.run | bash

Crear un entorno virtual con pyenv
------------------------------------------------------------------------

Hay que ejecutar ``pyenv virtualenv <python.version> <name>``, donde
``<python.version>`` es una especificación de la versión de Python
usando 4 dígitos separados por coma, como ``2.7.18`` o ``3.11.2``, y
``<name>`` el nombre del *virtualenv*:

.. code:: shell

    pyenv virtualenv 3.11.2 newacl

Si no se especifica la versión, se instalará la última versión estable
conocida por pyenv.

Listando los virtualenvs existentes
------------------------------------------------------------------------

Con el comando ``pyenv virtualenvs``.

Activando/Desactivando los entornos virtuales con pyenv
------------------------------------------------------------------------

Si en una carpeta existe un fichero ``.python-version`` cuyo contenido
coincide con el nombre de un entorno virtual, y si hemos ejecutado
previamente en la *shell*:

``eval "$(pyenv virtualenv-init -)"``

(Esto normalmente se hace en el fichero ``.bash-rc``)

Al cambiar a este directorio **se activa automáticamente el entorno
virtual**, y si nos salimos del directorio, se desactiva también
automáticamente.

También podemos activar/desactivar manualmente en entorno con los
comandos:

.. code:: shell

    pyenv activate <name>
    pyenv deactivate

Borrar un entorno virtual creado con pyenv
------------------------------------------------------------------------

Usaremos el comando ``unnistall`` de ``pyenv``:

.. code:: shell

    pyenv uninstall <name>


Cómo instalar versiones de Python adicionales en pyenv
------------------------------------------------------------------------

Usamos el subcomando ``install``. Por ejemplo, para descargar y poner
como disponible la versión de Python 3.12.1, haríamos:

.. code:: bash

    pyenv install 3.12.1

Ejecutando ``pyenv install -l`` devuelve un listado de todas las
versiones disponibles.

Cómo actualizar la lista de versiones de Python conocidas por pyenv
------------------------------------------------------------------------

Con el comando ``pyenv update``.

O si estás en un Mac, ``brew upgrade pyenv``.

Cómo listar las versiones de Python disponibles
------------------------------------------------------------------------

Con la orden ``install``, usando el flag ``--list`` o ``-l``:

.. code:: shell

    pyenv install --list

Qué son los shims
------------------------------------------------------------------------

Para que pyenv funcione, se inserta un **directorio de shims** (Cuñas o
calzadores) al principio del ``PATH``, de esta forma:

.. code:: shell

    $ echo $PATH
    $(pyenv root)/shims:/usr/local/bin:/usr/bin:/bin

Mediante un proceso llamada ``rehashing``, pyenv mantiene *shims* en ese
directorio para casar con todos los ejecutables de Python: ``pip``,
``python``, etc. En esencia, los *shims* son ejecutables ligeros, que
simplemente pasan el programa y los parámetros correspondientes a través
de pyenv, así que cuando se ejecuta, por ejemplo, ``pip``, el sistema
operativo hará lo siguiente:

- Buscar en el ``PATH`` un ejecutable que se llame ``pip``

- Encontrar el *shim* llamado ``pip`` en la primera carpeta del
  ``PATH``.

- Ejecutar el *shim* ``pip``, que a su vez para el comando con pyenv.

Fuente: `GitHub - pyenv/pyenv: Simple Python version management <https://github.com/pyenv/pyenv>`_

Como compilar la versión de Python que queremos desde las fuentes
------------------------------------------------------------------------

Hay que instalar varias librerías de código fuente:

.. code:: shell

    $ sudo apt install make libssl-dev libedit-dev libreadline-dev \
           openssl-dev libffi-dev libbz2-dev libsqlite3-dev \
           tk-dev liblzma-dev build-dep python3-dev
