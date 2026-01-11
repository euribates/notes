Logging
========================================================================

How to Configure your logging schema
------------------------------------------------------------------------

BasicConfig
~~~~~~~~~~~

This is by far the simplest way to configure logging. Just doing
``logging.basicConfig(level="INFO")`` sets up a basic ``StreamHandler``
that will log everything on the ``INFO`` and above levels to the
console. There are arguments to customize this basic configuration. Some
of them are:

- ``filename``: Specifies that a FileHandler should be created, using
the specified filename, rather than a StreamHandler.

- ``format`` : Use the specified format string for the handler.

- ``datefmt`` : Use the specified date/time format.

- ``level`` : Set the root logger level to the specified level.

**Warning** ``basicConfig`` only works **the first time it is called**
in a runtime. If you have already configured your root logger, posterior
calls to ``basicConfig`` will have no effect.

DictConfig
~~~~~~~~~~

The configuration for all elements and how to connect them can be
specified as a dictionary. This dictionary should have different
sections for loggers, handlers, formatters, and some basic global
parameters:

.. code:: python

    import logging
    # root logger doesn't exists

    logging.info('this info messages is lost, like tears in rain')
    # Now root logger exists. But its level by default is WARNING so no messages

    logging.warning('But this must be printed')
    # Default root log send messages to stderr

    root = logging.getLogger()
    # If we pass no name, we get the roor logger
    print(root.name)  # Must be root

Manually
~~~~~~~~

Let’s create a new handler, that outputs by stdout:

.. code:: python

    import sys

    new_handler = logging.StreamHandler(sys.stdout)
    new_handler.setLevel(logging.DEBUG)
    root = logging.getLogger()
    root.addHandler(new_handler)

Now Send an info message:

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


How to create a Custom Logging Handler Class
------------------------------------------------------------------------

To create your custom logging handler class we create a new class that
inherits from an existing handler.

For example, in my code I inherited from StreamHandler which sends logs
to a stream:

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

Configuring Logging for a Library
------------------------------------------------------------------------

When developing a library which uses logging, you should take care to
document how the library uses logging - for example, the names of
loggers used.

Some consideration also needs to be given to its logging configuration.
If the using application does not use logging, and library code makes
logging calls, then (as described in the previous section) events of
severity ``WARNING`` and greater will be printed to ``sys.stderr``. This
is regarded as the best default behaviour.

If for some reason you don’t want these messages printed in the absence
of any logging configuration, **you can attach a do-nothing handler to
the top-level logger for your library**. This avoids the message being
printed, since a handler will always be found for the library’s events:
it just doesn’t produce any output.

If the library user configures logging for application use, presumably
that configuration will add some handlers, and if levels are suitably
configured then logging calls made in library code will send output to
those handlers, as normal.

A do-nothing handler is included in the logging package: ``NullHandler``
(since Python 3.1). An instance of this handler could be added to the
top-level logger of the logging namespace used by the library:

.. code:: python

    import logging
    logging.getLogger('foo').addHandler(logging.NullHandler())

should have the desired effect. If an organisation produces a number of
libraries, then the logger name specified can be ‘orgname.foo’ rather
than just ‘foo’.

.. warning::

    It is strongly advised that you **do not add any handlers other than
    NullHandler to your library's loggers**. This is because the
    configuration of handlers is the prerogative of the application
    developer who uses your library. The application developer knows
    their target audience and what handlers are most appropriate for
    their application: if you add handlers ‘under the hood’, you might
    well interfere with their ability to carry out unit tests and
    deliver logs which suit their requirements.


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
dapter, it delegates the call to the underlying instance of Logger
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
