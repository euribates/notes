Systemd
========================================================================


Qué es *Systemd*
------------------------------------------------------------------------

`Systemd <https://es.wikipedia.org/wiki/Systemd>`__ es un sistema de
inicialización (*init*) usado por varias distribuciones de Linux. El
sistema de inicialización se ocupa de arrancar los componentes del
sistema que deben ejecutarse después de que el kernel ya haya arrancado.
Además, debe ocuparse de gestionar a los servicios y
`daemons <https://es.wikipedia.org/wiki/Daemon_%28computing%29>`__.

El comando ``systemctl`` es la herramienta principal para gestionar
``systemd``. Con respecto a los servicios o *daemons*, las opciones más
usadas típicas son arrancar un servicio (``start``), pararlo (``stop``),
reiniciarlo (``restart``) y habilitarlo para que se arranque
automáticamente al inicio, o no (``enable`` y ``disable``).

Unidades
------------------------------------------------------------------------

En *Systemd*, el objetivo de la mayoría de las acciones es conocido como
**unidades** o **units**, que son recursos que el sistema conoce y sabe
como gestionar. Las unidades se dividen en categorías basadas en los
tipos de recursos que representan y se definen con ficheros conocidos
como ficheros de unidades (*Unit files*). Se puede deducir el tipo de
cada unidad por el sufijo usado en el nombre del fichero.

Para unidades de gestión de servicios, el sufijo es ``.service``, pero
en la mayoría de los casos no necesitaremos incluirlo, ``systemd``
asumirá esta terminación por defecto. Por ejemplo, para gestionar el
*deamon* ``nginx`` no hace falta escribir ``nginx.service``, aunque se
puede hacer; basta con ``ngigx``.

Como listar todos los servicios en ejecución
------------------------------------------------------------------------

Si ejecutamos el comando ``systemctl`` sin ningún parámetro, el programa
listará **todas** las unidades que conozca, incluyendo los servicios,
mostrando además un indicador de estado que nos indicará si la unidad
está activa o no.

Para seleccionar solo los servicios, usaremos el subcomando
``list-units``, y con el parámetro ``--type`` indicamos el valor
``service``:

.. code:: shell

    systemctl list-units --type=service

Podemos filtrar también por el estado con el parámetro ``--state``, por
ejemplo para ver solo los servicios activos:

.. code:: shell

    systemctl list-units --type=service --state=active

Podemos indicar varios estados, separados por coma:

.. code:: shell

    systemctl list-units --type=service --state=active,failed

Fuente: `TecMint - How to List All Running Services Under Systemd in Linux <https://www.tecmint.com/list-all-running-services-under-systemd-in-linux/>`__

Arrancando y parando servicios
------------------------------------------------------------------------

Para arrancar un servicio, cuyas instrucciones de ejecución están
detalladas en el fichero de unidad, se usa el comando ``**start**``.
Hacen falta privilegios de ``root`` para esto, así que normalmente
usaremos la orden ``sudo``:

.. code:: shell

    sudo systemctl start servicio.service

O, como comentamos antes, omitiendo el sufijo ``.service``:

.. code:: shell

    sudo systemctl start servicio

Para pararlo, usaremos el subcomando ``**stop**``:

.. code:: shell

    sudo systemctl stop servicio

Rearranque y recarga
------------------------------------------------------------------------

Para arrancar de nuevo un servicio, es decir, para pararlo y volverlo a
arrancar, podemos usar el comando ``**restart*``:

.. code:: shell

    sudo systemctl restart servicio

En aquellos casos en que el sistema sea capaz de hacer un arranque en
caliente, es decir, que sea capaz de cargar de nuevo su configuración y
continuar trabajando los nuevos valores, podemos usar la orden
``**reload**``:

.. code:: shell

    sudo systemctl reload servicio

Por lo general es siempre preferible hacer un arranque en caliente, pero
si no estamos seguros de si el servicio lo soporta, podemos usar la
orden **``reload-or-restart``**:

.. code:: shell

    sudo systemctl reload-or-restart servicio

- Source: `How To Use Systemctl to Manage Systemd Services and Units <https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units>`__

