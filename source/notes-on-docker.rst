Docker
========================================================================

.. tags:: python, docker, devops

.. contents:: Relación de contenidos
    :depth: 3

Introducción a Docker
------------------------------------------------------------------------

Docker es una plataforma abierta para desarrollar, distribuir y ejecutar
aplicaciones. Docker permite separar las aplicaciones de la
infraestructura que debe ejecutarlas para que se pueda entregar software
más rápido.

Características principales de Docker
------------------------------------------------------------------------

- **Entorno de desarrollo integrado**: Docker proporciona un entorno de
  desarrollo completo que incluye *Docker Engine*, *Docker CLI* y
  *Docker Compose*, lo que facilita la creación, administración y
  ejecución de contenedores.

- **Facilidad de uso**: Con una interfaz de usuario intuitiva y comandos
  de línea de comandos simples, Docker es fácil de aprender y usar
  incluso para aquellos nuevos en el mundo de la contenedorización.

- **Soporte multiplataforma**: Docker está disponible para
  Windows, macOS y Linux, lo que permite a los desarrolladores
  trabajar de manera consistente en diferentes sistemas operativos.

- **Integración con Docker Hub**: Docker se integra perfectamente con
  *Docker Hub*, el registro de imágenes de Docker, lo que facilita la
  búsqueda, el acceso y el uso compartido de imágenes de contenedores.

Ventajas de Docker
------------------------------------------------------------------------

- **Velocidad en desarrollo**: La capacidad de crear y ejecutar
  contenedores localmente acelera el ciclo de desarrollo al simplificar
  la creación de entornos de desarrollo complejos.

- **Portabilidad de la aplicación**: Los contenedores creados con
  Docker son portátiles y se pueden compartir y ejecutar fácilmente
  en cualquier entorno compatible con Docker.

- **Consistencia en la implementación**: Al garantizar que el entorno
  de desarrollo sea idéntico al entorno de producción, Docker ayuda a
  evitar problemas de compatibilidad y errores durante la
  implementación de la aplicación.

¿Qué es un contenedor en Docker?
------------------------------------------------------------------------

Un contenedor es un proceso que se ejecuta en un *sandbox* 
dentro de una máquina *host* que está aislado de todos los demás
procesos que se ejecutan en esa máquina *host*. Ese aislamiento
aprovecha los espacios de nombres del kernel y los *cgroups*,
características que han estado en Linux durante mucho tiempo. Docker
hace que estas capacidades sean accesibles y fáciles de usar.

Para resumir, un contenedor:

- Es una instancia ejecutable de una imagen. Puede crear, iniciar,
  detener, mover o eliminar un contenedor utilizando la API o CLI de
  Docker.

- Se puede ejecutar en máquinas locales, máquinas virtuales o
  implementar en la nube.

- Es portátil (y se puede ejecutar en cualquier sistema operativo).

- Está aislado de otros contenedores y ejecuta su propio software,
  binarios, configuraciones, etc.

.. note:: 

    Si está familiarizado con ``chroot``, piense en un contenedor como una
    versión extendida de chroot. El sistema de archivos lo proporciona la
    imagen. El contenedor, no obstante, añade aislamiento adicional, no
    disponible cuando se utiliza solo ``chroot``.

¿Qué es una imagen en Docker?
------------------------------------------------------------------------

Un contenedor en ejecución utiliza un sistema de archivos aislado. Este sistema de archivos aislado es proporcionado por una imagen, y la imagen debe contener todo lo necesario para ejecutar una aplicación: todas las dependencias, configuraciones, scripts, binarios, etc. La imagen también contiene otras configuraciones para el contenedor, como variables de entorno, un comando predeterminado para ejecutar y otros metadatos.

How to dockerize Python
------------------------------------------------------------------------

- Use python:3.7.3-stretch as the base image, to pin the version and OS.
  Or, python:3.7-stretch if you’re feeling less worried about point
  releases.

- Create ``requirements.txt`` with transitively-pinned versions of all
  dependencies, e.g. by using pip-tools, poetry, or Pipenv.

- If you want fast builds, you want to rely on Docker’s layer caching.
  But by copying in the file before running pip install, all later
  layers are invalidated—this image will be rebuilt from scratch every
  time. Solution: Copy in files only when they’re first needed.

