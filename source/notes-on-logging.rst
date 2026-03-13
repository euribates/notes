Logging
========================================================================

Cuáles son los componentes principales de un sistema de *logging*
------------------------------------------------------------------------

El sistema de *logging* de Python está organizado en torno a cuatro
abstracciones principales: *Loggers*, Niveles, Manejadores o *Handler* y
Formateadores o *Formatters*. Cada uno de ellos tiene una función
específica. El conjunto de todos ellos determina cómo se clasifican,
enrutan y formatean los mensajes.

- Los *loggers* son el punto de entrada del sistema. Exponen los métodos
  ``debug()``, ``info()``, ``warning()``, ``error()`` y ``critical``, que
  son los que nos permiten enviar mensajes.  Se estructuran en forma de
  jerarquía de nombres (por ejemplo, ``app.module.submodule``), y tienen
  un nivel asociado, que filtra los mensajes que se procesan. 

- Los **niveles** controlan qué mensajes son aceptados y cuales son
  descartados, en base a la gravedad del mensaje (por ejemplo,
  ``CRÍTICA``). Los mensajes por debajo de un determinado nivel son
  ignorados, Los de nivel igual o superior son procesados. Los niveles
  están asociado con los *loggers**, pero también con los *handlers*.
  Podría pasar que un *logger* deje pasar un mensaje de aviso, porque su
  nivel es, por ejemplo, ``WARNING``, pero que un *handler* asociado a
  este *logger* lo ignore porque tiene el nivel ``ERROR``.

- Los **manejadores** o *handlers* determinan a dónde va un mensaje de
  registro. Esto incluye flujos de consola, archivos, archivos giratorios,
  *blogs*, correo electrónico, *sockets* de red, *búferes de memoria* o
  colas. Se pueden adjuntar múltiples *handlers* al mismo *logger*, y cada
  uno puede tener su propio formateador y su propio nivel de gravedad.

- Los formateadores controlan cómo se representan los mensajes de registro
  y pueden incluir metadatos (por ejemplo, marcas de tiempo, módulo,
  número de línea, hilo o ID de proceso). También permiten plantillas de
  cadena personalizadas o formatos estructurados como JSON. Cada
  *handler* puede usar un formateador diferente para producir múltiples
  estilos de salida para el mismo mensaje.


Cómo funciona a grandes rasgos el sistema de *logging*
------------------------------------------------------------------------

El proceso empieza cuando un desarrollados llama a alguno de los métodos
del *logger*, por ejemplo ``info("hola, mundo")``. El *logger* en primer
lugar determina el nivel del mensaje. Si el nivel del mensaje es igual o
superior a su propio nivel, el mensaje es aceptado, si no, se descarta.
En caso de ser aceptado, se crea un registro de tipo ``LogRecord`` que
contiene el mensaje y los metadatos.

Este objeto de tipo ``LogRecord`` se le pasa a todos los *handlers* que
estén vinculados con el *logger*. Como los *handlers* tienen sus propios
niveles, el mensaje puede ser aceptado o descartado en función del nivel.

Si es aceptado, el ``LogRecord`` se la pasa al formateador para que este
lo procese y lo convierta en una cadena de texto. Finalmente, el registro
es emitido a su destino por el *handler*.

Si la propagación está habilitada, el ``LogRecord`` puede continuar de los
*loggers* hijos hacia los *loggers* padres padres, repitiendo el proceso
con sus controladores.

Cuáles son los niveles de severidad del sistema de *logging*
------------------------------------------------------------------------

Python define seis niveles iniciales: ``NOTSET``, ``DEBUG``, ``INFO``,
``WARNING``, ``ERROR`` y ``CRITICA``. Cada uno de estos niveles implica un
determinado caso de uso, y define la importancia del mensaje. Los niveles
nos permite realizar un filtrado de los mensajes.

- ``NOTSET`` (0): Este nivel se usa para indicar que el nivel no ha sido
  definido explicitamente. Por tanto, su valor nominal es cero, pero
  hereda el nivel de su *logger* padre. No es muy frecuente usarlo, pero
  tiene su utilida al permitir definir el nivel de una librería para que
  asuma el nivel definido externamente.

- ``DEBUG`` (10): Se usa para inspeccionar estados internos, control de
  flujo, valores de las variables, etc. que sean de interes para el
  desarrollador. Se usa frecuentemente en las fases de desarrollo. 