Cómo listar todas las unidades activas gestionadas por systemd
------------------------------------------------------------------------

Ejecutamos el comando:

.. code:: shell

    sudo systemctl list-units

Fuente: `Cómo listar todas las unidades de servicios de systemd - Foro Vozidea.com <https://foro.vozidea.com/d/13-como-listar-todas-las-unidades-de-servicios-de-systemd>`_

How to see full log from systemctl status service?
------------------------------------------------------------------------

Just use the journalctl command, as in:

.. code:: shell

    journalctl -u service-name.service

Or, to see only log messages for the current boot:

.. code:: shell

    journalctl -u service-name.service -b

Cómo saber cuanto espacio en disco utilizan los logs de *systemd*
------------------------------------------------------------------------

El *journal* de systemd es el sistema de registro (*logging*) propio de
systemd. Es equivalente al *syslog* en el sistema *init*. Recopila y
almacena datos de registro del núcleo (*kernel*), mensajes de registro
del sistema, salida estándar y errores de diversos servicios de *systemd*.

Linux escribe los registros en el directorio ``/var/log/journal``.

Se puede consultar el espacio ocupado de dos formas: 

Usando el comando ``du`` (*disj usage*):

.. code:: shell

    du -sh /var/log/journal/

O podemos usar el comando ``journalctl``:

.. code::

    journalctl --disk-usage

Los dos deberían arrojar un resultado similar.

Cómo limpiar el tamaño de los registros de archivo de systemd
------------------------------------------------------------------------

El comando ``journalctl`` es la manera adecuada de gestionar los
registros antiguos.

Primero debemos rotar los archivos del *journal*. Esto marcará los
registros activos como archivados y creará otros nuevos. Es opcional,
pero resulta una buena práctica hacerlo.

.. code:: shell

    sudo journalctl --rotate

Hoy tres formas de eliminar los registros antiguos. Las opciones son:

- Borrar registros anteriores a un momento determinado.

- Borrar archivos de registro antiguos para que el tamaño total se
  ajuste a un límite de espacio en disco predefinido.

- Limitar el número de archivos de registro.

1. Eliminar registros del *journal* anteriores a *x* días
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Supongamos que se desea conservar el historial de registros de solo dos
días. Para eliminar las entradas anteriores a dos días, usaríamos:

.. code:: shell

    sudo journalctl --vacuum-time=2d

También se puede definir el intervalo de tiempo en otras unidades: horas
(por ejemplo, ``2h``), minutos (``2m``) o segundos (``2s``). Para
unidades de tiempo mayores, también se puede usar ``2weeks`` (semanas) o
``2months`` (meses).

2. Limitar el tamaño de los registros
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Esto eliminará archivos del *journal* hasta que el espacio en disco
ocupado por ellos sea inferior al límite que hayas especificado.

.. code:: shell

    sudo journalctl --vacuum-size=100M

Esto reducirá el tamaño de los registros a aproximadamente 100 MB.

Se puede especificar el tamaño utilizando sufijos como ``G`` para
gigabytes, ``M`` para megabytes, ``K`` para kilobytes, etc.

3. Limitar el número de archivos de registro
------------------------------------------------------------------------

La tercera forma consiste en limitar la cantidad de archivos de
registro. ``journalctl`` suele contener archivos de registro (logs)
tanto del sistema como de los usuarios. A medida que estos registros
envejecen, se archivan en diversos archivos.

Es posible limitar la cantidad de archivos de registro archivados. Por
ejemplo, si deseas conservar únicamente cinco archivos de registro:

.. code:: shell

    journalctl --vacuum-files=5

Esto eliminará los archivos de registro archivados más antiguos, dejando
solo la cantidad especificada.

Fuentes:

- `Systemd logs are too large and slow`_ - Ask Ubuntu
- `How to Clear Systemd Journal Logs`_ - Linux Handbook

.. _How to Clear Systemd Journal Logs: https://linuxhandbook.com/clear-systemd-journal-logs/
.. _Systemd logs are too large and slow: https://askubuntu.com/questions/1012912/systemd-logs-journalctl-are-too-large-and-slow
