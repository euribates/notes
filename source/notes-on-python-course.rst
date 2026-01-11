Curso de Python (Notas)
========================================================================


Patrones
------------------------------------------------------------------------

- Adapter - Match interfaces of different classes
- Bridge - Separates an object’s interface from its implementation
- Composite - A tree structure of simple and composite objects
- Decorator - Add responsibilities to objects dynamically
- Facade - A single class that represents an entire subsystem
- Flyweight - A fine-grained instance used for efficient sharing
- Proxy - An object representing another object
- Chain of Responsibility
- Command
- Iterator
- Mediator
- Memento
- Observer
- State
- Strategy
- Template Method
- Visitor

Chain of responsibility
------------------------------------------------------------------------

A way of passing a request between a chain of objects

Command
------------------------------------------------------------------------

Encapsulate a command request as an object

Interpreter
------------------------------------------------------------------------

A way to include language elements in a program

Iterator
------------------------------------------------------------------------

Sequentially access the elements of a collection

Mediator
------------------------------------------------------------------------

Defines simplified communication between classes

Memento
------------------------------------------------------------------------

Capture and restore an object’s internal state

Null Object
------------------------------------------------------------------------

Designed to act as a default value of an object

Observer
------------------------------------------------------------------------

A way of notifying change to a number of classes

State
------------------------------------------------------------------------

Alter an object’s behavior when its state changes

Strategy
------------------------------------------------------------------------

Encapsulates an algorithm inside a class

Template method
------------------------------------------------------------------------

Defer the exact steps of an algorithm to a subclass

Visitor
------------------------------------------------------------------------

Defines a new operation to a class without change

Librerías
------------------------------------------------------------------------

- socket
- Matemáticas: numbers, math, cmath, decimal, fractions, random,
satistics
- argparse, logging, timeit, trace, cmd, trace, configparser
- heapq, bisect, array
- File formats: json, xml, BeautifulSoup
- Sistema operativo: sys, os, shutil, glob
- Collections: OrderedDict, defaultdict, namedtuple,
- Ejecución concurrente: threading, subprocess, queue, sched
- Interfaces gráficas de usuario: tkinter, wxPython, PyQt, PyGTK, Kivy,
pGUI
- Numpy, Pandas, SciPy, matplotlib
- Pillow
- pygame
- pyglet
- pycrypto
- Django, Flask, Twisted, Pyramid, TurboGears

Youtube channels: ‘sentdex’,’thenewboston’,’Python training by Dan
Bader’,’Corey Schafer’,’Clever Programmer’,’Trevor Payne’.

Guerras de Internet tubos delitos del futuro master algorithm grandes
desastrrs tecnologicos Algoritmo de ada

Networking and Interprocess Communication

- asyncio — Asynchronous I/O
- socket — Low-level networking interface
- ssl — TLS/SSL wrapper for socket objects
- select — Waiting for I/O completion
- selectors — High-level I/O multiplexing
- asyncore — Asynchronous socket handler
- asynchat — Asynchronous socket command/response handler
- signal — Set handlers for asynchronous events
- mmap — Memory-mapped file support

Internet: email, json, base64, http, urllib, html

- email — An email and MIME handling package
- json — JSON encoder and decoder
- mailcap — Mailcap file handling
- mailbox — Manipulate mailboxes in various formats
- mimetypes — Map filenames to MIME types
- base64 — Base16, Base32, Base64, Base85 Data Encodings
- binhex — Encode and decode binhex4 files
- binascii — Convert between binary and ASCII
- quopri — Encode and decode MIME quoted-printable data
- uu — Encode and decode uuencode files
- threading — Thread-based parallelism
- multiprocessing — Process-based parallelism
- multiprocessing.shared_memory — Provides shared memory for direct access across processes
- The concurrent package
- concurrent.futures — Launching parallel tasks
- subprocess — Subprocess management
- sched — Event scheduler
- queue — A synchronized queue class
- thread — Low-level threading API
- dummy_thread — Drop-in replacement for the thread module
- dummy_threading — Drop-in replacement for the threading module

Patrones de diseño (Design Patterns)
------------------------------------------------------------------------

Introducción
~~~~~~~~~~~~

En ingeniería del software, se conoce como **Patron** a una solución a
un problema habitual, en un contexto determinado. Cada patrón tienen un
nombre propio, ya que la idea es que los patrones aporten un vocabulario
especializado, de forma que los desarrolladores puedan hablar de ellos
sin necesidad de explicar cada detalle del patrón.