- By default Docker containers **run as root**, which is a security
  risk. It’s much better to run as a non-root user, and do so in the
  image itself so that you don’t listen on ports < 1024 or do other
  operations that require a subset of root’s permissions.

Here’s a somewhat better—though still not ideal—Dockerfile that
addresses the issues above:

.. code:: dockerfile

    FROM python:3.7.3-stretch
 
    COPY requirements.txt /tmp/
 
    RUN pip install -r /tmp/requirements.txt
 
    RUN useradd --create-home appuser
    WORKDIR /home/appuser
    USER appuser
 
    COPY yourscript.py .
    CMD [ "python", "./yourscript.py" ]

Sources:

-  `Broken by default: why you should avoid most Dockerfile
   examples <https://pythonspeed.com/articles/dockerizing-python-is-hard/>`_

-  `regularly rebuild your images without caching to get security
   updates <https://pythonspeed.com/articles/docker-cache-insecure-images/>`_

-  `Official Dockerfile best
   practices <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/>`_

-  `Dockerizing Python
   Applications <https://stackabuse.com/dockerizing-python-applications/>`_


Cómo instalar el comando ``ps``
------------------------------------------------------------------------

Hay que instalar el paquete ``procps``:

.. code:: shell

    apt-get update && apt-get install -y procps


Cómo administrar Docker como usuario no root
------------------------------------------------------------------------

El demonio Docker escucha en un *socket* Unix, no en un puerto TCP. De
forma predeterminada, es el usuario ``root`` el que posee el *socket*, y
otros usuarios solo pueden acceder a él utilizando ``sudo``. El demonio
Docker siempre se ejecuta como usuario ``root``.

Para poder usar Docker desde otro usuario, se puede crear un grupo de
Unix llamado ``docker`` y agregarle usuarios.  Esto funciona porque el
*socket* Unix es accesible también por los miembros del grupo
``docker``. En algunas distribuciones de Linux, el sistema crea
automáticamente este grupo al instalar Docker. En ese caso, no hay
necesidad de crear manualmente el grupo.

Para crear el grupo de ``docker`` y añadir el usuario:

.. code:: shell

     sudo groupadd docker
     sudo usermod -aG docker $USER
     newgrp docker

.. warning:: 

    La orden ``newgrp`` debería activar los cambios en los grupos.
    Si no funciona, deberemos cerrar la sesión y volver a iniciarla
    para que la membresía de grupo sea reevaluada.  Si está ejecutando
    Linux en una máquina virtual, puede ser incluso necesario reiniciar
    la máquina virtual para que los cambios surtan efecto.

Pare verificar que podemos usar Docker sin usar sudo, podemos hacer:

.. code:: shell

   docker run hello-world


Cómo obtener estadísticas de procesos con el comando ``top``
------------------------------------------------------------------------

El comando ``top`` de docker es exactamente lo que parecee, ejecuta 
``top`` dentro del contenedor:

.. code:: shell

    $ docker run -d — name=toptest alpine:3.1 watch "echo 'Testing top'"
    fc54369116fe993ae45620415fb5a6376a3069cdab7c206ac5ce3b57006d4241
    $ docker top toptest
    UID PID … TIME CMD
    root 26339 … 00:00:00 watch "echo 'Testing top'"
    root 26370 … 00:00:00 sleep 2

Se imiten en el ejemplo algunas columnas por legibilidad.

También existe el comando ``stats`` que básicamente consiste en ejecutar
``top`` para cada uno de los contenedores de un *host*.

Cómo ver los detalles de un contendor (incluyendo variables de entorno)
------------------------------------------------------------------------

El comando de Docker ``inspect`` devuelve información acerca de un
contenedor o una imagen. A continuación se muestra un ejemplo de uso:

.. code:: shell

    $ docker inspect toptest
    [
        {
        “Id”: “fdb3008e70892e14d183f8 ... 020cc34fec9703c821”,
        “Created”: “2016–03–23T17:45:01.876121835Z”,
        “Path”: “/bin/sh”,
        “Args”: [
            “-c”,
            “while true; do sleep 2; echo ‘Testing top’; done”
        ],
        … and lots, lots more.
        }
    ]

Se ha recortado la salida, por claridad, pero algunos de los campos más
valiosos son:

- Estado actual del contenedor (En la propiedad ``State``)

- La ruta del archivo histórico o ``log`` (en la propiedad ``LogPath``)

- Valores de las variables de entorno (en el campo ``Config.Env``)

- Mapeo de puertos (en el campo ``NetworkSettings.Ports``)

Fuente: `Ten Tips for Debugging Docker Contaniers`_.


Cómo copiar un archivo desde el *host* al contenedor (y viceversa)
------------------------------------------------------------------------

La utilidad ``docker cp`` nos permite copiar un archivo desde o hacia
el contenedor. Si usamos ``-`` se utiliza la entrada/salida estándar.
El contenedor puede estar en ejecución o parado. Los parámetros pasados
pueden ser archivos o directorios.

Ejemplo:

.. code:: shell

    docker cp foo.txt mycontainer:/foo.txt
    docker cp mycontainer:/foo.txt foo.txt

Fuente: `Docker cp command <https://docs.docker.com/engine/reference/commandline/cp/>`_

Cómo ejecutar una imagen pero cambiando el *entrypoint*
------------------------------------------------------------------------

Solo hay que usar el parámetro ``--entrypoint`` de la suborden ``run``
de docker.

Ejemplo:

.. code:: shell

    docker run -it --entry-point python colend_app


How to Purge all unused or dangling Images, Containers, Volumes, and Networks
-----------------------------------------------------------------------------

Docker provides a single command that will clean up any resources —
images, containers, volumes, and networks — that are dangling (not
associated with a container):

.. code:: shell

    docker system prune

To additionally remove any stopped containers and all unused images (not
just dangling images), add the -a flag to the command:

.. code:: shell

    docker system prune -a



Cómo añadir una variable de entorno a un contenedor docker
------------------------------------------------------------------------

Hay que usar el parámetros ``--env`` cuando ejecutamos ``docker run``:

.. code:: shell

    docker run <image> --env COLEND_ENV=test

O podemos usar la orden ``ENV`` en el fichero ``dockerfile`` para
definirla.

Diferencias entre las ordenes RUN, CMD y ENTRYPOINT
------------------------------------------------------------------------

Aunque hacen cosas parecidas, (ejecutar un programa), existen
diferencias importantes:

- ``RUN`` ejecuta el programa a la hora de crear la imagen, lo que
  produce una nueva capa *layer*. El uso habitual es, por ejemplo,
  instalar librerias o dependencias. Es posible, y habitual, tener
  varias ordenes RUN en un dockerfile.

- ``CMD`` define el comando a ejecutar por defecto cuando se arranca el
  contenedor a partir de una imagen, aunque puede ser sobreescrito
  mediante los parámetros de docker. En principio solo puede haber una
  entrada de tipo ``CMD`` en un dockerfile. Si ponemos más de uno, solo
  hará caso de la última. Si le pasamos un comando especifico cuando
  ejecutamos el contenedor, esta orden por defecto no será ejecutada,
  sino lo que hemos suministrado.

- ``ENTRYPOINT`` configura el punto de entrada al ejecutar la imagen
  creada a partir del contenedor. Si definimos esta entrada, podemos
  usar ``CMD`` par definir los parámetros por defecto. Podemos
  modificarlo con el parámetro opcions ``--entrypoint``. Solo debe
  haber una entrada ``ENTRYPOINT`` en un fichero dockerfile,
  normalmente en la última línea.

  La orden ``ENTRYPOINT`` es muy similar a ``CMD``, la diferencia
  radica en que el valor en ``ENTRYPOINT`` **no es ignorado** cuando
  ejecutamos la imagen pasándole parámetros.

El siguiente ejemplo muestra el uso de ``RUN`` para instalar diferentes
sistemas de control de versiones:

.. code:: dockerfile

    RUN apt-get update && apt-get install -y \
        bzr \
        cvs \
        git \
        mercurial \
        subversion

Un punto interesante a observar es que las llamadas a ``apt-get update``
y ``apt-get install`` son ejecutadas **en una única línea**. Esto es
necesario si queremos garantizar que siempre estamos instalando las
últimas versiones disponibles. Si estos comandos estuvieran en dos
sentencias ``RUN``, el comando ``install`` podría ejecutarse basándose
en la capa anterior generada por el ``update``, pero esa capa podría ser
antigua.

