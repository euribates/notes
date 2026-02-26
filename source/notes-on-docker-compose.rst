docker-compose
========================================================================

.. tags:: Docker, devops

.. contents:: Relación de contenidos
    :depth: 3

Introdución a Docker Compose
------------------------------------------------------------------------

Con **docker-compose** podemos ejecutar aplicaciones en un entorno
aislado compuesto de contendores y que puede funcionar en cualquier
ordenador que tenga Docker instalado (Ver[[notes-on-docker]]). Esto
facilita trabajar y testear las aplicaciones en un entorno lo más
parecido posible al entorno de producción.

El fichero ``docker-compose.yaml`` gestiona todas las dependencias
(bases de datos, sistemas de colas, caché, etc.) y puede crear y
arrancar cada contenedor usando una sola orden.

Primeros pasos con Docker Compose
------------------------------------------------------------------------

Una vez que se sienta cómodo con los contenedores individuales, es hora
de entrar en Docker Compose. Con esto podemos implementar un grupo de
contenedores que trabajan juntos, generalmente descritos en un archivo
``docker-compose.yml``.

Docker Compose es el siguiente paso que debemos dar para ejecutar
cualquier cosa más allá de las aplicaciones más simples.

Escribir un archivo Compose puede parecer complicado al principio, pero
puede comenzar con ejemplos básicos. Puede definir un servidor web y una
base de datos, configurar sus puertos, vincularlos en una red
personalizada y configurar volúmenes en un solo archivo. 

La interfaz de pilas es útil para monitorear y depurar aplicaciones de
contenedores múltiples. Puede ver los registros de cada servicio,
reiniciarlos individualmente e incluso actualizar el archivo Compose más
tarde para realizar cambios. Este flujo de trabajo refleja cómo se
implementan los contenedores en entornos de producción, por lo que
aprenderlo ahora le brinda una ventaja significativa. También hace que
los proyectos complejos se sientan más manejables agrupando los
servicios relacionados.


Ventajas principales de Docker-compose
--------------------------------------

-  **Portabilidad**

Docker Compose lets you bring up a complete development environment
with only one command: ``docker-compose up``, and tear it down just
as easily using ``docker-compose down``. This allows us developers to
keep our development environment in one central place and helps us to
easily deploy our applications.

-  **Pruebas**

Another great feature of Compose is its support for running unit and
E2E tests in a quick a repeatable fashion by putting them in their
own environments. That means that instead of testing the application
on your local/host OS, you can run an environment that closely
resembles the production circumstances.


Estructura del fichero de composición
------------------------------------------------------------------------

El fichero ``docker-compose.yml`` consiste un múltiples niveles que se
subdividen usando indentación, en vez de llaves, al usar el formato
YAML. Existen **cuatro entradas principales** que prácticamente todo
fichero de composición debería tener:

- La **versión de la especificación** de docker-compose usada en el
  fichero

- Los **servicios** que se construiran y arrancarán

- Todos los **volúmenes** usados

- Las **redes** que conectan los diferentes servicios.

Un fichero de ejemplo podría ser:

.. code:: yaml

    version: '3.3'

    services:
        db:
            image: mysql:5.7
        volumes:
            - db_data:/var/lib/mysql
        restart: always
        environment:
            MYSQL_ROOT_PASSWORD: somewordpress
            MYSQL_DATABASE: wordpress
            MYSQL_USER: wordpress
            MYSQL_PASSWORD: wordpress

        wordpress:
            depends_on:
                - db
            image: wordpress:latest
            ports:
                - "8000:80"
            restart: always
            environment:
                WORDPRESS_DB_HOST: db:3306
                WORDPRESS_DB_USER: wordpress
                WORDPRESS_DB_PASSWORD: wordpress
                WORDPRESS_DB_NAME: wordpress
    volumes:
        db_data: {}

Como se ve en el fichero, se describen dos servicios, un servidor de
Wordoress y un serviodr de bases de datos MySQL. Cada uno de los
servicios se tratará como un contenedor separado, que puede ser
reemplazado cuando sea necesario.


Conceptos y terminología
------------------------------------------------------------------------

The core aspects of the Compose file are its concepts which allow it to
manage and create **a network of containers**.

Servicios
~~~~~~~~~