Los patrones se suelen clasificar en tres categorías, en función de si
nivel de abstracción y de su independencia respecto al lenguaje de
implementación. Estas categorías son patrones estructurales o de
arquitectura (*Architectural Patterns*), patrones de diseño (*Design
Patterns*) y modismos o expresiones ideomáticas (*Idioms*). En esta
parte nos vamos a centrar en los patrones de diseño, en decir patrones a
un nivel intermedio de abstracción y no especialmente vinculados con
ningún lenguaje.

Los patrones de diseño como tales fueron descritos inicialmente en el
libro is also known as the GANG OF FOUR -book (GOF for short) [GHJV95]
and Python language idioms. The patterns are not only microarchitectural
models but also useful as a common design vocabulary among software
engineers. The overall architecture of the system and related design
decisions can be explained by giving a set of patterns used.

While new patterns do emerge the GOF still remains as the definite
reference on design patterns. For this reason it is important to
introduce these patterns, the notions and the theory behind them and
their applicability to Python community.

GOF is divided into three parts and each part describes the patterns
related to the theme of the part. The themes describe the purpose of the
patterns. Creational patterns address object instantiation issues.
Structural patterns concentrate on object composition and their
relations in the runtime object structures. Whereas the structural
patterns describe the layout of the object system, the behavioral
patterns focus on the internal dynamics and object interaction in the
system.

While the design patterns strive to be language independent they still
require - at least implicitly - some support from the implementation
language and especially from its object model. In GOF the languages of
choice are C++ and Smalltalk. Therefore the availability of access
specifiers and static member functions (class methods) are assumed. The
aim here is to look at some GOF patterns and try to implement them in a
language (Python) whose object model is radically different from that of
C+By doing this we can draw some conclusions about the generality of GOF
patterns and what accommodations - if any - are necessary when applying
them in Python programming environment. And while operating on the
programming language level we look at some Python idioms and how they
can help implement GOF patterns.

We begin with a short description of Python as an object language in
Section 2 and then move on to the selected patterns. We have chosen one
pattern from each category of GOF: Singleton (creational, Section 3),
Chain of Responsibility (behavioral, Section 4) and Proxy (structural,
Section 5). In Section 6 we sum up the lessons learned and further
discuss the generality of our implementation solutions.

Python es un lenguaje que, por su naturaleza dinámica, facilita
implementar e incluso trae ya de serie implementados varios patrones de
uso frecuente. Esto hace posible que incluso hayamos usado varios
patrones sin ser conscientes de ello. Por otro lado, hay algunos
patrones que son totalmente innecesarios, por la naturaleza del
lenguaje.

Por ejemplo, el patrón **Factory** en un patrón de diseño orientado a la
creación de objetos, ocultando la lógica de instanciación de los mismos
al usuario. Pero la creación de objetos en Python es dinámica, por
diseño del lenguaje, así que normalmente este patrón no es necesario. No
es que no se pueda usar, claro. Se puede implementar sin problema, y
puede haber casos de uso en los que sea realmente útil, pero estos casos
serán más la excepción que la regla.

Que es un Patrón de diseño (Desing Pattern)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La idea de los patrones de diseño fue planteada por

The principle of least astonishment
------------------------------------------------------------------------

When designing an interface, there are many different things to bear in
mind. One of them, which for me is the most important, is the **law or
principle of least astonishment**. It basically states that if in your
design a necessary feature has a high astonishing factor, it may be
necessary to redesign your application. To give you one example, when
you’re used to working with Windows, where the buttons to minimize,
maximize and close a window are on the top-right corner, it’s quite hard
to work on Linux, where they are at the top-left corner. You’ll find
yourself constantly going to the top-right corner only to discover once
more that the buttons are on the other side.

If a certain button has become so important in applications that it’s
now placed in a precise location by designers, please don’t innovate.
Just follow the convention. Users will only become frustrated when they
have to waste time looking for a button that is not where it’s supposed
to be.

The disregard for this rule is the reason why I cannot work with
products like Jira. It takes me minutes to do simple things that should
require seconds.

Threading considerations

Links
------------------------------------------------------------------------

- Build a Crud application using Vue and Django
https://codesource.io/build-a-crud-application-vue-and-django/

- Add Push Notifications to a Web App with Firebase
https://codesource.io/add-push-notifications-to-a-web-app-with-firebase/

- Introduction to Zero
https://pygame-zero.readthedocs.io/en/stable/introduction.html

- Monads in Python https://pypi.org/project/PyMonad/