Source: `Yury Pitsishin blog - Docker RUN vs CMD vs
ENTRYPOINT <https://goinbigdata.com/docker-run-vs-cmd-vs-entrypoint/>`__

Diferencias entre ``COPY`` y ``ADD``
------------------------------------------------------------------------

``COPY`` and ``ADD`` are both Dockerfile instructions that serve similar
purposes. They let you copy files from a specific location into a Docker
image.

``COPY`` takes in a *source* and *destination*. It only lets you copy in
a local file or directory from your host (the machine building the
Docker image) into the Docker image itself.

``ADD`` lets you do that too, but it also supports 2 other sources.
First, **you can use a URL instead of a local file / directory**.
Secondly, you can **extract a tar file from the source directly into the
destination**.

Como ejecutar un servidor Apache
------------------------------------------------------------------------

Se puede usar la imagen `httpd <https://hub.docker.com/_/httpd>`_ para
arrancar un servidor web apache. En esta imagen no se incluye interprete
de PHP, pero no debería ser difícil de instalar, aunque para eso quizá
mejor usar directamente una imagen con PHP ya instalado y que incluya su
servido web.

La forma más sencilla de usar esta imagen es crear un fichero
``dockerfile`` sencillo y copiar en la carpeta ``public-html/`` de la
imagen los ficheros html a publicar.

Un ejemplo sencillo podría ser:

.. code:: docker

    FROM httpd:2.4
    COPY ./public-html/ /usr/local/apache2/htdocs/

Ahora podemos crear nuestra propia imagen personalizada y ejecutarla con
las siguientes ordenes:

.. code:: shell

    $ docker build -t my-apache2 .
    $ docker run -dit --name my-running-app -p 8080:80 my-apache2

Abre un navegador apuntando a ``http://localhost:8080`` y comprueba que
funciona.

- La opción ``-t`` en la orden ``build`` es para asignarle una etiqueta
  o ``tag`` a la imagen que vamos a crear. Se usa esta etiqueta en la
  orden ``run`` para identificar la imagen.

- La opción ``--name`` en la orden ``run`` le asigna un nombre al
  contenedor, que es por lo general una buena práctica para no tener
  que usar los identificadores hexadecimales generados automáticamente

- La opción ``-p`` (o en versión larga, ``--publish``) es el mapa de
  puertos que se realiza para comunicar el contenedor con el mundo
  exterior. En este caso indicamos que queremos *mapear* el puerto
  **8080** del ordenador anfitrión o *host* con el puerto **80**
  interno de la imagen, que es donde el servidor Apache está esperando
  las peticiones.


Cómo ejecutar un shell dentro de una imagen y conectarse con él
------------------------------------------------------------------------

Si el contenedor está en marcha:

.. code:: shell

    docker exec -it <Container ID or name> bash


Cómo crear un dockerfile
------------------------------------------------------------------------

Un fichero **dockerfile** solo es un fichero de texto que contiene
instrucciones detalladas que le permiten a docker crear una imagen,
normalmente basándonos en una imagen previa.

Veamos un ejemplo donde crearemos una imagen basándonos es la imagen
base de Ubuntu 16.04 y Python 3.X:

.. code:: dockerfile

    FROM ubuntu:16.04
    MAINTAINER Tu Menganito "menganito@invented-email.com"
    RUN apt-get update -y && \  
        apt-get install -y python3-pip python3-dev
    COPY ./requirements.txt /requirements.txt
    WORKDIR /
    RUN pip3 install -r requirements.txt
    COPY . /
    ENTRYPOINT [ "python3" ]
    CMD [ "app/app.py" ]  

Vamos a explicar cada uno de estas instrucciones:

- Todo fichero ``Dockerfile`` empieza con ``FROM`` en la primera
  instrucción, ya que se usa para indicar la imagen base sobre la cual
  se construirá nuestra nueva imagen.

- La orden ``MAINTAINER`` nos permite añadir metadatos sobre la persona
  que mantiene la imagen, normalmente nombre y email. Su uso no es
  obligatoria, pero si recomendable.

