Vs Code
========================================================================

.. tags:: editor,python

**Vs Code** es un IDE multipropósito de Microsoft.

Cómo definir *snippets* personalizados
------------------------------------------------------------------------

Abrir el menú **File** -> **Preferences** -> **User snippets** y
seleccionar el lenguaje (o la opción ``New Global Snippets File`` si
queremos crear un *snippet* para cualquier tipo de fichero).

Los *snippets* se escriben en formato JSON. Soportan la sintaxis del
editor TextMate. Se pueden usar las variables ``$1``, ``$2``, … ``%n``
para indicar puntos de parada del tabulador, y ``$0`` para indicar la
posición final del cursor. También se pueden usar *placeholders*, con la
forma ``{1:id}``, estando conectados los que usen el mismo valor de
``id``.

Este es un ejemplo de *snippet* para un bucle ``for`` de Javascript:

.. code:: json

    // in file 'Code/User/snippets/javascript.json'
    {
        "For Loop": {
            "prefix": ["for", "for-const"],
            "body": [
                "for (const ${2:element} of ${1:array}) {",
                "    $0",
                "}"
                ],
            "description": "A for loop."
            }
    }

Donde:

- ``For Loop`` es el nombre/descripción del *snippet*

- ``prefix`` el o los disparadores

- ``body`` es la lista de cadenas de texto que forman el cuerpo del
  *snippet*. Los saltos de línea y tabulaciones respetarán el contexto
  donde se expandan.

- ``description``: Campo opcional con la descripción a mostrar por inteliSense

Otro ejemplo, para Python:

.. code:: json

    {
        "Main if call": {
            "prefix": "ifmain",
            "body": [
                "if __name__ == '__main__':",
                "    main($0)",
                ],
            "description": "Call to main if applicable",
            }
    }

Trabajar con diferentes intérpretes
------------------------------------------------------------------------

Por defecto, la extensión de Python usará el primer intérprete que
encuentre en el ``PATH``. Para seleccionar un entorno específico hay que
seleccionar ``Python: Select Interpreter command`` desde la paleta do
comandos :keys:`ctrl+shift+p`.

Fuentes:

-  `Using Python Environments in Visual Studio Code <https://code.visualstudio.com/docs/python/environmentsDropbox/notes/notes-on-vscode.md_work-with-python-interpreters>`_

Usar VIM dentro de VSCode
------------------------------------------------------------------------

Source:
https://www.barbarianmeetscoding.com/blog/2019/02/08/boost-your-coding-fu-with-vscode-and-vim

- Open Visual Studio Code

- Go to Extensions

- Type vim in the search box

- The first plugin named Vim is the one you want

- Click on the install button

Now after the extension is installed you may need to restart Visual
Studio Code for the changes to take effect. latest-vscode

Have you restarted it? Open a code file from your latest project and
look at the cursor. Does it look like a rectangle? Yes? Welcome to Vim

How to Move Horizontally Word By Word
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Word Motions allows you to move faster horizontally:

- Use ``w`` to jump from word to word (and ``b`` to do it backward)

- Use ``e`` to jump to the end of a word (and ``ge`` to do it backward)

