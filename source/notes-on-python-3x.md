---
title: Notas sobre capacidades nuevas en Python 3
---

## Novedades en Python 3.xx

## Advanced unpacking

You know you can do this in Python:

```python
a, b, c = range(3)
assert a == 0
assert b == 1
assert c == 2
```

But the arity on both sides must be equal, so this fails:

```python
a, b, c = range(4)
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
ValueError: too many values to unpack (expected 3)
```

Now, in Python 3 (Since 3.0) you can use this extended version:

```python
a, b, *c = range(4)
assert a == 0
assert b == 1
assert c == [2, 3]
```

The catch-all element (known as the \"starred\" expression) can be in
any place:

```python
a, *b, c = range(5)
assert a == 0
assert b == [1, 2, 3]
assert c == 4
```

To get the last element of a list:

```python
*a, b = range(10)
assert b == 9
assert a == [0, 1, 2, 3, 4, 5, 6, 7, 8]
```

## Chained exceptions

Situation: you catch an exception with except, do something, and then
raise a different exception:

```python
def mycopy(source, dest):
    try:
        shutil.copy2(source, dest)
    except OSError: # We don't have permissions. More on this later
        raise NotImplementedError("No permissions")
```

Problem: You lose the original traceback:

```python
>>> mycopy('noway', 'noway2')
>>> mycopy(1, 2)
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
File "<stdin>", line 5, in mycopy
NotImplementedError: No permissions
```

It was an `OSError` exception, but this information was lost. We are
assuming is a permissions problem, but it can be a lot of different
things: File not found, is a directory, is not a directory, broken
pipe, etc.

You can add this information in the new exception manually, using
`raise ... from`:

```python
>>> raise NotImplementedError from OSError
OSError
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
    NotImplementedError
```

So we can implement this way:

```python
def mycopy(source, dest):
    try:
        shutil.copy2(source, dest)
    except OSError as err: # We don't have permissions. More on this later
        raise NotImplementedError("No permissions") from err
```

## Everything is an iterator

In Python 3, `range`, `zip`, `map`, `dict.values`, etc. are all
iterators. If you want a list, just wrap the result with list. Explicit
is better than implicit. This makes harder to write code that
accidentally uses too much memory, because the input was bigger than you
expected.

## How to Use yield from

Pretty great if you use generators. Instead of writing:

```python
for i in gen():
    yield i
```

Just write:

```python
yield from gen()
```

Makes it easier to turn everything into a generator. Instead of
accumulating a list, just yield or yield from.

Instead of:

```python
def duplicate(n):
    A = []
    for i in range(n):
        A.extend([i, i])
    return A
```

You can do this to convert this to a generator:

```python
def dup(n):
    for i in range(n):
        yield i
        yield i
```

And even better:

```python
def dup(n):
    for i in range(n):
        yield from (i, i)
```

## Data Classes

One of the most tedious parts about working with Python prior to 3.7 in
an object-oriented way was creating classes to represent data in your
application.

Prior to Python 3.7, you would have to declare a variable in your class,
and then set it in your `__init__` method from a named parameter. With
applications that had complex data models, this invariably led to a
large number of boilerplate model and data contract code that had to be
maintained.

Since 3.7 you have access to a decorator called `@dataclass`, that
automatically adds an implicit `__init__` function for you when you add
typings to your class variables. When the decorator is added, Python
will automatically inspect the attributes and typings of the associated
class and generate an `__init__` function with parameters in the order
specified:

```python
from typing import List
from dataclasses import dataclass, field

@dataclass
class Vector:
    name: str
    id: str
    bars: List[str] = field(default_factory=list)


# usage

a_foo = Foo("My foo’s name", "Foo-ID-1", ["1","2"])
```

Data classes add automatically the next dunder methods (unless explicity
defind):

- a `__init__()` method

- a `__repr__()` method. The generated repr string will have the class
  name and the name and repr of each field, in the order they are
  defined in the class.

- an `__eq__()` method. This method compares the class as if it were a
  tuple of its fields, in order. Both instances in the comparison must
  be of the identical type.

- `__lt__()`, `__le__()`, `__gt__()`, and `__ge__()` methods. These
  compare the class as if it were a tuple of its fields, in order.
  Both instances in the comparison must be of the identical type. If
  order is true and eq is false, a `ValueError` is raised.

You can still add class methods to your data class, and use it like you
would any other class.


## Make format string to use repr instead of str

Since Python 3.6, we can use f-Strings: A new and improved way to format
Strings. Also called **formatted string literals**, f-strings are string
literals that have an `f` at the beginning and curly braces containing
expressions that will be replaced with their values:

```python
>>> a = 3
>>> print(f"Value of a plus 1 is {a + 1}")
Value of a plus 1 is 4
```

You can make the f-string to represent using the `repr` function adding
a `!r` postfix in the expresion inside the `{` and `}`. For example:

```python
>>> msg = "Hello, world"
>>> print(f"Message is {msg!r}")
Message is 'Hello, world'
```

Also, in python 3.8 you can add a `=` symbol to the end of an f-string
expression, that prints the text of the f-string expression itself,
followed by the value:

```python
>>> x = 3
>>> print (f'{x+1=}')
x+1=4
```

## Logging using f-strings

You must **not** use f-strings with the logging library, though. So,
instead of this code:

```python
logging.info(f"User {user_id!r} logged in")
```

Is better (for the moment):

```python
logging.info("User %r logged in", user_id)
```

!!! warning 'Please, notice this is **NOT** using the `%` operator'
    
    but using a comma to pass additional parameters. If we were using 
    the `%` operand then have the same issues as with f-strings. So
    do not use:

    # Incorrect

    ```python
    logging.info(\"User %r logged in\" % user\_id\")
    ````

    Reasons for this:

    - Depending on the logging level, the conversion to str of the objects
      can be avoid. Documentation says "Formatting of message
      arguments is *deferred* until it cannot be avoided". For
      example, if the log level is `WARNING` and we call `info`, the
      log systems will ignore the formatting operation, because is
      useless; the message is going to be ignored.

    - Using `%r` in the logging messages will use `__repr__`, which is
      sometimes preferable to just `__str__`

    - If we implement our own handlers, we could access the values of the
      objects passed to the debug call. If we are just passing
      pre-formatted strings, we miss this option.


Also consider using `%r` (`repr`) instead of `%s` (`str`), in most cases
you get more information. For example, if we log an exception:

```python
import logging
log = logging.getLogger()

err = ZeroDivisionError("Can't divide by zero, you barmpot")
log.error("Error: %s", err)
log.error("Error: %r", err)
```

produce:

```python
Error: Can't divide by zero, you barmpot
Error: ZeroDivisionError("Can't divide by zero, you barmpot")
```

In this case we get the name of the exception, along with the message.


## Context Variables

When using `async`/`await` functions in the Python event loop prior to 3.7,
context managers that used thread local variables had the chance to bleed
values across executions, potentially creating bugs that are difficult to find.

Python 3.7 introduces the concept of **context variables**, which are variables
that have different values depending on their context.  They are similar to
thread locals in that there are potentially different values, but instead of
differing across execution threads, they differ across execution contexts and
are thus compatible with async and await functions.

Here is a quick example of how to set and use a context variable in Python 3.7.
Notice that when you run this, the second async call produces the default value
as it is evaluating in a different context:

```python
import contextvars
import asyncio

val = contextvars.ContextVar("val", default="0")

async def setval():
    val.set("1")

async def printval():
    print(val.get())

asyncio.run(setval()) # sets the value in this context to 1
asyncio.run(printval()) # prints the default value “0” as its a different context
```

Every run shows different values, because the context are different.


## Dictionary Unions (Python 3.9)

Ahora se puede usar el operador `|` para mezclar los valores de dos diccionarios
`a` and `b`:

```python
a = {1: 'a', 2: 'b', 3: 'c'}
b = {4: 'd', 5: 'e'}
c = a | b
print(c)

{1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}
```

Y también tenemos el operador `|=`, que actualizará los valores del diccionario
original:

```python
a = {1: 'a', 2: 'b', 3: 'c'}
b = {4: 'd', 5: 'e'}
a |= b
print(a)

{1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}
```

Como se puede ver, para cualquier entrada que esté a la vez en los dos
diccionarios, tendrá preferencia el valor del segundo.


## Dictionary Update with Iterables

Another cool behavior of the `|=` operator is the ability to update the
dictionary with new key-value pairs using an iterable object, like a
list or generator:

```python
a = {'a': 'one', 'b': 'two'}
b = ((i, i**2) for i in range(3))
a |= b
print(a)

{'a': 'one', 'b': 'two', 0: 0, 1: 1, 2: 4}
```

If we attempt the same with the standard union operator `|` we will get
a `TypeError` as it will only allow unions between dict types.

Fuentes:

- [New Features in Python 3.9 | Towards Data Science](https://towardsdatascience.com/new-features-in-python39-2529765429fe)


## String Methods

Not as glamourous as the other new features, but still worth a mention
as it is particularly useful. Two new string methods for removing
prefixes and suffixes have been added:

```
"Hello world".removeprefix("He")

"llo world"

"Hello world".removesuffix("ld")
"Hello wor"
```

## How to "Fire and forget" with Async

According to python docs for `asyncio.Task` it is possible to start some
coroutine to execute "in background". The task created by `asyncio.create_task`
function won't block the execution (therefore the function will return
immediately!). This acts like a way to "fire and forget".

An example:

```python
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
```

Output must be something like:

```
MAIN: Do some actions 1
FOO: async_foo started
MAIN: Do some actions 2
FOO: async_foo done
MAIN: Do some actions 3
```

Note: **What if tasks are executing after event loop complete?** Asyncio
expects task would be completed at the moment event loop completed. So
if you'll change `main()` to:

```python
async def main():
    asyncio.create_task(async_foo())  # fire and forget
    print('MAIN: Do some actions 1')
    await asyncio.sleep(0.001)
    print('MAIN: Do some actions 2')
```

You can see the task is killed (It never prints the \"done\" message)
before it finished:

```
MAIN: Do some actions 1
FOO: async_foo started
MAIN: Do some actions 2
```

To prevent that you can just await all pending tasks after event loop
completed:

```python
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    # Let's also finish all running tasks:
    pending = asyncio.Task.all_tasks()
    loop.run_until_complete(asyncio.gather(*pending))
```

Output now is:

```python
MAIN: Do some actions 1
FOO: async_foo started
MAIN: Do some actions 2
FOO: async_foo done
```

What if I want to Kill tasks instead of awaiting them? For example, some
tasks may be created to run forever. In that case, you can just
`cancel()` them instead of awaiting them:

```python
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
```


## Assignment expressions or the infamous Walrus operator

There is new operator `:=` that assigns values to variables as part of a
larger expression. It is affectionately known as **the walrus operator**
due to its resemblance to the eyes and tusks of a walrus.

Before Python 3.8, we have this code:

```python
if len(a) > 10:
    print(f"Too many elements ({len(a)}), expected <= 10)")
```

That calls `len(a)` twice. We can make just one:

```python
m = len(a)
if n > 10:
    print(f"Too many elements ({n}), expected <= 10)")
```

In python 3.8 we can use the Walrus operator to make the assigment and
the calculation in one single line:

```python
if (n := len(a)) > 10:
    print(f"Too many elements ({n}), expected <= 10)")
```

A typical case is using a regular expression twice, once to test whether
a match occurred and another to extract a subgroup:

```python
discount = 0.0
if (match := re.search(r'(\d+)% discount', ad)):
    discount = float(match.group(1)) / 100.0
```

The operator is also useful with while-loops that compute a value to
test loop termination and then need that same value again in the body of
the loop:

```python
# Loop over fixed length blocks
while (block := f.read(256)) != '':
    process(block)
```

Another motivating use case arises in list comprehensions where a value
computed in a filtering condition is also needed in the expression body:

```python
result = [
    clean_name.title()
    for name in names
    if (clean_name := normalize('NFC', name)) in allowed_names
]
```

Try to **limit use of the walrus operator to clean cases that reduce
complexity and improve readability**.

## New module for getting metadata on packages

The new `importlib.metadata` module provides (provisional) support for
reading metadata from third-party packages. For example, it can extract
an installed package's version number, list of entry points, and more:

\# Note following example requires that the popular \"requests\" \#
package has been installed.

```python
from importlib.metadata import version, requires
assert version('requests') == '2.24.0'
assert len(requires('requests')) == 6
```

## Changes in asyncio module

The `asyncio.run()` function has graduated from the provisional to
stable API. This function can be used to execute a coroutine and return
the result while automatically managing the event loop. For example:

```python
import asyncio

async def main():
    await asyncio.sleep(0)
    return 42

asyncio.run(main())
```

This is roughly equivalent to:

```python
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
```

The actual implementation is significantly more complex. Thus,
`asyncio.run()` should be the preferred way of running asyncio programs.

Running `python -m asyncio` launches a natively async REPL. This allows
rapid experimentation with code that has a top-level await. There is no
longer a need to directly call `asyncio.run()` which would
spawn a new event loop on every invocation:

```shell
▶ python -m asyncio
asyncio REPL 3.10.4 (main, Jun 29 2022, 12:14:53) [GCC 11.2.0] on linux
Use "await" directly instead of "asyncio.run()".
Type "help", "copyright", "credits" or "license" for more information.
```

## New decorator for cached properties

Added a new `functools.cached_property()` decorator, for computed
properties cached for the life of the instance:

```python
import functools
import statistics

class Dataset:
def __init__(self, sequence_of_numbers):
    self.data = sequence_of_numbers

@functools.cached_property
def variance(self):
    return statistics.variance(self.data)
```

## New decorator to convert methods into generic functions

New decorator `functools.singledispatchmethod` to convert methods into [generic
functions](https://docs.python.org/3/glossary.html#term-generic-function) using
[single dispatch](https://docs.python.org/3/glossary.html#term-single-dispatch):

```python
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
```

## The Inspect module

The `inspect.getdoc()` function can now find docstrings for `__slots__` if that
attribute is a `dict` where the values are docstrings. This provides
documentation options similar to what we already have for `property()`,
`classmethod()`, and `staticmethod()`:

```python
class AudioClip:

    __slots__ = {
        'bit_rate': 'expressed in kilohertz to one decimal place',
        'duration': 'in seconds, rounded up to an integer',
    }

    def __init__(self, bit_rate, duration):
        self.bit_rate = round(bit_rate / 1000.0, 1)
        self.duration = ceil(duration)
```

## Force the logging to reload the basic configuration

Added a `force` keyword argument to `logging.basicConfig()`. When set to
`True`, any existing handlers attached to the root logger are removed
and closed before carrying out the configuration specified by the other
arguments.

This solves a long-standing problem. Once a logger or `basicConfig()`
had been called, subsequent calls to `basicConfig()` were silently
ignored. This made it difficult to update, experiment with, or teach the
various logging configuration options using the interactive prompt or a
Jupyter notebook.

## Function annotations

We can now annotate (document) parameters and results for functions and
methods:

```python
def f(a: stuff, b: stuff = 2) -> result:
    ...
```

Annotations can be arbitrary Python objects. Python doesn't do anything
with the annotations other than put them in an `__annotations__`
dictionary:

```python
>>> def f(x: int) -> float:
... pass
...
>>> f.__annotations__
{'return': <class 'float'>, 'x': <class 'int'>}
```

But it leaves open the possibility for library authors to do fun things.
Example, IPython 2.0 widgets. Run IPython notebook (in Python 3) from
IPython git checkout and open
<http://127.0.0.1:8888/notebooks/examples/Interactive%20Widgets/Image%20Processing.ip>

## Optional Underscores in Numeric Literals

Since Python 3.6 the languague has the ability to use underscores in
numeric literals for improved readability. For example:

```python
>>> 1_000_000_000_000_000
1000000000000000
>>> 0x_FF_FF_FF_FF
4294967295
```

Single underscores are allowed between digits and after any base
specifier. Leading, trailing, or multiple underscores in a row are not
allowed.

The string formatting language also now has support for the \'\_\'
option to signal the use of an underscore for a thousands separator for
floating point presentation types and for integer presentation type
\'d\'. For integer presentation types \'b\', \'o\', \'x\', and \'X\',
underscores will be inserted every 4 digits:

    >>> '{:_}'.format(1000000)
    '1_000_000'
    >>> '{:_x}'.format(0xFFFFFFFF)
    'ffff_ffff' 


## The Path Module

The `pathlib` module makes easier to work with directories and files.
pathlib has been described as an object-oriented way of dealing with
paths. Rather than working with strings, you work with \"Path\" objects,
which not only allows you to use all of your favorite path- and
file-related functionality as methods, but it also allows you to paper
over the differences between operating systems.

Instead of doing:


```python
file_name = 'debug.log'
full_path = '/tmp/workdir/{file_name}'
```

We can do:

```python
from pathlib import Path

base_dir = Path('/tmp/workdir')
full_path = base_dir / 'debug.log'
```

In the first example, the code can fail if executed in a windows
environment. This is usually fixed using `os.path.join` and
`os.path.sep`. The second example looks like its making the same error,
but it\'s not the case: We create a `Path` object using a standar
syntax, and the library choose the right Path class to use based on the
underlying O/S.

Path objects allows you to represent files or directories. If you\'re
not sure what kind of object you have, you always can ask it, with the
`is_dir` and `is_file` methods:

```python
>>> p1 = pathlib.Path('config.py')
>>> p1.is_file(), p1.is_dir()
(True, False)
>>> p2 = pathlib.Path('.')
>>> p2.is_file(), p2.is_dir()
(False, True)
```

You can also check that the file or dir really exists with the `exists`
method:

```python`
>>> p2 = pathlib.Path('Supercalifragilisticexpialidocious')
>>> p2.exists()
False
```

You can use the `/` operator, normally used for division, to join paths
together. For example:

```python
>>> dirname = pathlib.Path('/foo/bar')
>>> dirname / filename
PosixPath('/foo/bar/abc.txt')
```

It takes a bit of time to get used to seeing `/` between what you might
think of as strings. But remember that `dirname` isn\'t a string;
rather, it's a `Path` object. And `/` is a Python operator, which means
that it can be overloaded and redefined for different types.

### Working with Directories

If your `Path` object contains a directory, there are a bunch of
directory-related methods that you can run on it.

For example, to find all of the files in the current directory:

```pythn
>>> p = pathlib.Path('.')
>>> p.iterdir()
<generator object Path.iterdir at 0x111e4b1b0>
```

`Path` objects have also the `glob` method. Like `iterdir`, the `glob`
method returns a generator, meaning that you can use it in a for loop.
For example, to find all the python files in the current dir and
subdirs, we can do:

```python
>>> for one_item in p.glob('**/*.py'):
...     print(f"{one_item}: {type(one_item)}")
```


## Simpler customization of class creation (PEP 487)

It is now possible to customize subclass creation without using a
metaclass. The new `__init_subclass__` classmethod will be called on the
base class whenever a new subclass is created:

```python
class PluginBase:
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

class Plugin1(PluginBase):
    pass

class Plugin2(PluginBase):
    pass
```

Fuente: [PEP 487](https://www.python.org/dev/peps/pep-0487) for more
information.
