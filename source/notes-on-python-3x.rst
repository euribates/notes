Python 3.*
========================================================================

Novedades en Python 3.xx

Advanced unpacking
-----------------------------------------------------------------------

En Python se puede hacer esto:

.. code:: python

    a, b, c = range(3)
    assert a == 0
    assert b == 1
    assert c == 2

Pero en Python 2 el número de elementos en ambos lados debe coincidir:

.. code:: python

    a, b, c = range(4)

Produce:

.. code::

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ValueError: too many values to unpack (expected 3)

Ahora, en Python 3 se puede usar esta versión extendida:

.. code:: python

    a, b, *c = range(4)
    assert a == 0
    assert b == 1
    assert c == [2, 3]

El elemento con el asterisco, que intenta atrapar todos los elementos que
pueda, puede aparecer en cualquier parte:

.. code:: python

    a, *b, c = range(5)
    assert a == 0
    assert b == [1, 2, 3]
    assert c == 4

Para obtener el último elemento de la lista:

.. code:: python

    *a, b = range(10)
    assert b == 9
    assert a == [0, 1, 2, 3, 4, 5, 6, 7, 8]


Excepciones encadenadas
------------------------------------------------------------------------

En Python 2, se puede capturar una excepción, hacer algo y luego elevar otra
excepción diferente:

.. code:: python

    def mycopy(source, dest):
        try:
            shutil.copy2(source, dest)
        except OSError: # We don't have permissions. More on this later
            raise NotImplementedError("No permissions")

El problema es que se perdía el contexto de la excepción original,
especialmente la traza de ejecución (*traceback*).

.. code:: python

    >>> mycopy('noway', 'noway2')
    >>> mycopy(1, 2)
    
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<stdin>", line 5, in mycopy
    NotImplementedError: No permissions

Originalmente era una excepción de tipo ``OSError``, pero esa información
ha desaparecido. Asumimos que el problema iba a ser un tema de permisos,
pero en realidad puede producirse cualquier tipo de error: no existe el
fichero, es un directorio, no un fichero, error de tipo de datos (como en
el ejemplo), etc.

Ahora podemos incorporar la información de la excepción original
usando la sintaxis ``raise ... from``:

.. code:: python

    raise NotImplementedError from OSError

La salida es algo similar a:

.. code::

    OSError
    The above exception was the direct cause of the following exception:
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    NotImplementedError

La implementación podría quedar así:

.. code:: python

    def mycopy(source, dest):
        try:
            shutil.copy2(source, dest)
        except OSError as err:
            raise NotImplementedError("No permissions") from err


Iteradores por todos lados
-----------------------------------------------------------------------

En Python 3, ``range``, ``zip``, ``map``, ``dict.values``, etc. son
todos iteradores. Si se necesita una lista, hay que envolver el interador
con una llamada a ``list``. Aquí se ha seguido el principio de **explícito
es mejor que implícito**. De esta forma, se dificulta el escribir código
que utilice accidentalmente demasiada memoria, porque la entrada es mayor
de lo esperado.

Cómo usar ``yield from``
-----------------------------------------------------------------------

Muy útil si se usan generadores. En vez de escribir:

.. code:: python

    for i in gen():
        yield i

Podemos escribir simplemente:

.. code:: python

    yield from gen()

Facilita convertiir cualquier cosa en un generador. En vez de:

.. code:: python

    def duplicate(n):
        A = []
        for i in range(n):
            A.extend([i, i])
        return A

Podemos convertir esto en un generador:

.. code:: python

    def dup(n):
        for i in range(n):
            yield i
            yield i

E incluso mejor:

.. code:: python

    def dup(n):
        for i in range(n):
            yield from (i, i)

*Data Classes* (3.7)
-----------------------------------------------------------------------

One of the most tedious parts about working with Python prior to 3.7 in
an object-oriented way was creating classes to represent data in your
application.

Prior to Python 3.7, you would have to declare a variable in your class,
and then set it in your ``__init__`` method from a named parameter. With
applications that had complex data models, this invariably led to a
large number of boilerplate model and data contract code that had to be
maintained.

