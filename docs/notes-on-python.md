---
title: Notes on Python
---

## Definir la versión por defecto a usar en Linux (Con apt)

En los sistemas Linux basados en Debian, como Ubuntu, Mint, etc. se puede usar
el programa `update-alternatives` para crear, borrar, editar y mostrar
información sobre determinados enlaces simbólicos que definen valores
alternativos de la distribución, como por ejemplo las versiones de Python o de
Java a utilizar por defecto.

La siguiente orden configura la versión 3.10 de Python (Debe estar instalada
previamente) como primera alternativa a usar si ejecutamos el comando `python`.

```shell
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1
```

Las opciones después de `--install` son:

- En enlace que queremos obtener al final

- En nombre de la alternativa que estamos ajustando

- El binario al que queremos enlazar

- El número de prioridad

Se pueden ver los valores asignados a `python` con el  siguiente comando:

```shell
sudo update-alternatives --config python
```

Fuentes:

- [Switch Java Version with update-alternatives](https://djangocas.dev/blog/linux/switch-java-version-with-update-alternatives/)
- [linux - How to update-alternatives to Python 3 without breaking apt? - Stack Overflow](https://stackoverflow.com/questions/43062608/how-to-update-alternatives-to-python-3-without-breaking-apt)

## Cómo obtener el directorio del usuario actual


Ser puede usar `os.path.expanduser`, que funciona en todas las
plataformas (`os.environ['HOME']` solo funciona en Unix/Linux):

```
from os.path import expanduser
home = expanduser("~")
```

A partir de Python 3.5 también se puede usar
`pathlib.Path.home()`:

```
from pathlib import Path
home = str(Path.home())
```

- Fuente: [Stackoverflow: What is a Cross plateorm way to get the home directory](https://stackoverflow.com/questions/4028904/what-is-a-cross-platform-way-to-get-the-home-directory)

## Python type checking

Python will always remain a dynamically typed language. However, [PEP
484](https://www.python.org/dev/peps/pep-0484/) introduced **type hints**,
which make it possible to also do static type checking of Python code.

Unlike how types work in most other statically typed languages, type hints by
themselves don’t cause Python to enforce types. As the name says, type hints
just suggest types. There are third party tools, which you’ll see later, that
perform static type checking using type hints.

To add information about types to the function, you simply annotate its
arguments and return value as follows:

Por ejemplo:

```python3
def headline(text: str, align: bool = True) -> str:
    ...
```

The `text: str` syntax says that the text argument should be of type str.
Similarly, the optional align argument should have type `bool` with the default
value `True`. Finally, the `->` str notation specifies that `headline()` will
return a string.

In terms of style, PEP 8 recommends the following:

- Use normal rules for colons, that is, no space before and one space after a
  colon: `text: str`

- Use spaces around the `=` sign when combining an argument annotation with a
  default value: `align: bool = True`

- Use spaces around the `->` arrow: `def headline(...) -> str`

Adding type hints like this has **no runtime effect**. To catch this kind of
error you can use a static type checker. That is, a tool that checks the types
of your code without actually running it in the traditional sense.

The most common tool for doing type checking is [Mypy](http://mypy-lang.org/).

With composite types, you are allowed to do:

```python
names: list
version: tuple
options: dict
```

Instead, you should use the special types defined in the `typing` module. These
types add syntax for specifying the types of elements of composite types. You
can write the following:

```python
>>> from typing import Dict, List, Tuple

>>> names: List[str]  # ["Guido", "Jukka", "Ivan"]
>>> version: Tuple[int, int, int]  # (3, 7, 1)
>>> options: Dict[str, bool]  # {"centered": False, "capitalize": True}
```

Each of these types **start with a capital letter** and that they all use square
brackets to define item types.

In many cases your functions will expect **some kind of sequence**, and not really
care whether it is a list or a tuple. In these cases you should use
`typing.Sequence`.

Note annotations are regular Python expressions. That means that you can
**define your own type aliases** by assigning them to new variables. You can for
instance create `Card` and `Deck` type aliases:

```python
from typing import List, Tuple

Card = Tuple[str, str]
Deck = List[Card]
```

these aliases can be inspected to see what they represent:

```python
>>> from typing import List, Tuple
>>> Card = Tuple[str, str]
>>> Deck = List[Card]

>>> Deck
typing.List[typing.Tuple[str, str]]
```

You may know that functions without an explicit return still return None: While
such functions technically return something, that return value is not useful.
You can add type hints saying as much by using `None` also as the return type:

 
```python
def play(player_name: str) -> None:
    print(f"{player_name} plays")

ret_val = play("Filip")
```

The annotations help catch the kinds of subtle bugs where you are trying to use
a meaningless return value. Mypy will give you a helpful warning:

```shell
$ mypy play.py
play.py:6: error: "play" does not return a value
```

### How to disable assertions in Python?

There are multiple approaches that affect a single process, the environment, or
a single line of code.

- **For the whole process**

Using the `-O` flag (capital O) disables all assert statements in a process.
You can also use `-OO`, this discard docstrings in addition to the -O
optimizations.

- **For the environment**

You can use the `PYTHONOPTIMIZE` environment variable to set this flag as well.
This will affect every process that uses or inherits the environment.

- **Single point in code**

If you want the code that fails to be exercised, you can catch either ensure
control flow does not reach the assertion, for example:

```
if False:
    assert False, "we know this fails, but we don't get here"
```

or you can catch the assertion error:

```
try:
    assert False, "this code runs, fails, and the exception is caught"
except AssertionError as e:
    print(repr(e))
```

which prints:

```
AssertionError('this code runs, fails, and the exception is caught')
```

Fuentes:

- [Stack OVerflow: Debugging - Disable assertions in Python](https://stackoverflow.com/questions/1273211/disable-assertions-in-python)


## Third party libraries

- [Pampy: The Pattern Matching for Python you always dreamed of](https://github.com/santinic/pampy) 

- [Record terminal sessions as SVG animations](https://github.com/nbedos/termtosvg)

- [Molten: A minimal, extensible, fast and productive framework for building HTTP APIs with Python 3.6 and later.](https://github.com/Bogdanp/molten)

- [A tour in the wonderland of math with python. ](https://github.com/neozhaoliang/pywonderland)

- [A command-line and interactive shell framework](https://github.com/facebookincubator/python-nubia)

- [A powerful set of Python debugging tools, based on PySnooper ](https://github.com/alexmojaki/snoop)

- [Animation engine for explanatory math videos](https://github.com/3b1b/manim)

- [Voluptuous, despite the name, is a Python data validation library.](https://github.com/alecthomas/voluptuous)

- [Python 3.7 to JavaScript compiler - Lean, fast, open!](https://github.com/qquick/Transcrypt)

- [Build GUI for your Python program with JavaScript, HTML, and CSS](https://github.com/r0x0r/pywebview)

- [A 3d rendering library written completely in python](https://github.com/ryu577/pyray)

- [Download SoundCloud music at 128kbps with album art and tags](https://github.com/sdushantha/soundcloud-dl)

- [Content aware image resizing ](https://github.com/avidLearnerInProgress/pyCAIR)

- [A Python utility belt containing simple tools, a stdlib like feel, and extra batteries. Hashing, Caching, Timing, Progress, and more made easy!](https://github.com/Erotemic/ubelt)

- [Terminal session recorder](https://github.com/asciinema/asciinema)

- [Fast, asynchronous and elegant Python web framework](https://github.com/vibora-io/vibora)

## CPython internals: A ten-hour codewalk through the Python interpreter source code

- http://www.pgbovine.net/cpython-internals.htm

## Allison Kaptur - Bytes in the Machine: Inside the CPython interpreter - PyCon 2015

- https://www.youtube.com/watch?v=HVUTjQzESeo

## How to make the Singleton Pattern in Python, the right way

### Use a metaclass:

```Python
class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
```

In Python2:

```
class MyClass(BaseClass):
    __metaclass__ = Singleton
    ...
```


In Python3:

```
class MyClass(BaseClass, metaclass=Singleton):
    ...
```

Usar en ambas versiones, con `six`:

```
import six

@six.add_metaclass(Singleton) 
class MyClass(BaseClass):
    ...
```

Pros of this method:

- It's a true class

- Auto-magically covers inheritance

- Uses __metaclass__ for its proper purpose (and made me aware of it)

Source from <https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python>

[TODO] Faltan más opciones

## How to make a chunk or batch, i.e. split a list or sequence into evenly sized chunks

An elegant way to do it is described by user
[sanderle](https://stackoverflow.com/users/577088/senderle) in [Stack
Overflow](https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks/22045226#22045226):

```
    from itertools import islice

    def batch(it, size):
        it = iter(it)
        return iter(lambda: tuple(islice(it, size)), tuple())
```

The trick uses a relative unknown property of iter; it can be called with one or two parameters. In this second case, the second parameter is a _sentinel_ value. From the documentation
of `iter`:

> `iter(o, [sentinel])`: Return an iterator object. The first argument is interpreted very
> differently depending on the presence of the second argument. Without a second argument, `o` must be
> a collection object which supports the iteration protocol (the `__iter__()` method), or it must
> support the sequence protocol (the `__getitem__()` method with integer arguments starting at 0). If
> it does not support either of those protocols, `TypeError` is raised. If the second argument,
> `sentinel`, is given, then `o` must be a callable object. The iterator created in this case will call
> `o` with no arguments for each call to its `next()` method; if the value returned is equal to
> `sentinel`, `StopIteration` will be raised, otherwise the value will be returned.

## Libs and news

### pygame 1.9.5 released

https://www.pygame.org/news/2019/3/1-9-5-released-into-the-wilds

> Every single source file has been heavily modified and moved in this release. Initial (source code
> only) support for SDL2 has been merged in. We also support compiling with SDL1 in the same code
> base, so the migration to pygame 2 is easier. pygame 2 will be released with SDL2 being the
> default backend when some remaining issues are ironed out. The 1.9.x releases will continue with
> SDL1 until then. Also, the C API of pygame is undergoing a transformation with lots of cleanups.
> Then there have been plenty of other cleanups all throughout the python code as well. There's
> still lots to clean up, but things should be significantly easier for people to contribute (👋
> hello and thanks new contributors!). The documentation has been improved with better examples
> links, search functionality, and improved navigation. Support for older Macs, and newer Macs has
> been improved. The mask, midi, draw, and math modules have gotten lots of polish with rough edges
> removed.


## OpenCV-Python Cheat Sheet

From Importing Images to Face Detection, Cropping, Resizing, Rotating,
Thresholding, Blurring, Drawing & Writing on an image, Face Detection &
Contouring to detect objects. All Explained.

https://heartbeat.fritz.ai/opencv-python-cheat-sheet-from-importing-images-to-face-detection-52919da36433

> OpenCV is an open source computer vision and machine learning library. It has 2500+ optimized
> algorithms—a comprehensive set of both classic and state-of-the-art computer vision and machine
> learning algorithms. It has many interfaces, including Python, Java, C++, and Matlab.

Here, we’re gonna tackle the Python interface.

Table of Contents

 - Installation
 - Importing/Viewing an Image
 - Cropping
 - Resizing
 - Rotating
 - Grayscaling and Thresholding
 - Blurring/Smoothing
 - Drawing a Rectangle/Bounding Box
 - Drawing a Line
 - Writing on an Image
 - Face Detection
 - Contours—A Method for Object Detection
 - Saving an Image


## Working with PDFs in Python: Reading and Splitting

https://stackabuse.com/working-with-pdfs-in-python-reading-and-splitting/

> This article is the beginning of a little series, and will cover these helpful Python libraries.
> In Part One we will focus on the manipulation of existing PDFs. You will learn how to read and
> extract the content (both text and images), rotate single pages, and split documents into its
> individual pages. Part Two will cover adding a watermark based on overlays. Part Three will
> exclusively focus on writing/creating PDFs, and will also include both deleting and re-combining
> single pages into a new document.


## Creating a GUI Application for NASA’s API with wxPython

https://www.blog.pythonlibrary.org/2019/04/18/creating-a-gui-application-for-nasas-api-with-wxpython/

> Growing up, I have always found the universe and space in general to be exciting. It is fun to
> dream about what worlds remain unexplored. I also enjoy seeing photos from other worlds or
> thinking about the vastness of space. What does this have to do with Python though? Well, the
> National Aeronautics and Space Administration (NASA) has a web API that allows you to search their
> image library. 


## PySnooper - Never use print for debugging again

https://github.com/cool-RR/PySnooper

> PySnooper is a poor man's debugger. You're trying to figure out why your Python code isn't doing
> what you think it should be doing. You'd love to use a full-fledged debugger with breakpoints and
> watches, but you can't be bothered to set one up right now.

You want to know which lines are running and which aren't, and what the values of the local
variables are.

Most people would use print lines, in strategic locations, some of them showing the values of
variables.

PySnooper lets you do the same, except instead of carefully crafting the right print lines, you just
add one decorator line to the function you're interested in. You'll get a play-by-play log of your
function, including which lines ran and when, and exactly when local variables were changed.


## Distributed notifications using websockets

> Dino is a distributed notification service intended to push events to groups of clients. Example
> use cases are chat server, real-time notifications for websites, push notifications for mobile
> apps, multi-player browser games, and more. Dino is un-opinionated and any kind of events can be
> sent, meaning Dino only acts as the router of events between clients.

Any number of nodes can be started on different machines or same machine on different port. Flask
will handle connection routing using either Redis or RabbitMQ as a message queue internally. An
nginx reverse proxy needs to sit in-front of all these nodes with sticky sessions (ip_hash).
Fail-over can be configured in nginx for high availability.

Fuentes:

- [GitHub - thenetcircle/dino: Distributed notifications using websockets](https://github.com/thenetcircle/dino/)


## Teaching a kid to code with Pygame Zero

> How can you excite a kid about coding and computers? As a software developer and father of two
> children, I think about this question often. A person with software skills can have big advantages
> in our modern world, so I’d like to equip my kids for their future.

In my home, we play video games together. My children (aged six and four) watch me play through many
classics like Super Mario World and The Legend of Zelda: A Link to the Past. They like spending that
time with daddy and are really engaged with the video game. When I considered how my six year old
son might enjoy coding, using video games as the channel into computing was a very natural idea.

Fuentes:

- [Teaching a kid to code with Pygame Zero - Matt Layman](https://www.mattlayman.com/blog/2019/teach-kid-code-pygame-zero/)


## Getting to Know Python 3.7: Data Classes, async/await and More!

https://blog.heroku.com/python37-dataclasses-async-await

> If you're like me, or like many other Python developers, you've probably lived (and maybe
> migrated) through a few version releases. Python 3.7(.3), one of the latest releases, includes
> some impressive new language features that help to keep Python one of the easiest, and most
> powerful languages out there. If you're already using a Python 3.x version, you should consider
> upgrading to Python 3.7. Read on to learn more about some of the exciting features and
> improvements.

## Reproducing Images using a Genetic Algorithm with Python

https://heartbeat.fritz.ai/reproducing-images-using-a-genetic-algorithm-with-python-91fc701ff84

> This tutorial uses a genetic algorithm to reproduce images, starting with randomly generated ones
> and evolving the pixel values.

Regarding the implementation of GA in Python, I also prepared a tutorial titled “Genetic Algorithm Implementation in Python” which discusses how to implement GA in details. It is available at these links:

https://www.linkedin.com/pulse/genetic-algorithm-implementation-python-ahmed-gad

## Python at Netflix

https://medium.com/netflix-techblog/python-at-netflix-bba45dae649e

> As many of us prepare to go to PyCon, we wanted to share a sampling of how Python is used at
> Netflix. We use Python through the full content lifecycle, from deciding which content to fund all
> the way to operating the CDN that serves the final video to 148 million members. We use and
> contribute to many open-source Python packages, some of which are mentioned below. If any of this
> interests you, check out the jobs site or find us at PyCon. We have donated a few Netflix
> Originals posters to the PyLadies Auction and look forward to seeing you all there.

## Monkey Patching in Python: Explained with Examples

https://thecodebits.com/monkey-patching-in-python-explained-with-examples/

> In this post, we will learn about monkey patching, i.e., how to dynamically update code behavior
> at runtime. We will also see some useful examples of monkey patching in Python.

## Python 3 at Mozilla

https://ahal.ca/blog/2019/python-3-at-mozilla/

> Mozilla uses a lot of Python. Most of our build system, CI configuration, test harnesses, command
> line tooling and countless other scripts, tools or Github projects are all handled by Python. In
> mozilla-central there are over 3500 Python files (excluding third party files), comprising roughly
> 230k lines of code. Additionally there are 462 repositories labelled with Python in the Mozilla
> org on Github (though many of these are not active). That’s a lot of Python, and most of it is
> Python 2.

With Python 2’s exaugural year well underway, it is a good time to take stock of the situation and
ask some questions. How far along has Mozilla come in the Python 3 migration? Which large work items
lie on the critical path? And do we have a plan to get to a good state in time for Python 2’s EOL on
January 1st, 2020?

## Python INTRO


Some of the most popular online interpreters and codepads. Give them a go to find your favorite.

https://www.python.org/shell/
https://www.onlinegdb.com/online_python_interpreter
https://repl.it/languages/python3
https://www.tutorialspoint.com/execute_python3_online.php
https://rextester.com/l/python3_online_compiler
https://trinket.io/python3

Additional Python resources

While this course will give you information about how Python works and how to write scripts in
Python, you’ll likely want to find out more about specific parts of the language. Here are some
great ways to help you find additional info: 

Read the official Python documentation.
Search for answers or ask a question on Stack Overflow. 
Subscribe to the Python tutor mailing list, where you can ask questions and collaborate with other Python learners.
Subscribe to the Python-announce mailing list to read about the latest updates in the language.

Python history and current status

Python was released almost 30 years ago and has a rich history. You can read more about it on the History of Python Wikipedia page or in the section on the history of the software from the official Python documentation.

Python has recently been called the fastest growing programming language. If you're interested in why this is and how it’s measured, you can find out more in these articles:

- [The Incredible Growth of Python (Stack Overflow)](https://stackoverflow.blog/2017/09/06/incredible-growth-python/)
- [Why is Python Growing So Quickly - Future Trends (Netguru)](https://www.netguru.com/blog/why-python-is-growing-so-quickly-future-trends)
- [By the numbers: Python community trends in 2017/2018 (Opensource.com)](https://opensource.com/article/18/5/numbers-python-community-trends)
- [Developer Survey Results 2018 (Stack Overflow)](https://insights.stackoverflow.com/survey/2018#technology)


## Palabras reservadas en Python (keywords)

Keywords are reserved words that are used to construct instructions. We briefly encountered for and in in our first Python example, and we'll use a bunch of other keywords as we go through the course. For reference, these are all the reserved keywords:

False	class	finally	is	return
None	continue	for	lambda	try
True	def	from	nonlocal	while
and	del	global	not	with
as	elif	if	or	yield
assert	else	import	pass	
break	except	in	raise