The services tag contains all the containers which are included in the
Compose file and acts as their parent tag.

Volúmenes
~~~~~~~~~

Los volúmenes son la forma preferida de Docker para persistir los datos
generados y utilizados por los contenedores. Son completamente
administrados por Docker y pueden usarse para compartir datos entre los
contenedores y el *host*.

No aumentan el tamaño de los contenedores que los utilizan y
son independientes del ciclo de vida del contenedor, es decir, que
siguen existiendo después de que el contenedor muera.

.. warning::

    Si no usamos volumenes, y guardamos datos dentro del contendor,
    estos datos se pierden si el contenedor muere.

Existen `diferentes tipos de volumenes`_ que se pueden usar en Docker.
Todos ellos se define usando la palabra reservada ``volumnes`` pero
presentan algunas diferencias que tenemos que tener en cuenta.

**Volúmenes Normales**:

La forma de definir un columen normal es simplenmente incluyendo la ruta
de la carpeta compartida y dejando que Docker cree el volumen
automáticamente, por ejemplo:

.. code:: yaml

    volumes:
        # Just specify a path and let the Engine create a volume
        - /var/lib/mysql

**Mapao de rutas**:

También se puede definir un mapeo para que una determinada ruta en
el *host* este accesible como una ruta diferente en el contenedor; en
este caso tenemos que definir las dos rutas usando el operador ``:``.

.. code:: yaml

    volumes:
        - /opt/data:/var/lib/mysql


El orden es primero la ruta en el *host*, luego la ruta dentro del
contenedor.

**Volúmenes con nombre**:

Otro tipo de volumen es el volumen con nombre, similar a los demás
volúmenes, pero con un nombre específico que facilita su uso en
múltiples contenedores. Por eso se usa a menudo para compartir datos
entre varios contenedores y servicios.

.. code:: yaml

    volumes:
        - datavolume:/var/lib/mysql

Redes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of only using the default network you can also specify your own
networks within the top-level ``networks`` key, allowing to create more
complex topologies and specifying network drivers and options.

.. code:: dockerfile

    networks:
        frontend:
        backend:
            driver: custom-driver
            driver_opts:
                foo: "1"

Each container can specify what networks to connect to with the service
level “``networks``” keyword, which takes a list of names referencing
entries of the top-level “``networks``” keyword.

.. code:: yaml

    services:
        proxy:
            build: ./proxy
        networks:
            - frontend
    app
        build: ./app
        networks:
            - frontend
            - backend
    db:
        image: postgres
        networks:
            - backend

También se puede (desde la versión 3.5) asignarle un nombre propio a las
redes:

.. code:: yaml

    version: "3.5"
    networks:
        webapp:
            name: website
            driver: website-driver

For a full list of the network configuration options, see the following
references:

-  `Top-level network
key <https://docs.docker.com/compose/compose-file/compose-file-v2/#network-configuration-reference>`__

-  `Service-level network
key <https://docs.docker.com/compose/compose-file/compose-file-v2/#networks>`__

Docker cli
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Toda la funcionalidad de Docker-Compose es expuesta a través del cliente
de línea de comando, de forma muy similar al propio Docker:


- ``build``: Build or rebuild services
- ``help``: Get help on a command
- ``kill``: Kill containers
- ``logs``: View output from containers
- ``port``: Print the public port for a port binding
- ``ps``: List containers
- ``pull``: Pulls service images
- ``rm``: Remove stopped containers
- ``run``: Run a one-off command
- ``scale``: Set number of containers for a service
- ``start``: Start services
- ``stop``: Stop services
- ``restart``: Restart services
- ``up``: Create and start containers
- ``down``: Stops and removes containers

They are not only similar but also behave like their Docker
counterparts. The only difference is that they affect the entire
multi-container architecture which is defined in the
``docker-compose.yml`` file instead of a single container.

Some Docker commands are not available anymore and have been replaced
with other commands that make more sense in the context of a completely
multi-container setup. The most important new commands are
``docker-compose up`` and ``docker-compose down``.

Fuente: `The definitive Guide to Docker compose`_, de Gabriel Tanner.


.. _The definitive Guide to Docker compose: https://gabrieltanner.org/blog/docker-compose
.. _diferentes tipos de volumenes: https://docs.docker.com/storage/volumes/