- Con ``RUN`` podemos ejecutar comandos en la imagen que nos permiten
  actualizar contenidos y preparar el contexto necesario para la
  ejecución del contenedor. Las ordedes especificadas con ``RUN`` se
  ejecutan **solo cuando se crear o recrea** la imagen. Podemos
  ejecutar todos los comandos ``RUN`` que queramos.

- La orden ``COPY`` se utiliza para añadir ficheros locales a la imagen
  durante la construcción de la imagen. Un caso típico es copiar el
  fichero ``requirements.txt`` para, en un paso posterior, ejecutar con
  ``RUN`` un ``pip install -r requirements.txt``.

- Con ``WORKDIR`` definimos el directorio de trabajo, es decir, la
  carpeta que se usará por defecto con las ordenes ``RUN``, ``COPY``,
  etc.

- La orden ``ENTRYPOINT`` define el punto de entrada, es decir, el
  comando a ejecutar cuando se cree el contenedor. Solo puede haber un
  ``ENTRYPOINT`` en el fichero.

- ``CMD`` define comandos a ejecutar cuando se arranque el contendor.


Cómo crear una imagen de Docker
------------------------------------------------------------------------

Las imágenes de Docker se construyen con el comando ``build``. Las
imágenes se hacen creando varias capas o **layers**, como las llama
Docker. Cada uno de las capas es una nueva imagen, que se crea
incorporando los cambios definidos en cada línea del ``Dockerfile`` a la
imagen generada por la línea anterior.

Todas estas capas son *cacheadas* internamente, para que al re-crear una
imagen, solo haga falta modificar los niveles que hayan cambiado. Por
ejemplo, si la primera línea declara como base la imagen de
``Ubuntu:16.04``, cada vez que vayamos a recrear la imagen final se
puede usar la imagen cacheada como base. Si no tuviéramos esta cache,
habría que descargar de nuevo la imagen base.

Si cambiamos la imagen base, por ejemplo a ``Ubutu:22.10``, entonces
todos los contenidos cacheados son inservibles, y habría que descargar
(y cachear) la nueva imagen base.

Esto es importante a la hora de crear ficheros ``Dockerfile``. Si
queremos que la caché sea efectiva, debemos tener en cuenta el orden en
que realizamos los pasos. Por ejemplo, si primero copiamos con ``COPY``
el fichero ``requirements.txt`` e instalamos todas las dependencias, y
luego copiamos los ficheros propios de nuestra aplicación, tendremos en
la cache una imagen con todas las dependencias instaladas que no
necesita ser reescrita cuando cambiemos nuestra aplicación, solo será
reescribirlo cuando se modifique el fichero ``requiremets.txt``.

Si lo hiciéramos al contrario, copiar el código fuente y luego copiar el
``requirements.txt`` y actualizar, cada vez que cambiamos el código
fuente tiene que descartar todas las imágenes generadas previamente y
empezar a partir de esta, así que tendría que copiar de nuevo los
requerimientos y volver a instalar.

Con esto explicado, vamos el proceso para crear una imagen:

.. code:: shell

    $ docker build -t docker-flask:latest .

La opción ``-t`` se usa para especificar la etiqueta o *tag* que se
asignará a esta imagen.

El punto ``.`` indica el directorio donde se buscará el fichero de
construcción ``dockerfile``.


Cómo ejecutar una aplicación en modo depuración con auto-reinicio
------------------------------------------------------------------------

Durante la etapa de desarrollo, es importante tener ciclos rápidos de
reconstrucción y pruebas. Para esto las aplicaciones web dependen de las
opciones de reinicio automático proporcionadas por *frameworks* como
Flask o Django. Es posible aprovechar esto desde dentro del contenedor.

Para ello, iniciamos el contenedor Docker asignando nuestro directorio
de desarrollo al directorio de aplicaciones dentro del contenedor. Esto
significa que Flask o Django verán los archivos en el host y para
cualquier cambio reiniciarán la aplicación automáticamente.

Además, necesitamos reenviar los puertos de la aplicación desde el
contenedor al host. 

Para lograr esto, comenzamos el contenedor Docker con opciones de mapeo
de volumen y de reenvío de puertos:

.. code:: shell

    docker run --name flaskapp -v$PWD/app:/app -p5000:5000 docker-flask:latest

Esto realiza los siguientes pasos:

- Arranca un contenedor basándose en la imagen que le hemos
  indicado, ``docker-flask``.

