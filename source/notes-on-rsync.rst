rsync
========================================================================

Introducción a rsync
--------------------

**rsync** es una aplicación libre que ofrece transmisión eficiente de
ficheros de forma incremental, que puede trabajar también con datos
comprimidos y cifrados. Mediante una técnica de *delta encoding*,
permite sincronizar archivos y directorios entre dos máquinas de una red
o entre dos ubicaciones en una misma máquina, minimizando el volumen de
datos transferidos.

Cómo obligar a rsync a sincronizar solo los ficheros nuevos
-----------------------------------------------------------

Podemos usar el flag ``--ignore-existing``:

.. code:: shell

    rsync -avhr --ignore-existing -e  /path/to/origin /path/to/target

De la documentación de *rsync*:

    - ``--ignore-existing``: skip updating files that exist on receiver
    
    Do not use ``--update``. The ``--update`` flag does skip files when
    the mtimes are identical (which is not what the wording implies). I
    tested this. I believe the wording would be better understood if it
    said “only source files which are newer than destination will be
    copied or source files that have same modification time as their
    destination file < counterparts, but have different sizes”.

Mirar también las opciones:

- ``-r`` (recursivo)

- ``-v`` (prolijo)

Los parámetros usados en el ejemplo anterior significan:

- ``-a``: Modo archivo

- ``-v``: prolijo

- ``-h``: números legibles para humanos

- ``-r``: recursivo


Cómo hacer que rsync mantenga los ficheros transferidos parcialmente
------------------------------------------------------------------------

Usando el parámetro ``-P`` o ``--partial``: Mantener los ficheros
transferidos parcialmente


Cómo hacer que rsync muestre una barra de progreso
------------------------------------------------------------------------

Con el *flag* ``--progress``: mostrar una barra de progreso


Cómo mantener las fechas de creación y modificación de los ficheros
------------------------------------------------------------------------

Usar el flag ``-t``: Mantener los tiempos de creación y modificación de
los ficheros transferidos.

Fuentes
-------

- Stack Exhchange: `How to rsync only new files <https://unix.stackexchange.com/questions/67539/>`_

- The electric toolbox: `Ignore existing files or update only newer files with rsync <https://electrictoolbox.com/rsync-ignore-existing-update-newer/>`_

- DigitalOcean: `How To Use Rsync to Sync Local and Remote Directories <https://www.digitalocean.com/community/tutorials/how-to-use-rsync-to-sync-local-and-remote-directories>`_
