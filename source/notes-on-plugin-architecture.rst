Plugin architecture
========================================================================

.. tags:: python, development


Notes on plug-in architecture (with Python)
------------------------------------------------------------------------

A plugin architecture could help you to extend the functionality of your
applications without affecting its core structure. The benefits are both
the greater isolation of the core system and easier enlargement of the
functionality of the system (by yourself or others) safely and reliably.

There are disadvantages too, being one of the main ones that you can
only extend the functionality based on the constraints that is imposed
on the plugin placeholder.

There are several methods to create a plugin architecture, here we will
walkthrough the approach using ``importlib``.


The Basic Structure Of A Plugin Architecture
------------------------------------------------------------------------

At its core, a plugin architecture consists of **two components**: a
core system and plug-in modules. The main key design here is to allow
adding additional features that are called plugins modules to our core
system, providing extensibility, flexibility, and isolation to our
application features.

.. code::

    +---------------------+                             +-----------+
    |                     |                             |           |
    |                     |                         +---> Plugin 1  |
    |                     |                         |   |           |
    |                     |                         |   +-----------+
    |                     |                         |
    |                   +-+----------------------+  |   +-----------+
    |       CORE        | |                      |  |   |           |
    |                   | |                      |  |   | Plugin 2  |
    |                   | |   Plugin Subsystem   +<-+--->           |
    |                   | |                      |  |   +-----------+
    |                   | |                      |  |       ...
    |                   +-+----------------------+  |   +-----------+
    |                     |                         |   |           |
    +---------------------+                         +---> Plugin n  |
    |           |
    +-----------+


The Core System
------------------------------------------------------------------------

The core system defines how it operates and the basic business logic. It
can be understood as the workflow, such as how the data flow inside the
application, but, the steps involved inside that workflow is up to the
plugin(s). Hence, all extending plugins will follow that generic flow
providing their customised implementation, but not changing the core
business logic or the application’s workflow.

In addition, it also contains **the common code** being used (or has to
be used) by multiple plugins as a way to get rid of duplicate and
boilerplate code, and have one single structure.


The Plug-in Modules
------------------------------------------------------------------------

On the other hand, plug-ins are **stand-alone, independent** components
that contain, additional features, and custom code that is intended to
enhance or extend the core system. The plugins however, **must follow a
particular set of standards or a framework imposed by the core system**
so that the core system and plugin must communicate effectively.

The independence of each plugin is the best approach to take. It is not
advisable to have plugins talk to each other, unless, the core system
facilitates that communication in a standardized way so that independent
plugins can talk to each other. Either way, it is simpler to keep the
communication and the dependency between plug-ins as minimal as
possible.


Building a Core System
------------------------------------------------------------------------

As mentioned before, we will have a core system and zero or more plugins
which will add features to our system, so, first of all, we are going to
build our core system (we will call this file ``core.py``) to have the
basis in which our plugins are going to work. To get started we are
going to create a class called ``MyApplication`` with a ``run()`` method
which prints our workflow:

.. code:: python

    #core.py

    class MyApplication:

        def __init__(self, plugins:list=[]):
            pass

        def run(self):  # This method will print the workflow of our application
            print("Starting my application")
            print("-" * 10)
            print("This is my core system")
            print("-" * 10)
            print("Ending my application")
            print()

Now we are going to create the main file, which will import our
application and execute the ``run()`` method:

.. code:: python

    # main.py

    from core import MyApplication

    if __name__ == "__main__":
        app = MyApplication()
        app.run()

Once that we have a simple application which prints it's own workflow,
we are going to enhance it so we can have an application which supports
plugins, in order to perform this, we are going to modify the ``init()``
and ``run()`` methods.

The importlib package
------------------------------------------------------------------------

In order to achieve our next goal, we are going to use the ``importlib``
which provide us with the power of implement the import statement in our
``init()`` method so we are going to be able to dynamically import as
many packages as needed. It's these packages that will form our plugins.

This is the code now:

.. code:: python

    # core.py
    import importlib

    class MyApplication:

        def __init__(self, plugins:list=None):
            plugins = plugins or ['default']
            self.plugins = [
                # Import the module and initialise it at the same time
                importlib.import_module(
                    f".{plugin}",
                    package='plugins',
                    ).Plugin()
                for plugin in plugins
                ]

        def run(self):
            print("Starting my application")
            print("package is", __package__)
            print("-" * 10)
            print("This is my core system")
            # We is were magic happens, and all the plugins are going to be printed
            for plugin in self.plugins:
                print(plugin)
                print("-" * 10)
            print("Ending my application")
            print()

The key line is ``importlib.import_modulei`` which imports the package
specified in the first string variable with a ``.py`` extension under
the ``plugins`` directory (specified by ``"plugins"`` package named
argument).

The second thing to note is that we appended ``.Plugin()`` to the
``importlib`` statement. This will allow the plugin to create an
instance of the class, to be stored into ``plugins`` internal variable.

We are now ready to create our first plugin.

Creating default plugin
------------------------------------------------------------------------

Keep in mind that we are going to call all plugins in the same way, so
files have to be named as carefully, in this sample, we are going to
create a ``default`` plugin, so, first of all, we create a new file
called ``default.py`` in the ``plugins`` folder.

Inside this file we are going to create a class called ``Plugin``, which
contains a method called ``process`` (This can also be a static method
in case you want to call the method without instantiating the calls).
It's important that any new plugin class is named the same so that these
can be called dynamically:

.. code:: python

    #deafult.py

    class Plugin:

    def process(self, num1, num2):
        # Some prints to identify which plugin is been used
        print("This is my default plugin")
        print(f"Numbers are {num1} and {num2}")

Let’s now modify just one line in our core.py file so we call the
``process()`` method instead of printing the module object:

.. code:: python

    # core.py
    import importlib

    class MyApplication:

        def __init__(self, plugins:list=None):
            plugins = plugins or ['default']
            self.plugins = [
                # Import the module and initialise it at the same time
                importlib.import_module(
                    f".{plugin}",
                    package='plugins',
                    ).Plugin()
                for plugin in plugins
                ]

        def run(self):
            print("Starting my application")
            print("-" * 10)
            print("This is my core system")
            # Modified for in order to call process method
            for plugin in self.plugins:
                plugin.process(5, 3)
            print("-" * 10)
            print("Ending my application")
            print()

Output as follows:

.. code::

    ▶ ./main.py
    Starting my application
    ----------
    This is my core system
    This is my default plugin
    Numbers are 5 and 3
    ----------
    Ending my application

We have successfully created our first plugin, and it is up and running.
You can see the statement "This is my default plugin" which comes from
the plugin ``default.py`` rather than the ``main.py`` program.

Next Steps
------------------------------------------------------------------------

Using this framework, you can easily extend this to add more plugins
easily. The key is that you don’t need to change the ``core.py`` nor the
``main.py`` which helps to keep your code clean but at the same time
help to extend your application.

To see a more in depth version of this article and more examples, you
can see the full article at PythonHowToProgram.com

Fuentes:

-  `A Plugin Architecture Using ImportLib In Python <https://pythonhowtoprogram.com/a-plugin-architecture-for-using-importlib-in-python-3/>`_