- Se la da nombre del contenedor (``flaskapp``) usando el *flag*
  ``--name``. Sin esta opción, el nombre del contenedor sería
  arbitrario. Esto nos ayuda a gestionarlo.

- La opción ``-v`` monta la carpeta local dentro del contenedor.

- La opción ``-p`` mapea los puertos de la máquina local y el 
  contenedor, permitiendo así acceder a la aplicación con la
  dirección ``http://localhost:5000`` o ``http://0.0.0.0:5000/``.


Cómo conectarse a un contenedor en ejecución
------------------------------------------------------------------------

Podemos usar la orden ``docker ps`` para averiguar el nombre del
contenedor, si no lo sabemos.

Sabiendo el nombre, podemos hacer simplemente:

.. code:: shell

    docker exec -it <name> /bin/bash

El significado de los parámetros es:

- ``-i``, ``--interactive`` : Mantiene abierto ``STDIN``
- ``-t``, ``--tty`` : Activa un pseudo-TTY


Cómo saber si una imagen de docker está en ejecución
------------------------------------------------------------------------

Es decir, que hay algún contenedor activo basado en esta imagen. Es
fácil si sabes el nombre:

.. code:: shell

    docker inspect -f '{{.State.Running}}' $container_name


Cómo borrar imágenes terminadas (``exited()``) ejecutadas previamente
------------------------------------------------------------------------

This is the way:

.. code:: shell

    docker rm $(docker ps -qa --filter status=exited )


Como parar uno (o varios) contenedores que están en ejecucion
------------------------------------------------------------------------

Con el siguiente comando podemos parar uno o varios contenedores:

.. code:: shell

   docker stop [OPTIONS] CONTAINER [CONTAINER...]

Las opciones pueden ser:

-  ``--time``, ``-t`` 10 : Segundos a esperar antes de parar el
   contenedor

Cómo borrar todas las imágenes y contenedores
------------------------------------------------------------------------

You use Docker, but working with it created lots of images and
containers. You want to remove all of them to save disk space.

.. code:: bash

   #!/bin/bash 
   # Delete all containers
   docker rm $(docker ps -a -q) 
   # Delete all images
   docker rmi $(docker images -q)

Options:

- ``--all`` , ``-a`` : Remove all unused images, not just dangling ones
- ``--filter`` : Provide filter values (e.g. ’until=')
- ``--force`` , ``-f`` : Do not prompt for confirmation

Why it is recommended to run only one process in a container?
------------------------------------------------------------------------

    In many blog posts, and general opinion, there is a saying that goes
    “one process per container”. Why does this rule exist? Why not run
    ntp, nginx, uwsgi and more processes in a single container that needs
    to have all processes to work?

Lets forget the high-level architectural and philosophical arguments for
a moment. While there may be some edge cases where multiple functions in
a single container may make sense, there are very practical reasons why
you may want to consider following "one function per container" as a
rule of thumb:

- **Scaling** containers horizontally **is much easier** if the
  container is isolated to a single function. Need another apache
  container? Spin one up somewhere else. However if my apache container
  also has my DB, cron and other pieces shoehorned in, this complicates
  things.

- Having a single function per container allows the container to be
  easily **re-used** for other projects or purposes.

- It also makes it more **portable and predictable** for devs to pull
  down a component from production to troubleshoot locally rather than
  an entire application environment.

- **Patching/upgrades** (both the OS and the application) can be done
  in a more **isolated and controlled** manner

- Juggling multiple bits-and-bobs in your container not only makes for
  larger images, but also **ties these components together**. Why have
  to shut down application X and Y just to upgrade Z?

  Above also holds true for code deployments and rollbacks.

- Splitting functions out to multiple containers allows **more
  flexibility** from a security and isolation perspective. You may want
  (or require) services to be isolated on the network level –either
  physically or within overlay networks– to maintain a strong security
  posture or comply with things like PCI.

- Other more minor factors such as dealing with stdout/stderr and
  sending logs to the container log, keeping containers as ephemeral as
  possible etc.

Note that I’m saying function, not process. That language is outdated.
The official docker documentation has moved away from saying “one
process” to instead recommending “one concern” per container.

What is a Docker volume?
------------------------------------------------------------------------

   tldr: The simplest way to describe a Docker volume is this: a Docker
   volume is a folder that exists on the Docker host and is mounted and
   accessible inside a running Docker container. The accessibility goes
   both ways, allowing the contents of that folder to be modified from
   inside the container, or on the Docker host where the folder lives.

Docker uses a special filesystem called a **Union File System**. This is
the key to Docker’s layered image model and allows for many of the
features that make using Docker so desirable. However, the one thing
that the Union File System does not provide for is the persistent
storage of data.

This is because the layers of a Docker image are read-only. When you run
a container from a Docker image, the Docker daemon creates a new
read-write layer that holds all of the live data that represents your
container. When your container makes changes to its filesystem, those
changes go into that read-write layer. As such, when your container goes
away, taking the read-write layer goes with it, and any and all changes
the container made to data within that layer are deleted and gone
forever. That equals non-persistent storage. Remember, however, that
generally speaking this is a good thing. A great thing, in fact. Most of
the time, this is exactly what we want to happen. Containers are meant
to be ephemeral and their state data is too. However, there are plenty
of use cases for persistent data, such as customer order data for a
shopping site. It would be a pretty bad design if all the order data
went bye-bye if a container crashed or had to be re-stacked.

Enter the Docker volume. The Docker volume is a storage location that is
**completely outside of the Union File System**. As such, it is not
bound by the same rules that are placed on the read-only layers of an
image or the read-write layer of a container. A Docker volume is a
storage location that, by default, is on the host that is running the
container that uses the volume. When the container goes away, either by
design or by a catastrophic event, the Docker volume stays behind and is
available to use by other containers. The Docker volume can be used by
more than one container at the same time.

How to fix some common kwnow problems
------------------------------------------------------------------------

Every docker command fails with “Error response from daemon: grpc: the connection is unavailable”
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The docker daemon is corrupt. Run this command:

.. code:: shell

    systemctl restart docker

Maybe you’ll need to use ``sudo`` for this.

Fuente: https://forums.docker.com/t/solved-docker-error-response-from-daemon-grpc-the-connection-is-unavailable/32510


Como ver los contenedores que están ejecutándose
------------------------------------------------------------------------

Usando el subcomando `ps`:

.. code:: shell
	
    sudo docker ps
 
Este es uno de los comandos más básicos de Docker. La salida muestra
el ID del contenedor, su imagen asociada, el nombre, la fecha de creación,
el estado actual y en la última columna, el mapeo de puertos que están
expuestos.

Pero por defecto solo se muestra los contenedores en ejecución y
los recientemente detenidos. Para ver **todos** los contenedores (incluidos los
detenidos) hay que usar el flag ``-a`` o ``--all``:

.. code:: shell
	
    sudo docker ps --all
 
Fuente: `UDMS_Part_13`_ (*Essential Docker Commands and Time-Saving Aliases*)


Como montar un volumen en un contenedor
------------------------------------------------------------------------

Hay que usar la opción ``-v`` y pasarle un mapeo desde un directorio
local a uno dentro de la máquina. Siempre hay que usar **rutas
absolutas**.

.. code:: shell

    docker run -t sandbox -v $(pwd)/sandbox:/sandbox




Learning docker
------------------------------------------------------------------------

Best 100+ Docker Containers for Home Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comprehensive list with 100+ docker containers that you can use on your
home server in 2026.

- https://www.bitdoze.com/docker-containers-home-server/#development-containers


Play with Docker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A simple, interactive and fun playground to learn Docker

-  https://labs.play-with-docker.com/

Play with Docker Classroom
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Play with Docker classroom brings you labs and tutorials that help
you get hands-on experience using Docker. In this classroom you will
find a mix of labs and tutorials that will help Docker users, including
SysAdmins, IT Pros, and Developers. There is a mix of hands-on tutorials
right in the browser, instructions on setting up and using Docker in
your own environment, and resources about best practices for developing
and deploying your own applications.

-  https://training.play-with-docker.com/mvim

.. _UDMS_Part_13: https://www.simplehomelab.com/udms-13-docker-and-docker-compose-commands/
.. _Ten Tips for Debugging Docker Contaniers: https://medium.com/@betz.mark/ten-tips-for-debugging-docker-containers-cde4da841a1d