Since 3.7 you have access to a decorator called ``@dataclass``, that
automatically adds an implicit ``__init__`` function for you when you
add typings to your class variables. When the decorator is added, Python
will automatically inspect the attributes and typings of the associated
class and generate an ``__init__`` function with parameters in the order
specified:

.. code:: python

    from typing import List
    from dataclasses import dataclass, field

    @dataclass
    class Vector:
        name: str
        id: str
        bars: List[str] = field(default_factory=list)


Uso:

.. code:: python

    a_foo = Foo("My foo’s name", "Foo-ID-1", ["1","2"])

Data classes add automatically the next dunder methods (unless explicity
defind):

- a ``__init__()`` method

- a ``__repr__()`` method. The generated repr string will have the class
name and the name and repr of each field, in the order they are
defined in the class.

- an ``__eq__()`` method. This method compares the class as if it were a
tuple of its fields, in order. Both instances in the comparison must
be of the identical type.

- ``__lt__()``, ``__le__()``, ``__gt__()``, and ``__ge__()`` methods.
These compare the class as if it were a tuple of its fields, in order.
Both instances in the comparison must be of the identical type. If
order is true and eq is false, a ``ValueError`` is raised.

You can still add class methods to your data class, and use it like you
would any other class.

Make format string to use repr instead of str
---------------------------------------------

Since Python 3.6, we can use f-Strings: A new and improved way to format
Strings. Also called **formatted string literals**, f-strings are string
literals that have an ``f`` at the beginning and curly braces containing
expressions that will be replaced with their values:

.. code:: python

    >>> a = 3
    >>> print(f"Value of a plus 1 is {a + 1}")
    Value of a plus 1 is 4

You can make the f-string to represent using the ``repr`` function
adding a ``!r`` postfix in the expresion inside the ``{`` and ``}``. For
example:

.. code:: python

    >>> msg = "Hello, world"
    >>> print(f"Message is {msg!r}")
    Message is 'Hello, world'

Also, in python 3.8 you can add a ``=`` symbol to the end of an f-string
expression, that prints the text of the f-string expression itself,
followed by the value:

.. code:: python

    >>> x = 3
    >>> print (f'{x+1=}')
    x+1=4

Logging usando f-strings
-----------------------------------------------------------------------

Es mejor **no usar** *f-strings* con la librería ``logging``. Asi que en vez de:

.. code:: python

    logging.info(f"User {user_id!r} logged in")

Es mejor (por el momento):

.. code:: python

    logging.info("User %r logged in", user_id)

.. note:: Hay que recalcar que esto no es usar el operador ``%``
    sino usar una coma parapasar parámetros adicionales. Si usaramos
   el operador ``%`` tendríamos exactamente los mismos problemas
   que tenemos con las *f-strings*.

Las razones de hacerlo así:

- Dependiendo del nivel del *log*, se puede evitar la conversión a
  ``str`` de los objetos. La documentación indica que "El formateo de
  los argumentos del mensaje se *difiere* hasta que sea inevitable". Por
  ejemplo, si el nivel de registro es `WARNING` y llamamos a `info`, los
  sistemas de *log* ignorarán la operación de formateo, ya que es
  inútil; el mensaje se ignorará.

- Usar `%r` en los mensajes de registro usará `__repr__`, que a menudo
  es preferible a solo `__str__`.

- Si implementamos nuestros propios controladores, podríamos acceder
  a los valores de los objetos pasados a la llamada de depuración. Si
  solo pasamos cadenas preformateadas, esta opción se pierde.

.. code:: python

    import logging
    log = logging.getLogger()

    err = ZeroDivisionError("Can't divide by zero, you barmpot")
    log.error("Error: %s", err)
    log.error("Error: %r", err)

produce:

.. code::

    Error: Can't divide by zero, you barmpot
    Error: ZeroDivisionError("Can't divide by zero, you barmpot")

En este caso obtenemos el nombre de la excepción, además del mensaje.


Variables de contexto (3.7)
-----------------------------------------------------------------------

Al usar las funciones ``async``/``await`` en el bucle de eventos de Python
antes de la versión 3.7, los administradores de contexto que usaban
variables locales de subproceso podían filtrar valores entre ejecuciones,
lo que podía generar errores difíciles de detectar.

