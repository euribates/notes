REDIS
========================================================================

Introducción a :index:`Redis`
------------------------------------------------------------------------

**Redis** es un motor de base de datos en memoria, basado en el
almacenamiento en tablas de *hashes* (clave/valor) pero que opcionalmente
puede ser usada como una base de datos durable o persistente. Está
escrito en ANSI C por Salvatore Sanfilippo, quien es patrocinado por
Redis Labs. Está liberado bajo licencia BSD por lo que es considerado
software de código abierto.

Cómo limpiar la caché de Redis y borrar todo el contenido con el CLI
----------------------------------------------------------------------

Puedes limpiar toda la cache/database y borrar todas las claves y
valores que contenga usando una de las dos siguientes ordenes:

-  ``FLUSHDB`` Borra todas las claves y valores de la base de datos
  actual

-  ``FLUSHALL`` Borra todas las claves y valores de **todas las bases de
  datos**.

La sintaxis para hacerlo desde la línea de comandos es:

.. code:: bash

   redis-cli FLUSHDB
   redis-cli -n DB_NUMBER FLUSHDB
   redis-cli -n DB_NUMBER FLUSHDB ASYNC
   redis-cli FLUSHALL
   redis-cli FLUSHALL ASYNC

Source: `Nixcraft How to flush Redis cache and delete everything using
the
CLI <https://www.cyberciti.biz/faq/how-to-flush-redis-cache-and-delete-everything-using-the-cli/>`__


Cómo hacer transacciones en Redis
-----------------------------------------------------------------------

Orders ``MULTI``, ``EXEC``, ``DISCARD`` and ``WATCH`` are the foundation
of transactions in Redis. They allow the **execution of a group of
commands in a single step**, with two important guarantees:

-  **ISOLATION**: All the commands in a transaction are serialized and
   executed sequentially. **It can never happen that a request issued by
   another client is served in the middle of the execution of a Redis
   transaction**. This guarantees that the commands are executed as a
   single isolated operation.

-  **ATOMICITY**: Either **all of the commands or none** are processed,
   so a Redis transaction is also atomic.

The ``EXEC`` command triggers the execution of all the commands in the
transaction, so if a client loses the connection to the server in the
context of a transaction before calling the ``MULTI`` command none of
the operations are performed, instead if the ``EXEC`` command is called,
all the operations are performed.

When using the append-only file Redis makes sure to use a single
write(2) syscall to write the transaction on disk. However if the Redis
server crashes or is killed by the system administrator in some hard way
it is possible that only a partial number of operations are registered.
Redis will detect this condition at restart, and will exit with an
error. Using the redis-check-aof tool it is possible to fix the append
only file that will remove the partial transaction so that the server
can start again.

Usage
~~~~~

A Redis transaction is entered using the ``MULTI`` command. The command
always replies with ``OK``. At this point the user can issue multiple
commands. Instead of executing these commands, Redis will queue them.
All the commands are executed once ``EXEC`` is called.

Calling ``DISCARD`` instead will flush the transaction queue and will
exit the transaction.

The following example increments keys foo and bar atomically:

.. code:: redis

   > MULTI
   OK
   > INCR foo
   QUEUED
   > INCR bar
   QUEUED
   > EXEC
   1) (integer) 1
   2) (integer) 1

``EXEC`` returns an array of replies, where every element is the reply
of a single command in the transaction, in the same order the commands
were issued.

When a Redis connection is in the context of a ``MULTI`` request, all
commands will reply with the string ``QUEUED``.

Errors inside a transaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~

During a transaction it is possible to encounter **two kind of command
errors**:

-  A command may **fail to be queued**, so there may be an error before
   ``EXEC`` is called. For instance the command may be syntactically
   wrong (wrong number of arguments, wrong command name, ...), or there
   may be some critical condition like an out of memory condition (if
   the server is configured to have a memory limit using the maxmemory
   directive).