- A word in Vim only includes letters, digits and numbers. If you want
  to consider special characters like ``.,`` (, {, etc as part of a word
  (called WORD in Vim jargon) you can use the capitalized equivalents of
  the keys above (``W``, ``B``, ``E``, ``gE``)

- In general, word motions allow for more precise changes while WORD
  motions allow for faster movement.

How to Move To A Specific Character
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Find character motions allow you to move horizontally quickly and with
high precision:

- Use ``f{char}`` to move (find) to the next occurrence of a character
  char in a line (and ``F`` to move backwards). For instance, ``f"``
  sends you to the next occurrence of a double quote.

- Use ``t{char}`` to move the cursor just before (until) the next
  occurrence of a character char

- After using ``f{char}`` you can type ``;`` to go to the next
  occurrence or ``,`` to go to the previous one. You can see the ``;``
  and ``,`` as commands for repeating the last character search.

how to move horizontally extremely
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To move extremely horizontally use:

- ``0``: Moves to the first character of a line

- ``^``: Moves to the first non-blank character of a line

- ``$``: Moves to the end of a line

- ``g_``: Moves to the non-blank character at the end of a line

How to move vertically
~~~~~~~~~~~~~~~~~~~~~~

Starting from ``k`` and ``j``, we move on to a faster way of maneuvering
vertically with:

- ``}`` jumps entire paragraphs downwards

- ``{`` similarly but upwards

- ``CTRL-D`` let’s you move down half a page

- ``CTRL-U`` let’s you move up half a page

How to Moving Semantically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Use ``gd`` to jump to definition of whatever is under your cursor

- Use ``gf`` to jump to a file in an import


Editing Like Magic With Vim Operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Motions aren’t just for moving. They can be used in combination with a
series of commands called operators to edit your code in Normal mode.
These combos normally take this shape:

.. mermaid::

    graph LR

    operator --> TOP[an_action to perform]
    operator ==> count ==> motion;
    count -->  TCOUNT[perform action count times]
    motion --> TMOTION[subject of the action]
    
Por ejemplo, suponiendo el operador de borrado, ``d``:

- ``d5j`` borra 5 líneas hacia abajo

- ``df'`` borrar todos los caracteres que encuentre desde la posición
  actual en adelante (*forward*) hasta que encuentre la primera
  aparición del carácter ``'``, que también es borrado.

- ``dt'`` Igual que el anterior, pero no borra el carácter ``'``.

- ``d/hello`` borra todo hasta laprimera aparición del texto ``hello``.

- ``ggdG`` Borra todo el documento. Con `gg` el cursor se situa al
  principio, con `d` se borra y el movimiento, ``G``, es ir hasta el
  final del documento.

Other useful operators are:

-  ``c`` change. This is the most useful operator. It deletes and sends
you into insert mode so that you can type

-  ``y`` yank or copy in Vim jargon

-  ``p`` put or paste in Vim jargon

-  ``g~`` to toggle caps

All these operators have some useful shorthand syntax aimed at saving
you typing and increasing your speed in common use cases:

- Double an operator to make it operate on a whole line: ``dd`` deletes
  a whole like, ``cc`` changes a whole line, etc.

- Capitalize an operator to make it operate from the cursor to the end
  of a line: ``D`` deletes from the cursor to the end of the line, ``C``
  changes to the end of a line, etc.


Editing Up a Notch With Text Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Text objects are structured pieces of text or, if you will, the entities
of a document domain model. What is a document composed of? Words,
sentences, quoted text, paragraphs, blocks, (HTML) tags, etc. These are
text objects.

The way that you specify a text object within a command is by combining
the letter ``a`` (which represents the text object plus whitespace) or
``i`` (inner object without whitespace) with a character that represents
a text object itself: ``w`` for word, ``s`` for sentence, ``'`` ``"``
for quotes, ``p`` for paragraph, ``b`` for block surrounded by ``(``,
``B`` for block surrounded by ``{`` and ``t`` for tag. So to delete
different bits of text you could:

- ``daw`` to delete a word (plus trailing whitespace)
- ``ciw`` to change inner word
- ``das`` to delete a sentence (dis delete inner sentence)
- ``da"`` to delete something in double quotes including the quotes
- ``ci"`` to change something inside double quotes
- ``dap`` to delete a paragraph
- ``dab`` ``da(`` or ``da)`` to delete a block surrounded by (
- ``daB`` ``da{`` or ``da}`` to delete a block surrounded by {
- ``dat`` to delete an HTML tag
- ``cit`` to change the contents of an HTML tag

Combining text objects with operators is extremely powerful and you’ll
use them very often. Stuff like ``cit``, ``ci"`` and ``cib`` is just
brilliant.

Let’s say that we want to change the contents of this string below for
something else:

.. code::

    const salute = 'I salute you oh Mighty Warrior'

tecleamos  ``ci'Hi!<ESC>`` y se convierte en:

.. code::

    const salute = 'Hi!'

Just like that. You don’t need to go grab the mouse, select the text and
then write something else. You type three letters and Boom.


### Repeating The Last Change with The Dot Operator

Vim has yet another trick in store for you aimed at saving you more
keystrokes: The magic ``.`` command. This command allows you to repeat
the last change you made. Imagine that you run ``dd`` to delete a line.
You could type ``dd`` again to delete another line but you could also
use ``.`` which is just a single keystroke. Ok, you save one keystroke,
so what? Well, you can use the ``.`` command to repeat any type of
change, not just single commands. For instance, you could change a word
for “Awesome” like so ``cawAwesome<CR>``, and then repeat that whole
command with all those keystrokes by just using ``.``. Think of the
possibilities!

The ``.`` command works great in combination with the repeat search
commands (``;``, ``,``, ``n`` or ``N``). Imagine that you want to delete
all occurrences of *cucumber*. An alternative would be to search for
cucumber ``/cucumber`` then delete it with ``daw``. From then on you can
use ``n`` to go to the next match and ``.`` to delete it! Two
keystrokes!?! Again think of the possibilities!!


Some handy Visual Studio Code only key mappings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alguna funciones que no están en Vim pero que soporta este *plugin*:

- ``gb`` añade otro cursor en la siguiente palabra que encuentre que sea
  igual que la palabra en la que está el cursor actual. Como ``\*``̀ pero
  en vez de salra, cread cursores adicionales.

- ``af`` es un modo visual que seleeciona de forma incremental secciones
  cada vez mæs amplias de texto.

- ``gh`` es equivalente a mover el cursor del ratøn por donde está el
  cursor del texto. Resulta útil pasra habilitar ciertas opciones que
  normalmente solo están disponibles desde el ratón.