A partir de Python 3.7 se introduce el concepto de **variables de
contexto**, que son variables que tienen valores diferentes según su
contexto. Son similares a las variables locales de subproceso en que
pueden tener valores diferentes, pero en lugar de diferir entre
subprocesos de ejecución, difieren entre contextos de ejecución y, por lo
tanto, son compatibles con las funciones ``async`` y ``await``.

A continuación, se muestra un ejemplo rápido de cómo establecer y usar una
variable de contexto en Python 3.7. Observe que, al ejecutar esto, la
segunda llamada async produce el valor predeterminado, ya que se evalúa en
un contexto diferente:

.. code:: python

    import contextvars
    import asyncio

    val = contextvars.ContextVar("val", default="0")

    async def setval():
        val.set("1")

    async def printval():
        print(val.get())

    asyncio.run(setval()) # sets the value in this context to 1
    asyncio.run(printval()) # prints the default value “0” as its a different context

Cada llamada a ``run`` muestra valores diferentes, porque el contexto es diferente.


Unión de diccionarios (3.9)
-----------------------------------------------------------------------

Ahora se puede usar el operador ``|`` para mezclar los valores de dos
diccionarios ``a`` and ``b``:

.. code:: python

    a = {1: 'a', 2: 'b', 3: 'c'}
    b = {4: 'd', 5: 'e'}
    c = a | b
    print(c)

Produce:

.. code::

    {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}

Y también tenemos el operador ``|=``, que actualizará los valores del
diccionario original:

.. code:: python

    a = {1: 'a', 2: 'b', 3: 'c'}
    b = {4: 'd', 5: 'e'}
    a |= b
    print(a)

Produce:

.. code::

    {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}

Como se puede ver, para cualquier entrada que esté a la vez en los dos
diccionarios, tendrá preferencia el valor del segundo.

Actualización de diccionarios con iteradores (3.9)
-----------------------------------------------------------------------

El operador ``|=`` tiene ahora una nueva funcionalidad que permite
actualizar un diccionario usando un iterable que proporcione parejas de
clave / valor, como una lista o un generador:


.. code:: python

    a = {'a': 'one', 'b': 'two'}
    b = ((i, i**2) for i in range(3))
    a |= b
    print(a)

Produce:

.. code::

    {'a': 'one', 'b': 'two', 0: 0, 1: 1, 2: 4}

Si intentamos hacer esto usando el operador ``|`` nos dará un error, ya que
solo se permite la unión entre diccionarios.

Fuentes:

- `New Features in Python 3.9 \| Towards Data Science <https://towardsdatascience.com/new-features-in-python39-2529765429fe>`_


String Methods (3.9)
-----------------------------------------------------------------------

Hay un par de métodos nuevos en la clase ``str``, que pueden ser
moderadamente útiles: ``removeprefix`` y ``removesuffix`` (Que no son
nombres de irreductibles guerreros galos, pese a las apariencias). Son
métodos que recortan prefijos o sufijos.

.. code:: python

    "Hello world".removeprefix("He")

Produce:

.. code::

    "llo world"

Mientras que:

.. code:: python

    "Hello world".removesuffix("ld")

Produce:

.. code::

    "Hello wor"

Cómo "Disparar y olvidares" con async
-----------------------------------------------------------------------

According to python docs for ``asyncio.Task`` it is possible to start
some coroutine to execute "in background". The task created by
``asyncio.create_task`` function won’t block the execution (therefore
the function will return immediately!). This acts like a way to “fire
and forget”.

An example:

.. code:: python

    import asyncio

    async def async_foo():
        print("FOO: async_foo started")
        await asyncio.sleep(1)
        print("FOO: async_foo done")

    async def main():
        asyncio.create_task(async_foo())  # fire and forget async_foo()
        # btw, you can also create tasks inside non-async funcs
        print('MAIN: Do some actions 1')
        await asyncio.sleep(1)
        print('MAIN: Do some actions 2')
        await asyncio.sleep(1)
        print('MAIN: Do some actions 3')
    
    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

Produce:

.. code::

    MAIN: Do some actions 1
    FOO: async_foo started
    MAIN: Do some actions 2
    FOO: async_foo done
    MAIN: Do some actions 3