-  A command may **fail after \``EXEC`\` is called**, for instance since
   we performed an operation against a key with the wrong value (like
   calling a list operation against a string value).

Clients used to sense the first kind of errors, happening before the
EXEC call, by checking the return value of the queued command: if the
command replies with ``QUEUED`` it was queued correctly, otherwise Redis
returns an error. If there is an error while queueing a command, most
clients will abort the transaction discarding it.

However starting with Redis 2.6.5, the server will remember that there
was an error during the accumulation of commands, and will **refuse to
execute the transaction** returning also an error during ``EXEC``, and
discarding the transaction automatically.

Errors happening after ``EXEC`` are not handled in a special way: all
the other commands will be executed even if some command fails during
the transaction.

Discarding the command queue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``DISCARD`` can be used in order to abort a transaction. In this case,
no commands are executed and the state of the connection is restored to
normal.

Optimistic locking using check-and-set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``WATCH`` is used to provide a **check-and-set (CAS)** behavior to Redis
transactions.

WATCHed keys are monitored in order to detect changes against them. If
**at least one watched key is modified before the EXEC command, the
whole transaction aborts**, and EXEC returns a Null reply to notify that
the transaction failed.

For example, imagine we have the need to atomically increment the value
of a key by 1 (let's suppose Redis doesn't have ``INCR``).

The first try may be the following:

::

   val = GET mykey
   val = val + 1
   SET mykey $val

This will work reliably only if we have a single client performing the
operation in a given time. If multiple clients try to increment the key
at about the same time there will be a **race condition**. For instance,
client A and B will read the old value, for instance, 10. The value will
be incremented to 11 by both the clients, and finally SET as the value
of the key. So the final value will be 11 instead of 12.

Thanks to ``WATCH`` we are able to model the problem very well:

::

   WATCH mykey
   val = GET mykey
   val = val + 1
   MULTI
   SET mykey $val
   EXEC

Using the above code, if there are race conditions and another client
modifies the result of val in the time between our call to WATCH and our
call to EXEC, the transaction will fail.

We just have to repeat the operation hoping this time we’ll not get a
new race. This form of locking is called **optimistic locking** and is a
very powerful form of locking. In many use cases, multiple clients will
be accessing different keys, so collisions are unlikely – usually there
is no need to repeat the operation.

Cómo funciona *WATCH*
---------------------

So what is ``WATCH`` really about? It is a command that will make the
``EXEC`` conditional: we are asking Redis to perform the transaction
only if none of the WATCHed keys were modified. (But they might be
changed by the same client inside the transaction without aborting it.
More on this.) Otherwise the transaction is not entered at all. (Note
that if you ``WATCH`` a volatile key and Redis expires the key after you
WATCHed it, ``EXEC`` will still work. More on this.)

``WATCH`` can be called multiple times. Simply all the ``WATCH`` calls
will have the effects to watch for changes starting from the call, up to
the moment ``EXEC`` is called. You can also send any number of keys to a
single ``WATCH`` call.

When ``EXEC`` is called, all keys are UNWATCHed, regardless of whether
the transaction was aborted or not. Also when a client connection is
closed, everything gets UNWATCHed.

It is also possible to use the ``UNWATCH`` command (without arguments)
in order to flush all the watched keys. Sometimes this is useful as we
optimistically lock a few keys, since possibly we need to perform a
transaction to alter those keys, but after reading the current content
of the keys we don't want to proceed. When this happens we just call
UNWATCH so that the connection can already be used freely for new
transactions.

Cómo usar *WATCH* para implementar *ZPOP*
-----------------------------------------

A good example to illustrate how ``WATCH`` can be used to create new
atomic operations otherwise not supported by Redis is to implement
``ZPOP``, that is a command that pops the element with the lower score
from a sorted set in an atomic way. This is the simplest implementation:

::

   WATCH zset
   element = ZRANGE zset 0 0
   MULTI
   ZREM zset element
   EXEC

If ``EXEC`` fails (i.e. returns a Null reply) we just repeat the
operation.

Fuentes y más información:

-  `Beyond the Cache with Python - Using Redis and Python for everything
   but
   caching! <https://redislabs.com/blog/beyond-the-cache-with-python/>`__

Cómo implementar un sistema de colas y trabajadores con Redis
-----------------------------------------------------------------------

Una cola de mensajes proporciona un mecanismo de comunicación asíncrono
entre el emisor y el receptor del mensaje, de forma que no interactúan
entre ellos sino con el sistema de colas en si. Los mensajes enviados a
una cola se almacenan en esta hasta que el receptor las acepte.

