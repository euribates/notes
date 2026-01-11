uwsgi
========================================================================

.. tags:: python,web,wsgi,server


Sobre uWSGI
-----------

El proyecto **uWSGI** intenta ofrecer un *Stack* completo para alojar
desarrollos web. Servidores de aplicación (Para diferentes lenguajes y
protocolos), *proxies*, gestores de procesos y monitores utilizan una
API común y un sistema de configuración homogéneo.

Cómo instalar uWSGI
-------------------

Podemos instalarlo con pip:

.. code:: shell

pip install uswgi

Puede que necesite al compilador de ``C`` y el fuente de Python. Podemos
garantizar que tenemos las dos cosas (En Debian y derivados que usen
``apt``) con:

.. code:: shell

apt install build-essential python

Para máquinas Fedora/Red Hat:

.. code:: shell

yum groupinstall "Development Tools"
yum install python
yum install python-devel

El “HOla, Mundo” de WSGI
------------------------

Creamos el fichero ``foobar.py`` (Puede llamarse como queramos, en
realidad):

::

def application(env, start_response):
start_response('200 OK', [('Content-Type','text/html')])
return [b"Hello World"]

Podemos arranar ahora un servicio web. En este caso, ``application`` si
que es un nombre *obligatorio*, ya que es el nombre del punto de entrada
por defecto de uSWGI (Aunque se podría cambiar en la configuración).

Podemos arrancar uWSGI para que empiece a servir nuestra aplicación, en
este caso escuchando el el puerto ``9090``:

.. code:: shell

uwsgi --http :9090 --wsgi-file foobar.py

Añadiendo concurrencia y monitorización
---------------------------------------

Por defecto, uSWGI arranca un único proceso, y este usa un único
*thread*. Podemos añadir más procesos con ``--process`` (y normalmente
``--master``) y mas *threads* con ``--threads``:

.. code:: shell

uwsgi --http :9090 --wsgi-file foobar.py --master --processes 4 --threads 2

Esto arrancara 4 procesos (Cada uno de ellos con dos *threads*), y un
proceso *master* que rearrancara estos procesos en caso de caida de
alguno de ellos).

Otro aspecto importante es la monitorización, especialmente en
producción. Se puede arrancar un subsistema que da estadisticas de uso
en JSON con ``--stats``:

.. code:: shell

uwsgi --http :9090 --wsgi-file foobar.py --master --processes 4 --threads 2 --stats 127.0.0.1:9191

Una opción más avanzada es usar
``Make some request to your app and then telnet to the port 9191, you’ll get lots of fun information. You may want to use [``\ uwsgitop\ ``]() (Sólo hay que instalarlo con``\ pip\`).
(just pip install it), which is a top-like tool for monitoring
instances.