- ``INFO`` (20): Se usa para describir operaciones de interés pero que
  sean parte de la mecánica operacional del sistema, como por ejemplo "El
  usuario menganito se ha conectado" o "La copia de seguridad ha
  terminado". Los administradores del sistema puede utilizar los mensajes
  de nivel ``INFO`` para monitorizar actividad y rendimiento.

- ``WARNING`` (30): Es un aviso para los desarrolladores y administradores
  de que algo extraño ha pasado, o que existe una condición que puede
  causar daños futuros. A pesar de eso, la aplicación puede seguir
  funcionando sin problema. Un ejemplo podría ser "El espacio ocupado en
  disco está por encima del 90%", o "Falta un valor en el fichero de
  configuración, se usará el valor por defecto".

- ``ERROR`` (40): Un mensaje de error, que impide que el programa en su
  totalidad o una parte de el no puede ejecutarse como se esperaba.
  Normalmente, este tipo de situaciones afectan la lógica del programa o
  el funcionamiento de ciertas operaciones críticas, como la falta de un
  fichero de configuración, o la imposibilidad de conectarse con una base
  de datos.

- ``CRITICAL`` (50): El más alto de los niveles, un mensaje crítico
  implica un fallo importante, que puede comprometer incluso la integridad
  o seguridad del sistema en su totalida. Normalmente requiere atención
  inmediata.


Cómo configurar un sistema de *logging*
------------------------------------------------------------------------

Existen varias formas, vamos a verlas en orden de complejidad creciente.

Usando el *logger* por defecto
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si empezamos a usar las funciones del módulo ``logging`` directamente, en
la primera llamada realizada en tiempo de ejecución se creará el *logger*
raíz por defecto. El *logger* por defecto está configurado para tener un
único *handler*, que imprime los mensajes (con un formato también asumido
por defecto) a la salida estándar de errores, ``sys.stderr``.

.. code:: python

    import logging
    # Todavía no existe un logger raiz

    logging.info('this info messages is lost, like tears in rain')
    # Esto crea automáticamente, si no existe, un *logger* raiz
    # Pero el nivel por defecto en ``WARNING``, así que el mensaje
    # se descarta

    logging.warning('But this must be printed')
    # Este mensaje si pasa el nivel, así que se envía al *handler*.
    # En el caso de un *logger* creado por defecto, la salida es ``stderr``

    root = logging.getLogger()
    # Si llamamos a la función ``getLogger`` sin pasarle ningún nombre,
    # nos devuelve el *logger* raíz.
    print(root.name)  # Debería ser ``root``


BasicConfig
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Esta es la forma más sencilla de configurar un sistema de *logging* más
complicado que el *logger* por defecto. Solo con la siguiente línea de
código:

.. code:: python

    logging.basicConfig(level="INFO")

Obtenemos un sistema completamente configurado, con un *handler* de tipo
``StreamHandler``, que usa la salida estándar de errores de la consola,
configurado en el nivel ``INFO``. Podemos usar ciertos parámetros que
nos permite personalizar más el sistema:

- ``filename``: Si se utiliza, indica que se debe usar un fichero con
  el nombre indicado para los mensajes, en vez de usar la salida
  estándar.

- ``format`` : Si se especifica, el valor pasado se usará como cadena de
  texto de formato para los mensajes.

- ``datefmt`` : Permite especificar el formato para fechas y *timestamps*.

- ``level`` : Define el nivel del sistema de *logging*.

.. warning:: 

    Es importante hacer notar que ``basicConfig`` **solo funciona la primera
    vez que es invocado** en tiempo de ejecución. Si ya existe un **logger**
    raiz, las llamadas a la función no hacen nada.


Configuración usando DictConfig
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Toda la configuración, incluyendo todos los componentes y como se conectan
entre si se especifica en un diccionario. El diccionario tiene diferentes
secciones para los *loggers*, manejadores, formateadores y algunos
parámetros globales.

Montar el sistema de *logging* a mano
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

POdemos crear el sistema de *logging* de forma totalmente manual, como en 
el siguiente ejemplo:

.. code:: python

    import sys

    new_handler = logging.StreamHandler(sys.stdout)
    new_handler.setLevel(logging.DEBUG)
    root = logging.getLogger()
    root.addHandler(new_handler)

Ahora enviemos un mensaje de tipo ``INFO``:

.. code:: python

    logging.info('ok')
    root.level
    root.setLevel(logging.DEBUG)
    root.level
    logging.info('ok')
    get_ipython().magic(u'copy 1,19')
    get_ipython().run_cell_magic(u'copy', u'1,19', u'')
    get_ipython().run_cell_magic(u'copy', u'', u'')
    get_ipython().run_cell_magic(u'edit', u'', u'')
    get_ipython().magic(u'edit')
    get_ipython().magic(u'edit 1-24')


Cuáles son los *handlers* que vienen de serie?
------------------------------------------------------------------------

- **Consola** (``StreamHandler``): Directo a la consola, o a un objeto
  similar a un fichero (concretamente, cualquier objeto que implemente los
  métodos ``write`` y ``flush``), útil para diagnóstico en tiempo real,
  desarrollo y depurado.

- **Manejador Nulo** (``NullHandler``): Basicamente un *handler* que
  ignora todo tipos de mensajes. Puede ser útil en el caso de desarrollo
  de librerías.

- **Fichero** (``FileHandler``): Para guardar la información en un único
  fichero, sin rotación.

- **Ficheros rotantes** (``RotatingFileHandler``,
  ``TimedRotatingFileHandler``): Para gestionar automáticamente el
  crecimiento de un fichero. Superado un cierto tamaño o un cierto tiempo,
  el nombre del fichero cambia, se empieza a usar un fichero nuevo, y el
  anterior se puede archivar.

- **System logs** (``SysLogHandler``): Para monitorización de sistemas,
  vía Unix *syslog* o *Windows Event Log*.

- **Email** (``SMTPHandler``): Para comunicar por correo electrónico.

- **Network** (``SocketHandler``, ``DatagramHandler``, ``HTTPHandler``):
  Para comunicar los eventos por red, usando TCP o UDP, a servidores
  remotos.

- **Memorias o Colas** (``MemoryHandler``, ``QueueHandler``): Para
  almacenar temporalmente los mensajes en memoria o en un sistema de colas
  de forma que el envio no sea bloqueante y los eventos puedan ser
  procesados más adelante o en otras máquinas.


Como crear tu propia clase de *handler* o manejador
------------------------------------------------------------------------

La forma más sencilla es crear una clase nueva derivandola de un *handler*
ya existente que se parezca más o menos al que queremos hacer.

En el siguiente ejmplo, se deriva de la clase ``StreamHandler``:

.. code:: python

    from logging import StreamHandler
    from mykafka import MyKafka

    class KafkaHandler(StreamHandler):

        def __init__(self, broker, topic):
            StreamHandler.__init__(self)
            self.broker = broker
            self.topic = topic
            # Kafka Broker Configuration
            self.kafka_broker = MyKafka(broker)

        def emit(self, record):
            msg = self.format(record)
            self.kafka_broker.send(msg, self.topic)


Configurando el sistema de *logging* para una librería
------------------------------------------------------------------------

Es importante documentar como usa nuestra librería el sistema de
*logging*. Lo más importante es poder conocer el nombre bajo el que se
registran los *loggers* de la librería.

Si la aplicación que utiliza la librería no utiliza *logging*, pero la
librería si, los eventos de nivel ``WARNING`` o superior se imprimirán por
defecto en ``sys.stderr``.  Este se considera el mejor comportamiento
predeterminado.

Si por alguna razón se desea que estos mensajes no se impriman, se puede
adjuntar un *handler* nulo (Que no hace nada) al *logger* del nivel
superior del sistema de *logging* de la librería.  De esta forma, el
mensaje es capturado y nunca se muestra ninguna salida.

Si el usuario de la biblioteca configura el registro para el uso de la
aplicación, es de suponer que agregará algunos controladores y, si los
niveles están configurados adecuadamente, las llamadas de registro
realizadas en el código de la biblioteca enviarán la salida a esos
controladores, como de costumbre.

Hay un *handler* nulo definido ya en la librería estándar:  ``NullHandler``
(desde Python 3.1). Veamos un ejemplo:

.. code:: python

    import logging
    logging.getLogger('foo').addHandler(logging.NullHandler())


Si lo organización de la librería es más complicada, se puede usar los
nombres de los *loggers* como espacio de nombres: ``orgname.foo``, por
ejemplo, en vez de solo ``foo``.