Note: **What if tasks are executing after event loop complete?** Asyncio
expects task would be completed at the moment event loop completed. So
if you’ll change ``main()`` to:

.. code:: python

    async def main():
        asyncio.create_task(async_foo())  # fire and forget
        print('MAIN: Do some actions 1')
        await asyncio.sleep(0.001)
        print('MAIN: Do some actions 2')

You can see the task is killed (It never prints the "done" message)
before it finished:

.. code::

    MAIN: Do some actions 1
    FOO: async_foo started
    MAIN: Do some actions 2

To prevent that you can just await all pending tasks after event loop
completed:

.. code:: python

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

        # Let's also finish all running tasks:
        pending = asyncio.Task.all_tasks()
        loop.run_until_complete(asyncio.gather(*pending))

Output now is:

.. code:: python

    MAIN: Do some actions 1
    FOO: async_foo started
    MAIN: Do some actions 2
    FOO: async_foo done

What if I want to Kill tasks instead of awaiting them? For example, some
tasks may be created to run forever. In that case, you can just
``cancel()`` them instead of awaiting them:

.. code:: python

    import asyncio
    from contextlib import suppress

    async def echo_forever():
        while True:
            print("echo")
            await asyncio.sleep(1)

    async def main():
        asyncio.create_task(echo_forever())  # fire and forget
        print('Do some actions 1')
        await asyncio.sleep(1)
        print('Do some actions 2')
        await asyncio.sleep(1)
        print('Do some actions 3')

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

        # Let's also cancel all running tasks:
        pending = asyncio.Task.all_tasks()
        for task in pending:
            task.cancel()
        # Now we should await task to execute it's cancellation.
        # Cancelled task raises asyncio.CancelledError that we can suppress:
        with suppress(asyncio.CancelledError):
            loop.run_until_complete(task)


Expresiones de asignación o el infausto "Operador Morsa" (3.8)
-----------------------------------------------------------------------

Hay un nuevo operador ``:=`` que asigna valores a variables como parte
de una expresión mayor. Se le conoce cariñosamente como **el operador
morsa** debido a su parecido con los ojos y colmillos de una morsa.

Antes de Python 3.8:

.. code:: python

    if len(a) > 10:
        print(f"Too many elements ({len(a)}), expected <= 10)")

Este código llama a ``len(a)`` dos veces. Podemos hacerlo con una
sola llamada:

.. code:: python

    m = len(a)
    if n > 10:
        print(f"Too many elements ({n}), expected <= 10)")

Desde python 3.8 podremos usar el operador morsa para realizar el cálculo
y la asignación en una sola línea:

.. code:: python

    if (n := len(a)) > 10:
        print(f"Too many elements ({n}), expected <= 10)")

El caso típico implica tener que evaluar una expresión regular dos veces,
una para determinar si hay una ocurrencia y otras para extraer subgrupos:

.. code:: python

    discount = 0.0
    if (match := re.search(r'(\d+)% discount', ad)):
        discount = float(match.group(1)) / 100.0

También resulta útil en bucles *white* que calculan un valor
para determinar el final del bucle y a la vez necesitan usar ese
valor en el cuerpo:

.. code:: python

    # Loop over fixed length blocks
    while (block := f.read(256)) != '':
        process(block)

También se puede usar en compresión de listas, donde se quiere
usar un valor calculado en la parte del filtrado también en el
cálculo del valor final:

.. code:: python

    result = [
        clean_name.title()
        for name in names
        if (clean_name := normalize('NFC', name)) in allowed_names
        ]

Se recomienda usar el operador morsa solo en aquellos casos en los
que se reduce la complejidad **y** se mejora la legibilidad.


New module for getting metadata on packages
-------------------------------------------

The new ``importlib.metadata`` module provides (provisional) support for
reading metadata from third-party packages. For example, it can extract
an installed package’s version number, list of entry points, and more:

# Note following example requires that the popular "requests" # package
has been installed.

.. code:: python

    from importlib.metadata import version, requires
    assert version('requests') == '2.24.0'
    assert len(requires('requests')) == 6

Changes in asyncio module
-------------------------

The ``asyncio.run()`` function has graduated from the provisional to
stable API. This function can be used to execute a coroutine and return
the result while automatically managing the event loop. For example:

.. code:: python

    import asyncio

    async def main():
        await asyncio.sleep(0)
        return 42

    asyncio.run(main())

This is roughly equivalent to:

.. code:: python

    import asyncio

    async def main():
        await asyncio.sleep(0)
        return 42

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        asyncio.set_event_loop(None)
        loop.close()

The actual implementation is significantly more complex. Thus,
``asyncio.run()`` should be the preferred way of running asyncio
programs.

Running ``python -m asyncio`` launches a natively async REPL. This
allows rapid experimentation with code that has a top-level await. There
is no longer a need to directly call ``asyncio.run()`` which would spawn
a new event loop on every invocation:

.. code:: shell

    ▶ python -m asyncio
    asyncio REPL 3.10.4 (main, Jun 29 2022, 12:14:53) [GCC 11.2.0] on linux
    Use "await" directly instead of "asyncio.run()".
    Type "help", "copyright", "credits" or "license" for more information.


New decorator for cached properties
-----------------------------------------------------------------------

Added a new ``functools.cached_property()`` decorator, for computed
properties cached for the life of the instance:

.. code:: python

    import functools
    import statistics

    class Dataset:

        def __init__(self, sequence_of_numbers):
            self.data = sequence_of_numbers

        @functools.cached_property
        def variance(self):
            return statistics.variance(self.data)


New decorator to convert methods into generic functions
-----------------------------------------------------------------------

New decorator ``functools.singledispatchmethod`` to convert methods into
`generic
functions <https://docs.python.org/3/glossary.html#term-generic-function>`__
using `single
dispatch <https://docs.python.org/3/glossary.html#term-single-dispatch>`__:

.. code:: python

    import functools
    import typing

    class Negator:

        @functools.singledispatchmethod
        def neg(self, arg):
            raise NotImplementedError(f"Cannot negate {a!r}")

        @neg.register
        def _(self, arg: str) -> str:
            return arg[::-1]

        @neg.register
        def _(self, arg: float) -> float:
            return -arg

        @neg.register
        def _(self, arg: int) -> int:
            return -arg

        @neg.register
        def _(self, arg: bool) -> bool:
            return not arg

    nope = Negator()
    assert nope.neg("Hola") == "aloH"
    assert nope.neg(-1) == 1
    assert nope.neg(432.22) == -432.22
    assert nope.neg(True) is False


The Inspect module
-----------------------------------------------------------------------

The ``inspect.getdoc()`` function can now find docstrings for
``__slots__`` if that attribute is a ``dict`` where the values are
docstrings. This provides documentation options similar to what we
already have for ``property()``, ``classmethod()``, and
``staticmethod()``:

.. code:: python

    class AudioClip:

        __slots__ = {
            'bit_rate': 'expressed in kilohertz to one decimal place',
            'duration': 'in seconds, rounded up to an integer',
            }

        def __init__(self, bit_rate, duration):
            self.bit_rate = round(bit_rate / 1000.0, 1)
            self.duration = ceil(duration)


Force the logging to reload the basic configuration
-----------------------------------------------------------------------

Added a ``force`` keyword argument to ``logging.basicConfig()``. When
set to ``True``, any existing handlers attached to the root logger are
removed and closed before carrying out the configuration specified by
the other arguments.

This solves a long-standing problem. Once a logger or ``basicConfig()``
had been called, subsequent calls to ``basicConfig()`` were silently
ignored. This made it difficult to update, experiment with, or teach the
various logging configuration options using the interactive prompt or a
Jupyter notebook.

Function annotations (3.5)
-----------------------------------------------------------------------

We can now annotate (document) parameters and results for functions and
methods:

.. code:: python

    def f(a: stuff, b: stuff = 2) -> result:
        ...

Annotations can be arbitrary Python objects. Python doesn’t do anything
with the annotations other than put them in an ``__annotations__``
dictionary:

.. code:: python

    >>> def f(x: int) -> float:
    ...     pass
    ...
    >>> f.__annotations__
    {'return': <class 'float'>, 'x': <class 'int'>}


But it leaves open the possibility for library authors to do fun things.
Example, IPython 2.0 widgets. Run IPython notebook (in Python 3) from
IPython git checkout and open
http://127.0.0.1:8888/notebooks/examples/Interactive%20Widgets/Image%20Processing.ip