La cola de mensajes es un pariente del patrón ``PUB-SUB``. Este patrón
permite a los emisores de los mensajes, llamados en este escenario
**publicadores** (*publishers*) publicar mensajes en un **canal**, que
los receptores, llamados aquí **suscriptores** (*suscribers*), si los
hubiera, recibirían si previamente se han suscrito a dicho canal. En
este caso, el mensaje puede ser entregado a cero, uno o más
suscriptores, sin que el emisor tenga control algunos sobre ello. En un
sistema de colas, sin embargo, el mensaje no desaparece, sino que se
almacena hasta que algún suscriptor lo acepte. Redis tiene un mecanismo
PUB-SUB, que podemos combinar con una lista para construir un sistema de
colas.

Veamos primero como usar una lista en Redis. Las listas son simplemente
una lista de cadenas de texto, que están ordenadas según el orden de
inserción. Podemos añadir una cadena nueva al final de la lista, con la
orden ``LPUSH``, o al principio, con ``RPUSH``.

::

   LPUSH mylist a   # Ahora la lista es "a"
   LPUSH mylist b   # Ahora la lista es "b","a"
   RPUSH mylist c   # Ahora la lista es "b","a","c" (se usó RPUSH)

Una opción muy interesante dentro de las operaciones soportadas por las
listas en Redis son las ordenes bloqueantes ``BLPOP`` (*Blocking Left
Pop*) y ``BRPOP`` (*Blocking Right Pop*), que respectivamente extraen
elementos de la izquierda o derecha de la lista, pero que se bloquean si
la lista está vacía.

Para ver un ejemplo de como funciona, abre tres terminales y ejecuta un
cliente de redis (``redis-cli``) en cada una de ellas. En las dos
primeras ejecuta:

::

   BLPOP workqueue 0

Que significa “Dame el primer elemento de la lista llamada
``workqueue``, y si no lo hubiera, espera por un tiempo indefinido hasta
que haya un valor disponible. El :math:`0` indica el *timeout* en
segundos, donde el valor especial de :math:`0` significa que debe
esperar por siempre.

En la tercera terminal, ejecuta estos dos sentencias:

::

   LPUSH "Hola"
   LPUSH "Mundo"

Una vez añadidos los dos elementos a la lista en la tercera terminal,
vemos que cada uno de los otros dos clientes recibieron un valor.

Implementando una colas de trabajos simple
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vamos a implementar primero al consumidor, y lo probaremos usando el
cliente básico de Redis.

.. code:: python

.. include: source/redis-subscriber.py

El siguiente paso es crear un repartidor de trabajos, vamos a hacer un
*script* que envíe varios trabajos a esta cola. Le pasaremos como
parámetro opcional el número de la primera tarea (por defecto 1) para
poder ver como los trabajos se distribuyen entre los diferentes
suscriptores:

.. code:: python

   --8<--
   notes/redis-publisher.py
   --8<--

Podemos ahora abrir varios suscriptores y varios publicadores y podemos
ver como la carga de trabajos se distribuye de forma equitativa entre
ellos, no se pierde ningún trabajo y nunca acaba un trabajo a la vez en
dos suscriptores.

Esta implementación puede quedarse un poco corta, especialmente en el
caso de que alguno de los suscriptores falle al procesar el trabajo por
la razón que sea, quedando por tanto el proceso sin ejecutar.

Las ordenes de Redis ``RPOPLPUSH`` y ``BRPOPLPUSH`` están pensadas para
resolver este problema, usando una segunda cola específicamente para
almacenar los trabajos mientras están siendo procesados.

Si el *worker* finaliza correctamente, quita el trabajo de la segunda
cola. En caso de que falle, el trabajo se quedaría eternamente en la
segunda cola, pero se puede implementar un proceso que periódicamente
revise los trabajos que llevan demasiado tiempo en la segunda cola sin
ser terminados, y los pase de nuevo a la primera cola para que otro
trabajador tenga la oportunidad de procesarlo.

El siguiente paso, si esto se queda corta, seria usar una librería como
`rq <https://pypi.org/project/rq/>`__, o algo incluso más complejo como
`rabbit-mq <https://www.rabbitmq.com/>`__.

Fuentes:

-  `Implement Job Queue using Redis - Mohammed Hewedy -
   Medium <https://mohewedy.medium.com/implement-job-queue-in-redis-9f0f8d394561>`__

-  `Redis <https://redis.io/>`__

-  `rq <https://pypi.org/project/rq/>`__

-  `rabbit-mq <https://www.rabbitmq.com/>`__