.. warning::

    Se recomienda encarecidamente que no se agrega **ningún otro handler
    que no sea el handler nulo**. Esto es porque la configuración de los
    controladores es responsabilidad del desarrollador de la aplicación
    que utiliza la biblioteca. El desarrollador conoce a su público
    objetivo y qué controladores son los más adecuados para su aplicación.
    Si se añaden controladores de forma oculta, interferimos con su
    capacidad para realizar pruebas unitarias y entregar registros que se
    ajusten a sus requisitos.

Cómo usar los formateadores (``Formatters``)
------------------------------------------------------------------------

Los formateadores definen cómo se muestra un registro de log (clase
``LogRecord``), y pueden enriquecer el mensaje con metadatos.  Estos
metadatos pueden aportar información adicional útil  para la detección de
errores. Algunos de los metadatos disponibles son:

- **Marcas temporales** ``(%(asctime)s)`` almacenan el momento en en ocurre el evento.
 
- **Nombre del logger**: ``(%(name)s)`` identifica que *logger*, y por tanto, que parte de la aplicación es la que ha geneado este mensaje.
 
- Modules o funciones ``(%(module)s``, ``%(funcName)s)`` identifican especialmente qué función originó el mensaje.

- **Números de línea**: ``(%(lineno)d)``.
- **Identificador del proceso o del hilo**: ``%(thread)d``, ``%(process)d)``.
- **Nivel de severidad**: ``(%(levelname)s)``.


Cuando se necesitan salidas de registro analizables por máquina e
integradas con otras máquinas, los formatos estructurados pueden ser una
buena opción. En tales casos, se puede utilizar JSON o pares clave-valor:

.. code:: python

    '{"time": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'


Using ``LoggerAdapters`` to impart contextual information
------------------------------------------------------------------------

An easy way in which you can pass contextual information to be output
along with logging event information is to use the ``LoggerAdapter``
class. This class is designed to look like a ``Logger``, so that you can
call ``debug()``, ``info()``, ``warning()``, ``error()``,
``exception()``, ``critical()`` and ``log()``. These methods have the
same signatures as their counterparts in ``Logger``, so you can use the
two types of instances interchangeably.

When you create an instance of ``LoggerAdapter``, you pass it a
``Logger`` instance and a dict-like object which contains your
contextual information. When you call one of the logging methods of the
adapter, it delegates the call to the underlying instance of Logger
passed to its constructor, and arranges to pass the contextual
information in the delegated call. Here’s a snippet from the code of
LoggerAdapter:

.. code:: python

    def debug(self, msg, /, *args, **kwargs):
        """
        Delegate a debug call to the underlying logger, after adding
        contextual information from this adapter instance.
        """
        msg, kwargs = self.process(msg, kwargs)
        self.logger.debug(msg, *args, **kwargs)

The ``process()`` method of ``LoggerAdapter`` is where the contextual
information is added to the logging output. It’s passed the message and
keyword arguments of the logging call, and it passes back (potentially)
modified versions of these to use in the call to the underlying logger.
The default implementation of this method leaves the message alone, but
inserts an ``extra`` key in the keyword argument whose value is the
dict-like object passed to the constructor. Of course, if you had passed
an ``extra`` keyword argument in the call to the adapter, it will be
silently overwritten.

The advantage of using ``extra`` is that the values in the dict-like
object are merged into the LogRecord instance’s ``__dict__``, allowing
you to use customized strings with your Formatter instances which know
about the keys of the dict-like object. If you need a different method,
e.g. if you want to prepend or append the contextual information to the
message string, you just need to subclass ``LoggerAdapter`` and override
``process()`` to do what you need. Here is a simple example:

.. code:: python

    class CustomAdapter(logging.LoggerAdapter):
        """
        This example adapter expects the passed in dict-like object to have a
        'connid' key, whose value in brackets is prepended to the log message.
        """
        def process(self, msg, kwargs):
            return '[%s] %s' % (self.extra['connid'], msg), kwargs

which you can use like this:

.. code:: python

    logger = logging.getLogger(__name__)
    adapter = CustomAdapter(logger, {'connid': some_conn_id})

Then any events that you log to the adapter will have the value of
``some_conn_id`` prepended to the log messages.

Source: `logging Cookbook <https://docs.python.org/3/howto/logging-cookbook.html#using-loggeradapters-to-impart-contextual-information>`_