Optional Underscores in Numeric Literals (3.6)
-----------------------------------------------------------------------

Since Python 3.6 the languague has the ability to use underscores in
numeric literals for improved readability. For example:

.. code:: python

    >>> 1_000_000_000_000_000
    1000000000000000
    >>> 0x_FF_FF_FF_FF
    4294967295

Single underscores are allowed between digits and after any base
specifier. Leading, trailing, or multiple underscores in a row are not
allowed.

The string formatting language also now has support for the '\_' option
to signal the use of an underscore for a thousands separator for
floating point presentation types and for integer presentation type 'd'.
For integer presentation types 'b', 'o', 'x', and 'X', underscores will
be inserted every 4 digits:

.. code:: python

    >>> '{:_}'.format(1000000)
    '1_000_000'
    >>> '{:_x}'.format(0xFFFFFFFF)
    'ffff_ffff'


The ``pathlib`` Module (3.4)
-----------------------------------------------------------------------

The ``pathlib`` module makes easier to work with directories and files.
pathlib has been described as an object-oriented way of dealing with
paths. Rather than working with strings, you work with "Path" objects,
which not only allows you to use all of your favorite path- and
file-related functionality as methods, but it also allows you to paper
over the differences between operating systems.

Instead of doing:

.. code:: python

    file_name = 'debug.log'
    full_path = '/tmp/workdir/{file_name}'

We can do:

.. code:: python

    from pathlib import Path

    base_dir = Path('/tmp/workdir')
    full_path = base_dir / 'debug.log'

In the first example, the code can fail if executed in a windows
environment. This is usually fixed using ``os.path.join`` and
``os.path.sep``. The second example looks like its making the same
error, but it's not the case: We create a ``Path`` object using a
standar syntax, and the library choose the right Path class to use based
on the underlying O/S.

Path objects allows you to represent files or directories. If you're not
sure what kind of object you have, you always can ask it, with the
``is_dir`` and ``is_file`` methods:

.. code:: python

    >>> p1 = pathlib.Path('config.py')
    >>> p1.is_file(), p1.is_dir()
    (True, False)
    >>> p2 = pathlib.Path('.')
    >>> p2.is_file(), p2.is_dir()
    (False, True)

You can also check that the file or dir really exists with the
``exists`` method:

.. code:: python

    p2 = pathlib.Path('Supercalifragilisticexpialidocious')
    assert p2.exists() is False

You can use the ``/`` operator, normally used for division, to join
paths together. For example:

.. code:: python

    >>> dirname = pathlib.Path('/foo/bar')
    >>> dirname / filename
    PosixPath('/foo/bar/abc.txt')

It takes a bit of time to get used to seeing ``/`` between what you
might think of as strings. But remember that ``dirname`` isn't a string;
rather, it’s a ``Path`` object. And ``/`` is a Python operator, which
means that it can be overloaded and redefined for different types.

Working with Directories
~~~~~~~~~~~~~~~~~~~~~~~~

If your ``Path`` object contains a directory, there are a bunch of
directory-related methods that you can run on it.

For example, to find all of the files in the current directory:

.. code:: python

    >>> p = pathlib.Path('.')
    >>> p.iterdir()
    <generator object Path.iterdir at 0x111e4b1b0>

``Path`` objects have also the ``glob`` method. Like ``iterdir``, the
``glob`` method returns a generator, meaning that you can use it in a
for loop. For example, to find all the python files in the current dir
and subdirs, we can do:

.. code:: python

    >>> for one_item in p.glob('**/*.py'):
    ...     print(f"{one_item}: {type(one_item)}")


Simpler customization of class creation (3.6)
-----------------------------------------------------------------------


It is now possible to customize subclass creation without using a
metaclass. The new ``__init_subclass__`` classmethod will be called on
the base class whenever a new subclass is created:

.. code:: python

    class PluginBase:
        subclasses = []

        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
            cls.subclasses.append(cls)

    class Plugin1(PluginBase):
        pass

    class Plugin2(PluginBase):
        pass

Fuente: `PEP 487`_.

.. _PEP 487: https://peps.python.org/pep-0487/
