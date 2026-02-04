Vim
========================================================================

.. tags:: unix,linux,vim,development

.. contents:: Relación de contenidos
    :depth: 3

Cómo hacer que Vim copie al porta papeles del sistema, ademas del interno
-------------------------------------------------------------------------

Este es el camino (Ponerlo en el fichero ``.vimrc``):

.. code::

    set clipboard+=unnamedplus,unnamed

Referencia: ``help: clipboard``

When the ``"unnamed"`` string is included in the ``clipboard``
option, the unnamed register is the same as the ``*`` register. Thus
you can yank to and paste the selection without prepending ``"*`` to
commands.

Cómo incluir caracteres unicode en Vim (*Diagraphs*)
------------------------------------------------------------------------

======================= ================ ======
Keys                    Meaning          Symbol
======================= ================ ======
++ctrl+shift+k++ ``OK`` OK               ✓
++ctrl+shift+k++ ``XX`` BALLOT X         ✗
++ctrl+shift+k++ ``*1`` BLACK STAR       ☆
++ctrl+shift+k++ ``*2`` WHITE STAR       ★
++ctrl+shift+k++ ``AA`` AND              ∧
++ctrl+shift+k++ ``OR`` OR               ∨
++ctrl+shift+k++ ``-+`` Más o menos      ±
++ctrl+shift+k++ ``<<`` Abre Comillas    «
++ctrl+shift+k++ ``>>`` Cierra comillas  »
++ctrl+shift+k++ ``->`` Flecha a derecha →
++ctrl+shift+k++ ``*X`` Multiplicación   ×
++ctrl+shift+k++ ``?=`` Aproximadamente  ≅
++ctrl+shift+k++ ``?3`` Equivalente      ≡
======================= ================ ======

Fuentes:

- `List of Unicode useful symbols <https://en.wikibooks.org/wiki/Unicode/List_of_useful_symbols>`_

- `RFC 1345 - Character Mnemonics and Character Sets <https://datatracker.ietf.org/doc/html/rfc1345>`_

- `Deep dive into Digraph - Part 1 <https://hjkl.substack.com/p/deep-dive-into-digraph-part-1?s=r>`_

Cómo resolver las búsquedas
------------------------------------------------------------------------

Cuando buscamos, podemos resaltar los textos encontrados con:

.. code::

    :set hlsearch

Para desactivar el resaltado usar el siguiente comando (Ojo, es un
comando no una opción, no lleva ``set``):

.. code::

    :nohlsearch

Fuentes:

- `Highlight all search pattern matches \| Vim Tips Wiki <https://vim.fandom.com/wiki/Highlight_all_search_pattern_matches>`_

Diferencia entre ``remap``, ``noremap``, ``nnoremap`` y ``vnoremap``
------------------------------------------------------------------------

.. warning:: ``remap`` es una opción que hace que los
    mapeos funcionen recursivamente. Está activo por defecto y se recomienda
    dejarlo así.

El resto son comandos que funcionan así:

- ``:map`` y ``:noremap`` son las versiones **recursivas** y **no
  recursivas** de los diferentes comandos de mapeo. Por ejemplo, si
  ejecutamos:

.. code::

    :map j gg           (moves cursor to first line)
    :map Q j            (moves cursor to first line)
    :noremap W j        (moves cursor down one line)

Entonces:

- ``j`` se mapea a ``gg``.

- ``Q`` también se mapea ``gg``, porque ``j`` será expendido ya que se
  aplica recursividad.

- ``W`` se mapea a ``j`` (y no a ``gg``) porque ``j`` **no** será
  expandido, ya que se ha hecho un mapeo no recursivo.

Es importante recordar que Vim es un editor **modal**; tiene un modo
**normal**, un modo **visual**, entre otros. Hay un mapeo que funciona
en los modos normal, visual, selección y operador (``:map`` y
``:noremap``), uno que funciona solo en modo normal (``:nmap`` y
``:nnoremap``), uno que funciona solo en modo visual (``:vmap`` t
``:vnoremap``), etc.

Para más información sobre este tema:

- ``:help :map``
- ``:help :noremap``
- ``:help recursive_mapping``
- ``:help :map-modes``

Fuentes:

- Stackoverflow: `What is the difference between the remap, noremap, nnoremap and vnoremap mapping commands in Vim <https://stackoverflow.com/questions/3776117/>`_

- Vim Fandom: `Mapping keys in Vim - Tutorial (Part 1) <https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)>`_

Cómo reutilizar una selección visual
------------------------------------------------------------------------

Con ``gv`` seleccionamos de nuevo la última área visual seleccionada.

A menudo necesitamos realizar varias operaciones sobre un bloque visual
que hemos seleccionado, pero al realizar, por ejemplo, una búsqueda, o
un reemplazo, salimos del modo visual y tenemos que seleccionar de nuevo
el área que nos interesa.

Podemos volver a seleccionar el área anterior con ``gv``.

Fuentes:

- StackOverflow: `How do you reuse a visual mode selection? <https://superuser.com/questions/220666/how-do-you-reuse-a-visual-mode-selection>`_


Dónde puedo obtener resumenes/chuletas sobre Vim
------------------------------------------------------------------------

- `Vim Diff cheatshhet <https://devhints.io/vim-diff>`_

- `Vim Cheatshhet <https://vim.rtorr.com/>`_


Plantillas automáticas por tipo de fichero (*skeletons*)
------------------------------------------------------------------------

Vim tiene un concepto integrado llamado **archivos esqueleto** que
permite rellenar automáticamente un nuevo archivo con una plantilla
dada. Más información con ``:help skeleton``. La idea general de
los archivos esqueleto es que configures Vim para que lea una plantilla
del disco cada vez que abras un nuevo *buffer* vacío con un nombre de
archivo que coincida con un patrón dado.

Para configurarlo, hay que añadir al ``.vimrc``:


.. code::

    autocmd BufNewFile readme.md 0r ~/skeletons/readme.md
    autocmd BufNewFile *.sh 0r ~/skeletons/bash.sh

Donde:

- ``autocmd``: Ejecuta esto automáticamente ante un evento

- ``BufNewFile``: Este es el evento: Se crea en *buffer* para un nuevo
  fichero.
 
- ``readme.md``: El patrón que debe seguir el nombre del nuevo archivo.

- ``0r``: insertar la plantilla en el *buffer*, empezando por la línea 0.

- ``~/skeletons/readme.md``: La plantilla.


Fuentes:

- VimTricks: `Automated file templates <https://vimtricks.com/p/automated-file-templates/>`_


Cómo posicionar el cursor después de una búsqueda
------------------------------------------------------------------------

Se puede hacer de la siguiente manera:

.. code::

    /Fish/e

La ``/e`` del final posiciona el cursor al final del texto encontrado,
en lugar de posicionarse al principio, que es el comportamiento por
defecto. Además se puede añadir ``-n`` o ``+n`` para posicionar el
cursor ``n`` posiciones antes o después de la posición final.

También se puede usar ``/s[+|-]<num>`` para posicionarse a partir del
principio. Usando ``/Fish/s+2`` te posiciona en la letra ``s``.


Fuente:

- StackOverflow: `Is there a command in Vim/Vi to move the cursor to the end of a search highlight <https://stackoverflow.com/questions/10707626/>`_

Como indentar/desindentar en modo de inserción.
------------------------------------------------------------------------

Si estás en modo inserción, la combinación :keys:`ctrl+t` sirven para
*indentar* la línea actual, mientras que :keys:`ctrl+d` sirve para
*desindentar*. No importa en que posición de la línea esté el cursor. Si
escribes ``0`` y pulsas ++ctrl+d++, la línea se *indentará* al principio
y el ``0`` que escribimos se borra.

Fuente: 

- VimWorkgruop: `Insert mode Ctrl-d <https://github.com/VimWorkgroup/workproducts/blob/master/examples/commands/i_Ctrl-d.md>`_


Como activar/desactivar el corrector de sintaxis
------------------------------------------------------------------------

Para habilitar o inhabilitar el corrector.

- ``:set spell`` activa el corrector. Yo por defecto no tengo habilitado
  el corrector ortográfico. Lo activo cuando voy a redactar un
  documento, pero cuando estoy escribiendo código, me incomoda mucho.

- ``:set nospell`` desactiva el corrector

Si queremos activar el corrector en español:

.. code:: vim

    setlocal spell spelllang=es

Para navegar entre errores:

- ``]s`` te lleva hasta la siguiente palabra errónea. Si precedes esta
  combinación de teclas con un número, saltará tantas palabras erróneas
  como hayas indicado.

- ``[s`` te lleva a la palabra errónea anterior. Igual que en el caso
  anterior, anteponiendo un número, realizará la misma operación.

- ``]S`` funciona igual que ``\]`` pero no tiene en cuenta las palabras
  erróneas de otra región.

- ``[S`` igual que el anterior pero hacia atrás.

Para añadir o eliminar palabras al diccionario

- ``zg`` añade la palabra incorrecta sobre la que está el cursor al
  archivo definido en el parámetro de la configuración ``spellfile``.

- ``zG`` funciona exactamente igual que ``zg`` pero añade la palabra a
  la lista de palabras interna.

- ``zw`` en este caso en lugar de guardar la palabra como correcta, la
  guarda como incorrecta. Así, en el caso de que se encuentre en el
  archivo ``spellfile`` la comentará.

- ``zW`` igual que en el caso anterior, pero en este caso la añade al
  listado interno, tal y como has visto en el caso anterior con ``zg`` y
  ``zG``.

- ``zug`` y ``zuw`` deshacen las acciones de ``zg`` y ``zw``. Lo mismo
  sucede con ``zuG`` y ``zuW``, pero de nuevo en el caso de los listados
  internos.

También es posible realizar estas operaciones utilizando comandos:

- ``[count]spellgood <palabra>`` se comporta como ``zg``

- ``spellgood! <palabra>`` funciona como ``zG``

- ``[count]spellwrong <palabra>`` se comporta como ``zw``

- ``spellwrong! <palabra>`` funciona como ``zW``

Una vez estés sobre una palabra que tienes que corregir, simplemente
tienes que encontrar el reemplazo más adecuado para esa palabra. Para
ello, tienes que utilizar ``z=``. Si estás sobre una palabra incorrecta,
te mostrará un listado de alternativas o posibilidades correctas para
reemplazar la palabra que tienes que corregir.

Fuentes:

-  Atareao: `El corrector ortográfico en Vim <https://atareao.es/tutorial/vim/el-corrector-ortografico-en-vim/>`_

- Jake Harding: `Using Spell Check in Vim <https://thejakeharding.com/using-spell-check-in-vim>`_


Cómo activar el modo Django para plantillas
------------------------------------------------------------------------

Usa ``:setfiletype htmldjango`` en Vim para seleccionar resaltado de
sintaxis de plantillas Django. Si queremos activar el resaltado de
sintaxis solo para Django y no para HTML, podemos usar
``:setfiletype django``.


Cómo integrar Vim con el porta papeles del sistema.
---------------------------------------------------

En los sistemas Unix/Linux hay **dos** porta papeles, independientes
entre si.

- **PRIMARY** - Este porta papeles copia el contenido solo con
  seleccionarlo. Podemos pegarlo normalmente con el botón intermedio del
  ratón (A veces, la rueda de *scroll* que actúa también como botón).

- **CLIPBOARD** - Este porta papeles solo copia lo seleccionado con una
  combinación de tecla, normalmente :keys:`ctrl+c`, y se pega con
  :keys:`ctrl+v` igual que en Windows.

En los sistemas Linux/Unix, hay numerosas utilidades que modifican la
forma en que se sincronizan los porta papeles; si los dos se comportan
como si solo hubiera un porta papales, es probable que haya alguno de
estos programas funcionando.

Vim define dos registros para estos porta papeles:

- ``*`` usa el **PRIMARY**; mnemotécnico: e**S**trella para copia el
  **S**eleccionar.

- ``+`` usa el **CLIPBOARD**; mnemotécnico: Porque hay que seleccionar
  **+** combinación de teclas

En Windows/MAC, ambos registros se refieren al mismo, ya que solo hay un
porta papeles.

Estos registros se usan como cualquier otro registro, por ejemplo, para
cortar (``y``) y pegar (``p``) usando el registro PRIMARY:

.. code:: vim

    "*yy
    "*p

Estos atajos de teclado pueden ser útiles:

..code:: vim

    noremap <Leader>y "*y
    noremap <Leader>p "*p
    noremap <Leader>Y "+y
    noremap <Leader>P "+p

Se puede configurar Vim para que usa por defecto el parta papeles del
sistema ``CLIPBOARD`` en vez del interno, que es el usado por defecto,
usando la variable ``clipboard``:

- Con el valor ``unnamed`` usa ``*`` (``PRIMARY``)

- Con el valor ``unnamedplus`` usa ``+`` (``CLIPBOARD``)

Con estos valores, al copiar con ``yy`` o pegar con ``p`` se estará
trabajando con el porta papeles indicado.

Estos registros también se pueden usar con ``let``:

.. code:: vim

    :let @+=42
    :let @*=42

Al usar **gVim**, se puede activar el comportamiento de "copia al
seleccionar" usado:

.. code:: vim

    :set guioptions+=a

Normalmente esta opción está activa por defecto para GVim, usando el
porta papales ``PRIMARY``, si estamos en Linux/Mac, pero no en Windows o
MAC. Con ``:help 'clipboard'`` podemos ver más opciones de
configuración.

Fuentes:

- Stack Overflow: `How can I copy text to the system clipboard from Vim <https://vi.stackexchange.com/questions/84/how-can-i-copy-text-to-the-system-clipboard-from-vim>`_


Cómo activar/desactivar los números de línea en Vim
------------------------------------------------------------------------

Para activar la numeración, ``:set nu`` o ``set number`` y pulsamos
:keys:`enter` Para desactivar, ``:set nu!`` o ``:set number!``.


Cómo usar el sistema integrado de ayuda
------------------------------------------------------------------------

Está información está disponible con ``:h help-summary``, ``:h howdoi``,
``:h quickref``.

También son útiles ``:h index``, ``:h option-list``, ``:h vim-variable``
y ``:h functions``, y para cosas más avanzadas está ``:h :helpgrep``
para las búsquedas y ``:h help-tags``.

Hay que pulsar ``Ctrl-]`` para seguir el enlace.


Cómo ajustar el directorio de trabajo al del fichero actual
------------------------------------------------------------------------

Podemos ver el directorio actual con:

.. code:: vim

    pwd

Para cambiarlo al directorio del fichero actual:

.. code:: vim

    cd %:p:h

También se puede cambiar el directorio solo para la ventana actual. Cada
ventana mantiene un directorio actual local, que puede ser diferente del
directorio actual global:

.. code:: vim

    lcd %:p:h

En estas ordenes, ``%`` es el nombre del fichero actual, ``%:p`` es el
fichero con el *path* completo, y ``%:p:h`` nos da el directorio, (la
``h`` significa la cabeza o *head* de la ruta completa.

.. note:: Cambiar automáticamente al directorio del fichero en edición

    Para mantener siempre como directorio activo el del directorio que
    estemos editando, podemos poner en el fichero ``.vimrc``:

.. code:: vim

    set autochdir


Cómo abrir una terminal dentro de Vim
------------------------------------------------------------------------

Desde Vim 8.0, hay una orden ``:term`` que abre una terminal en una
ventana nueva. Para salir de la terminal, usa el comando ``exit`` o
simplemente cerrar la ventana con :keys:`ctrl+shift+w` y ``:q``.

Fuentes:

- Stack Overflow: `How do I run a terminal inside of Vim <https://stackoverflow.com/questions/1236563/>`_


Cómo desactivar Syntastic
------------------------------------------------------------------------

Para desactivar Syntactic de la sesión actual:

.. code:: vim

    SyntasticToggleMode

Pare desactivarlo para un lenguaje específico, se puede definir una
lista vacía en la variable correspondiente, en el fichero ``.vimrc``.
Por ejemplo, para desactivar el chequeo de HTML, se podría usar:

.. code:: vim

    let g:syntastic_html_checkers = []


Cómo usar un programa externo como un filtro dentro de Vim
------------------------------------------------------------------------

El siguiente ejemplo es un *script* en Python para ordenar las palabras
de un contenido que se le pasa mediante la entrada estándar:

.. code:: python

    import sys

    for line in sys.stdin:
        print(' '.join(sorted(line.split())))

Por ejemplo, si estamos editando el siguiente texto:

.. code::

    this is a line with some words
    words on each line will be sorted
    fried banana and cream

Podemos usar nuestro programa como un filtro así:

- Pulsar ``V`` en la primera línea, luego ``jj`` para seleccionar las
  tres líneas.

- Escribir ``!python sortwords.py`` y pulsar :keys:`enter`.

Debería producir el siguiente resultado:

.. code::

    a is line some this with words
    be each line on sorted will words
    and banana cream fried

Fuentes:

- Vim fandom: `Use filter commands to process text <https://vim.fandom.com/wiki/Use_filter_commands_to_process_text/>`_


Cómo salir rápidamente de Vim
------------------------------------------------------------------------

Una opción para salvar más rápido:

.. code:: vim

    nmap <Leader>w :update<CR>

Así solo hay que pulsar la tecla *leader*, normalmente :keys:`comma`,
seguido de la tecla ++w++ para salvar, si hay algún cambio. 

.. note:: La orden ``update`` solo salva a disco si tiene que hacerlo.
   Si no hay cambios entre el *bufer* y el fichero no hace nada.

Fuentes:

- Coderwall: `Quick save in vim <https://coderwall.com/p/0tmfjw/quick-save-in-vim>`_


Cómo usar la calculadora del registro
------------------------------------------------------------------------

El registro de expresión de Vim es un registro temporal que permite
ejecutar código. Podemos usarlo para diversas tareas.

Un caso práctico es realizar cálculos matemáticos directamente en Vim e
insertar el resultado en nuestro documento. Para usar el registro de
expresión, presione :keys:`ctrl+r` y luego :keys:`=` desde el modo de
inserción.

Escriba un cálculo simple como ``1 + 2`` y presione ``<enter>``; se
insertará ``3`` en el documento. El registro de expresión es
como una pequeña línea de comandos de Vim que evalúa lo que escriba
e inserta el resultado en su documento.


Fuentes:


- VimTricks: `Performing calculations <https://vimtricks.com/p/performing-calculations/>`_


Búsquedas de texto alternativas
------------------------------------------------------------------------

Si queremos buscar por las palabras ``logging`` o ``logger``:

.. code:: vim

    :/logging\|logger


Caracteres Unicode usados para crear diagramas y cajas
------------------------------------------------------------------------

Este es el conjunto de caracteres definido en el
`Box Drawing Blocl <https://en.wikipedia.org/wiki/Box_Drawing>`_.

.. code::

    0 1 2 3 4 5 6 7 8 9 A B C D E F

    250x  ─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋ ┌ ┍ ┎ ┏
    251x  ┐ ┑ ┒ ┓ └ ┕ ┖ ┗ ┘ ┙ ┚ ┛ ├ ┝ ┞ ┟
    252x  ┠ ┡ ┢ ┣ ┤ ┥ ┦ ┧ ┨ ┩ ┪ ┫ ┬ ┭ ┮ ┯
    253x  ┰ ┱ ┲ ┳ ┴ ┵ ┶ ┷ ┸ ┹ ┺ ┻ ┼ ┽ ┾ ┿
    254x  ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋ ╌ ╍ ╎ ╏
    255x  ═ ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙ ╚ ╛ ╜ ╝ ╞ ╟
    256x  ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬ ╭ ╮ ╯
    257x  ╰ ╱ ╲ ╳ ╴ ╵ ╶ ╷ ╸ ╹ ╺ ╻ ╼ ╽ ╾ ╿

Un ejemplo de uso:

.. code::

    ┌──┬┐  ╔══╦╗  ╓──╥╖  ╒══╤╕  ╭──┬╮  ┏━━┳┓  ┌──┬┒
    │  ││  ║  ║║  ║  ║║  │  ││  │  ││  ┃  ┃┃  │  │┃
    ├──┼┤  ╠══╬╣  ╟──╫╢  ╞══╪╡  ├──┼┤  ┣━━╋┫  ├──┼┨
    └──┴┘  ╚══╩╝  ╙──╨╜  ╘══╧╛  ╰──┴╯  ┗━━┻┛  ┕━━┷┛

Fuentes:

- Wikipedia: `Box-drawing character - Wikipedia <https://en.wikipedia.org/wiki/Box-drawing_character>`_


Definir el área para buscar/reemplazar
------------------------------------------------------------------------

Estos son las expresiones definir el área donde se realizarán las
operaciones de búsqueda/sustitución:

+-----------------+-----------------------------------------------------+
| Expresión       | Descripción                                         |
+=================+=====================================================+
| *number*        | En la linea indicada                                |
+-----------------+-----------------------------------------------------+
| ``.``           | En la línea actual                                  |
+-----------------+-----------------------------------------------------+
| ``$``           | La última línea                                     |
+-----------------+-----------------------------------------------------+
| ``%``           | Todo el contenido del fichero. Equivale a ``1,$``   |
+-----------------+-----------------------------------------------------+
| ``'t``          | En la posición indicada por la marca ``t``          |
+-----------------+-----------------------------------------------------+
| ``/pattern[/]`` | La siguiente línea que case con ``pattern``         |
+-----------------+-----------------------------------------------------+
| ``?pattern[?]`` | La línea anterior que case con ``pattern``          |
+-----------------+-----------------------------------------------------+
| ``\/``          | Línea siguiente a la usada en la búsqueda anterior  |
+-----------------+-----------------------------------------------------+
| ``\?``          | Línea anterior a la usada en la búsqueda anterior   |
+-----------------+-----------------------------------------------------+
| ``\&``          | Siguiente línea que case con el patrón anterior     |
+-----------------+-----------------------------------------------------+

Quantifiers, Greedy and Non-Greedy.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using quantifiers you can set how many times certain part of you pattern
should repeat by putting the following after your pattern:

========== ============================================================
Quantifier Description
========== ============================================================
``*``      Matches 0 or more of the preceding characters
``\+``     Matches 1 or more of the preceding characters…
``\=``     Matches 0 or 1 more of the preceding characters…
``\{n,m}`` Matches from n to m of the preceding characters…
``\{n}``   Matches exactly n times of the preceding characters…
``\{,m}``  Matches at most m (from 0 to m) of the preceding characters…
``\{n,}``  Matches at least n of of the preceding characters
========== ============================================================

Options at the end
~~~~~~~~~~~~~~~~~~

====== ============================================================
letra  Significado
====== ============================================================
``c``  Confirma cada operación
``g``  Reemplaza todas lasocurrencia (sin ``g`` solo la primera)
``i``  Ignora mayúsculas / minúsculas
``I``  No ignora mayúsculas / minúscula
====== ============================================================

Escaped characters or metacharacters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So far our pattern strings were constructed from normal or literal text
characters. The power of regexps is in the use of metacharacters. These
are types of characters which have special meaning inside the search
pattern. With a few exceptions these metacharacters are distinguished by
a “magic” backslash in front of them. The table below lists some common
VIM metacharacters.

====== ===============================================
#      Matching
====== ===============================================
``.``  any character except new line
``\s`` Whitespace character
``\S`` Non-whitespace character
``\d`` Digit
``\D`` Non-digit
``\x`` Hex digit
``\X`` Non-hex digit
``\o`` Octal digit
``\O`` Non-octal digit
``\h`` Head of word character (a,b,c…z,A,B,C…Z and \_)
``\H`` Non-head of word character
``\p`` Printable character
``\P`` Like ``\p``, but excluding digits
``\w`` Word character
``\W`` Non-word character
``\a`` Alphabetic character
``\A`` Non-alphabetic character
``\l`` Lowercase character
``\L`` Non-lowercase character
``\u`` Uppercase character
``\U`` Non-uppercase character
====== ===============================================

Fuentes:


- Vim regex: `Vim Regular Expressions 101 <http://vimregex.com/>`_


Cómo eliminar los espacios al final de las líneas en un fichero
------------------------------------------------------------------------

Usar la siguiente orden:

.. code::

    :%s/\s\+$//e

Explicación: El comando busca en todo el contenido del archivo (``%``),
por el patrón «Uno o más espacios, antes del final de la línea»
(``\s\+$``). El patrón ``\s`` encuentra espacios en blanco, espacios o
tabuladores, ``\+`` significa, la expresión regular anterior, repetida
una o más veces, y ``$`` es el final de la línea. Si los encuentras,
cambiarlos por una cadena vacía (No hay nada en la segunda parte,
``//``)/. Como hemos incluido el modificador final ``e``, no se muestra
mensaje de error aunque no hubiera ninguna línea que cumpla el criterio.

Cómo hacer *Undo* y *ReDo* en Vim
------------------------------------------------------------------------

PAra deshacer un cambio, hay que ponerse en modo comando:

- :keys:`u` deshace el último cambio (se puede usar repetición para deshacer varios campos)

- :keys:`ctrl+r` vuelve a aplicar los cambios que se hubieran desecho (*Redo*)

- :keys:`shift+u` devuelve la última línea modificada a su estado original

- :keys:`colon` vuelve a aplicar los cambios en la línea (deshacer el :keys:`shift+u`)

Desde Vim 7.0, existe la posibilidad
de retroceder o avanzar a cualquier punto de la edición en el tiempo. Por ejemplo, si estoy editando un documento y, después de un par de minutos (digamos 10), me doy cuenta de que he cometido un error, puedo retroceder fácilmente el documento 10 minutos con el comando:

.. code:: vim

    :earlier 10m

Y luego moverte 5 segundos hacia adelante, por ejemplo, con:

.. code:: vim

    :later 5s

Se puede usar el comando ``:undolist`` para ver una lista de las ramas de 
deshacer existentes en el *bufer*. Cada rama tendrá un número asociado y
es posible acceder al nivel de deshacer con el comando ``:undo``.


Usando *viewports*
------------------------------------------------------------------------

A really useful feature in Vim is the ability to split the viewable area
between one or more files, or just to split the window to view two bits
of the same file more easily. The Vim documentation refers to this as a
**viewport** or **window**, interchangeably.

Vim viewport keybinding quick reference

- ``:sp`` will split the Vim window horizontally. Can be written out entirely as ``:split``.

- ``:vsp`` will split the Vim window vertically. Can be written out as ``:vsplit``.

- ``Ctrl-w Ctrl-w`` moves between Vim viewports.

- :keys:`ctrl+w` :keys:`j` moves one viewport down.

- :keys:`ctrl+w` :keys:`k` moves one viewport up.

- :keys:`ctrl+w` :keys:`h` moves one viewport to the left.

- :keys:`ctrl+w` :keys:`l` moves one viewport to the right.

- :keys:`ctrl+w` :keys:`equal` tells Vim to resize viewports to be of equal size.

- :keys:`ctrl+w` :keys:`minus` reduce active viewport by one line.

- :keys:`ctrl+w` :keys:`plus` increase active viewport by one line.

- :keys:`ctrl+w` :keys:`q` will close the active window.

- :keys:`ctrl+w:keys:` `r` will rotate windows to the right.

- :keys:`ctrl+w` :keys:`shift+r` will rotate windows to the left.

The ``:sp`` command will divvy up the viewport into two equal viewports
for the file that you have open. If you’d like to work on two files
simultaneously, no problem – just follow the command with the filename
you’d like to use, like this:

.. code:: vim

    sp filename

let’s say you want to open a reference file in the top viewport, but
want the majority of the viewport available for the file you’re actually
editing. No problem. Just prepend a number to the ``sp`` command, and
the new viewport will fill that number of lines:

.. code:: vim

    10 sp filename

To move between the viewports while working, use :keys:`ctrl+w`
:keys:`j` to move down, and :keys:`ctrl+w` :keys:`k` to move up. This
should prove easy to remember – :keys:`ctrl+w` for "window" commands,
and the normal vi movement commands :keys:`j` for down and :keys:`k` for
up. You can also cycle between viewports by using :keys:`ctrl+w`
:keys:`ctrl+w`

Fuentes:

- Linux.com: `Vim Tipos: Using viewports <https://www.linux.com/learn/vim-tips-using-viewports>`_


Cómo usar sesiones en Vim
------------------------------------------------------------------------

Vim proporciona un sistema para guardar la configuración y el conjunto
de ficheros abiertos en un momento dado, usado **sesiones**.

De ``:help sessiones``:

    Session keeps the Views for all windows, plus the global settings.
    You can save a Session and when you restore it later the window
    layout looks the same. You can use a Session to quickly switch
    between different projects, automatically loading the files you were
    last working on in that project

Con el comando ``:mks`` (o ``:mksession``), Vim guardara en la carpeta
actual un fichero ``Session.Vim``, que es un fichero en vimscript que
restaura la sesión. Si el fichero ya existe, tenemos que forzar a
actualizar con ``:mks!``. También podemos especificar la ruta del
fichero de sesiones particular:

.. code:: vim

    :mksession header-files-work.vim

Para restaurar una sesión en Vim Hay dos maneras: La primera es llamando
a Vim con el parámetro ``-S``, este buscará un fichero ``Session.vim``
en la carpeta actual y, si existe, lo ejecutará, restaurando así la
sesión.

La otra forma sería desde dentro de Vim, ejecutando el comando ``:so``
(o ``:source``), al cual debemos pasarle la ruta al fichero ``.vim``
donde está guardad la sesión.

Fuentes:

- All drops: `Vim Sessions <https://alldrops.info/posts/vim-drops/2020-11-15_vim-sessions/>`_


Cómo plegar/desplegar secciones de texto manualmente
------------------------------------------------------------------------

Hay que posicionarse al principio del bloque que queremos plegar, por
ejemplo, al inicio de la definición de una una función, y pulsar ``mb``,
para poner la marca ``b`` (O cualquier otra marca que queramos). Luego
nos movemos al final y escribimos ``zf'b``

Con ``zd`` podemos borrar el plegado. El texto no se borra, solo el
plegado. Las ordenes ``zo`` y ``zc`` abren y cierran un plegado
respectivamente. Puede ser más fácil usar ``za``, que alterna (*toogle*)
entra ambos estados.

Fuentes:

- Vim Fandom: `Folding <https://vim.fandom.com/wiki/Folding>`_


Vim tab-pages
------------------------------------------------------------------------

Para trabajar con pestañas o *tabs*.

- ``:tabedit file`` abrirá una nueva pestaña y te llevará a editar
  archivo.

- Para navegar entre estas pestañas, puedes usar el modo normal y
  escribir ``gt`` o ``gT`` para ir a la siguiente o a la anterior,
  respectivamente. También puedes navegar a una pestaña de índice
  específica (indexada desde 1) usando ``{i}gt``, donde ``i` es el
  índice de tu pestaña. Ejemplo: ``2gt`` te lleva a la segunda pestaña.

- Para ir directamente a la primera o a la última pestaña, puedes
  escribir lo siguiente en modo comando: ``:tabfirst`` o ``:tablast``
  para la primera o la última pestaña, respectivamente.

- Para avanzar y retroceder, usa ``:tabn`` para la siguiente pestaña y
  ``:tabp`` para la anterior.

- Puedes listar todas las pestañas abiertas usando ``:tabs``.

- Para abrir varios archivos en pestañas: ``$ vim -p source.c source.h``.

- Para abrir varios archivos usando ``find``: ``$ vim -p $(find ...)``.

- Para cerrar una sola pestaña, usa ``:tabclose`` y para cerrar todas
  las demás excepto la actual, usa ``:tabonly``.

- Usa el sufijo ``!`` para anular los cambios en los archivos no guardados.


Cómo usar ctags con Vim
------------------------------------------------------------------------

Ejecutar ``ctags`` en modo recursivo en el directorio que nos interese:

.. code:: shell

    ctags -R *

Para localizar un *tag* determinado y abrir Vim con el fichero que
contienen la definición del mismo, usar:

.. code:: shell

    vim -t <tag>

O, si estamos dentro de Vim, podemos usar los siguienes comandos:

========== ==============================================
Keyboard   command
========== ==============================================
``Ctrl-]`` Jump to the tag underneath the cursor
``Ctrl-t`` Jump back up in the tag stack
``:ts``    Search for a particular tag
``:tag``   Locate a particular tag
``:tn``    Go to the next definition for the last tag
``:tp``    Go to the previous definition for the last tag
``:ts``    List all of the definitions of the last tag
========== ==============================================

El primer comando es seguramente el más usado:
:keys:`ctrl+bracket-right`
salta a la definición de la etiqueta que esta bajo el cursor (Nombres de
funciones, clases, métodos, etc.).

La segunda orden, :keys:`ctrl+t` se usa para regresar, recorriendo el camino
hacia atrás de las búsquedas que hayamos hecho con el primero.

Los siguientes comandos ``:tag``, ``:tn``, ``:tp`` and ``:ts`` pueden
ser usados para buscar cualquier etiqueta, independientemente del
fichero donde pueda estar definida. Si hubiera múltiples candidatos para
la definición, con las ordenes ``tn`` y ``tp`` podemos ir recorriéndolas
de una en una, hacia adelante o hacia atrás, o también podemos usar
``ts`` para seleccionar desde una lista la definición que nos interesa.

Fuentes:

-  Weicode: `Configuring ctags for Python and Vim <https://weicode.wordpress.com/2018/05/01/configuring-ctags-for-python-and-vim/comment-page-1/>`_

.. _`reformatear_el_texto`

Reformatear el texto hasta una determinada anchura
------------------------------------------------------------------------

Definimos la variable ``textwidth`` al máximo ancho que queremos:

.. code:: vim

    :set textwidth=72

Se puede asignar automáticamente y de forma que solo se aplica
a determinados tipos de ficheros (como por ejemplo MarkDown)
en el fichero ``.vimrc``:

.. code:: vim

    au BufRead,BufNewFile *.md setlocal textwidth=72

Fuentes:

- Thoughtbot: `Wrap existing text at 80 characteres in Vim <https://thoughtbot.com/blog/wrap-existing-text-at-80-characters-in-vim>`_

Cómo establecer una línea vertical en Vim
---------------------------------------------

Por ejemplo, para saber donde se formateará el texto automáticamente,
véase :ref:`reformatear_el_texto`_. Solo hay que hacer:

.. code:: vim

    :set colorcolumn=72

Se puede prefijar el valor con ``-`` o ``+`` para poner el marcador
desplazado a la derecha o a la izquierda del valor indicado. También
acepta una serie de valores separados por coma.

Fuentes:

- SuperUser: `How to setup a line length marker in vim/gvim <https://superuser.com/questions/249779/how-to-setup-a-line-length-marker-in-vim-gvim>`_


Cómo eliminar líneas duplicadas
------------------------------------------------------------------------

La siguiente orden ordenará todas las líneas y elminará los duplicados
que hubiese, dejanfo todas las líneas diferentes.

.. code:: vim

    :sort u

Fuentes:

- Vim Fandom: `Removing duplicate lines <https://vim.fandom.com/wiki/Uniq_-_Removing_duplicate_lines>`_


Ordenes básicas de Vim
------------------------------------------------------------------------

The following sections explain the following categories of vi commands.

Moving around in a file
~~~~~~~~~~~~~~~~~~~~~~~

========== ========================================================
Keyboard   Command
========== ========================================================
``Ctrl-b`` Move back one full screen (Remenmber b for backwards)
``Ctrl-f`` Move forward one full screen (Remenmber f for fordwards)
``Ctrl-d`` Move forward 1/2 screen (Remenmber d for down)
``Ctrl-u`` Move back (up) 1/2 screen (Remember u for up)
========== ========================================================

Moving the Cursor When you start vi, the cursor is in the upper left
corner of the vi screen. In command mode, you can move the cursor with a
number of keyboard commands. Certain letter keys, the arrow keys, and
the Return key, Back Space (or Delete) key, and the Space Bar can all be
used to move the cursor when you’re in command mode.

.. note:: La mayoría de las ordenes de Vi distinguen mayúsculas y
   minusculas. La misma letra en mayúsculas o en minúsculas pueden tener
   efectos diferentes, a veces opuestos.

Si las teclas de flechas del teclado no funcionan, se pueden usar estos
sustitutos, el modo comando:

- Para moverse a la izquierda, pulsar ``h``.

- Para moverse a la derecha, pulsar ``l``.

- Para moverse abajo, pulsar ``j``.

- Para moverse arriba, pulsar ``k``.

- Pulsar ``w`` (*word*) para mover el cursor una palabra hacia la
  derecha.

- Pulsar ``b`` (*back*)  para mover el cursor una palabra hacia la
  izquierda.

- Con ``W`` o ``B`` el movimiento sigue hacia la línea anterior o la
  siguiente, según corresponda.

- Pulsar ``e`` (*end*) para mover el cursor al último carácter de la
  palabra sobre la que esta,

- Pulsar ``^`` para mover el cursor al principio de la línea.

- Pulsar ``$`` para mover el cursor al final de la línea.

- Pulsar la tecla de retorno para mover el cursor al principio de la
  siguiente línea.

- Pulsar la tecla de retroceso para mover el cursor un carácter a la
  izquierda.

- Pulsar la barra de espacio para mover el cursor un carácter hacia la
  derecha.

- Pulsar ``H`` (*high*) para mover el cursor a la parte superior de la
  pantalla.

- Pulsar ``M`` (*middle*) para mover el cursor a la parte media de la
  pantalla.

- Pulsar ``L`` (*low*)  para mover el cursor a la parte inferior de la
  pantalla.

- Pulsar ``Ctrl-F`` para moverse una pantalla hacia adelante.

- Pulsar ``Ctrl-D`` para moverse media pantalla hacia adelante.

- Pulsa ``Ctrl-B`` para moverse una pantalla hacia atrás (Es decir,
  hacía el principio del fichero.

- Pulsa ``Ctrl-U`` para  moverse una media pantalla hacia atrás.


Insertando Texto
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

vi provides many commands for inserting text. This section introduces
you to the most useful of these commands. Note that each of these
commands places vi in entry mode. To use any of these commands, you must
first be in command mode. Remember to press Esc to make sure you are in
command mode.

Append Type ``a`` (append) to insert text to the right of the cursor.
Experiment by moving the cursor anywhere on a line and typing a,
followed by the text you want to add. Press Esc when you’re finished.

Type ++shift+a++ to add text to the end of a line. To see how this
command works, position the cursor anywhere on a text line and type
``A``. The cursor moves to the end of the line, where you can type your
additions. Press Esc when you are finished.

Insert text to the left of the cursor by typing ++i++ from command mode.

Type ++shift+i++ to insert text at the beginning of a line. The command
moves the cursor from any position on that line. Press ++esc++ to return
to command mode after you type the desired text.

Open Lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use these commands to open new lines, either above or below the current
cursor position.

Type ``o`` to open a line below the current cursor position. To
experiment, type ``o`` followed by a bit of text. You can type several
lines of text if you like. Press ``Esc`` when you are finished.

Type ``O`` to open a line above the current cursor position.

Changing Text Changing text involves the substitution of one section of
text for another. vi has several ways to do this, depending on
circumstances.

Changing a Word To replace a word, position the cursor at the beginning
of the word to be replaced. Type ``cw``, followed by the new word. To
finish, press ``Esc``.

To change part of a word, place the cursor on the word, to the right of
the portion to be saved. Type ``cw``, type the correction, and press
``Esc``.

Changing a Line To replace a line, position the cursor anywhere on the
line and type ``cc``. The line disappears, leaving a blank line for your
new text (which can be of any length). Press ``Esc`` to finish.

Substituting Character(s) To substitute one or more characters for the
character under the cursor, type ``s``, followed by the new text. Press
``Esc`` to return to command mode.

Replacing One Character Use this command to replace the character
highlighted by the cursor with another character. Position the cursor
over the character and type ``r``, followed by just one replacement
character. After the substitution, vi automatically returns to command
mode (you do not need to press Esc).


Borrando Texto
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These commands delete the character, word, or line you indicate. vi
stays in command mode, so any subsequent text insertions must be
preceded by additional commands to enter entry mode.

Deleting One Character: position the cursor over the character to be
deleted and type ``x``.

The ``x`` command also deletes the space the character occupied—when a
letter is removed from the middle of a word, the remaining letters will
close up, leaving no gap. You can also delete blank spaces in a line
with the ``x`` command.

To delete one character before (to the left of) the cursor, type ``X``
(uppercase).

Deleting a Word or Part of a Word To delete a word, position the cursor
at the beginning of the word and type ``dw``. The word and the space it
occupied are removed.

To delete part of a word, position the cursor on the word to the right
of the part to be saved. Type ``dw`` to delete the rest of the word.

Deleting a Line To delete a line, position the cursor anywhere on the
line and type ``dd``. The line and the space it occupied are removed.

Copying and Moving Text — Yank, Delete, and Put Many word processors
allow you to “copy and paste” and “cut and paste” lines of text. The vi
editor also includes these features. The vi command-mode equivalent of
“copy and paste” is yank and put. The equivalent of “cut and paste” is
delete and put.

The methods for copying or moving small blocks of text in vi involves
the use of a combination of the yank, delete, and put commands.

Copying Lines Copying a line requires two commands: ``yy`` or ``Y``
(“yank”) and either ``p`` (“put below”) or ``P`` (“put above”). Note
that ``Y`` does the same thing as ``yy``.

The ``yy`` command works well with a count: to yank 11 lines, for
example, type ``11yy``. Eleven lines, counting down from the cursor, are
yanked, and vi indicates this with a message at the bottom of the
screen: 11 lines yanked.

You can also use the ``P`` or ``p`` commands immediately after any of
the deletion commands discussed earlier. This action puts the text you
deleted above or below the cursor, respectively.

Fuentes:

- Oracle: `Basic vi Commands <https://docs.oracle.com/cd/E19683-01/806-7612/6jgfmsvqf/>`_

Crear nuestros propios atajos de teclado en Vim
------------------------------------------------------------------------

Key mapping refers to creating a shortcut for repeating a sequence of
keys or commands. Vim supports several editing modes - ``normal``,
``insert``, ``replace``, ``visual``, ``select``, ``command-line`` and
``operator-pending``. You can map a key to work in all or some of these
modes.

The general syntax of a map command is:

.. code::

    {cmd} {attr} {lhs} {rhs}

Donde:

- ``{cmd}`` is one of ``:map``, ``:map!``, ``:nmap``, ``:vmap``,
  ``:imap``, ``:cmap``, ``:smap``, ``:xmap``, ``:omap``, ``:lmap``, etc.

- ``{attr}`` is optional and one or more of the following: ``<buffer>``,
  ``<silent>``, ``<expr> <script>``, ``<unique>`` and ``<special>``.
  More than one attribute can be specified to a map.

- ``{lhs}`` left hand side, is a sequence of one or more keys that you
  will use in your new shortcut.

- ``{rhs}`` right hand side, is the sequence of keys that the {lhs}
  shortcut keys will execute when entered.

Note that you **cannot map** the ++shift++ or ++alt++ or ++ctrl++ keys
alone as they are key modifiers. You have to combine these key modifiers
with other keys to create a map.

The first step in creating a map is to **decide the sequence of keys**
the mapping will run. When you invoke a map, Vim will execute the
sequence of keys as though you entered it from the keyboard. You can
test the keys for your mapping by manually entering the key sequence and
verifying that it performs the desired operation.

The second step is to **decide the editing mode** (insert mode, visual
mode, command-line mode, normal mode, etc.) in which the map should
work. Instead of creating a map that works in all the modes, it is
better to define the map that works only in selected modes.

The third step is to **find an unused key sequence** that can be used to
invoke the map. You can invoke a map using either a single key or a
sequence of keys. :help map-which-keys

Fuentes:

- Vim Fandom: `Mapping Keys in Vim (Part 1) <https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)>`_

- Vim Fandom: `Mapping Keys in Vim (Part 2) <https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_2)>`_

- Vim Fandom: `Mapping Keys in Vim (Part 3) <https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_3)>`_


Vim help and keywordprg
------------------------------------------------------------------------

As you might have heard by now - the best resource for learning Vim is
still the integrated Vim help. Just type ``:help`` or ``:h`` followed by
a help tag and hit the enter key. For example ``:h :s<CR>`` to read and
learn about the substitute command.

But sometimes you don’t know the exact keywords you can use. There are 2
built-in solutions I know of that I constantly use. First is to use the
``TAB`` key to auto-complete the help tags. For example ``:h sub<TAB>``
and this should give you a matching list you can iterate with further
TAB key presses. Select one and hit enter.

The second method is to use the ``:helpgrep`` or ``:lhelpgrep`` command
followed by a keyword. For example ``:lhelpgrep substitute<CR>`` and
this gives you a location list (or quickfix list in case ``:helpgrep``)
showing all occurrences of the given keyword. Use ``:lopen`` or
``:copen`` to show these lists. I suggest here only to learn about that
and to maybe setup some mappings for faster list navigation/usage.

Vim can also show the manuals of the plugins you have installed. I don’t
know if a plugin manager handles that automatically (because I don’t use
one) but I have to update my help tags manually. For that I run
``:helptags path/to/doc/folder<CR>`` for example
``:helptags ~/.vim/doc<CR>`` and now the help tags can be accessed with
the ``:help`` command.

The last but very useful tip is the usage of the ``K`` command. When you
have the Vim help open or when you write a Vim script then you can put
your cursor on help tags or Vim commands and press ``K``. This will
bring you directly to the help of the keyword under the cursor. With
that you can navigate quickly in the Vim help. Use ``Ctrl-o`` to jump
back on the jump list. The ``K`` command makes use of the keywordprg
setting and on some systems this is set up for manpages instead of the
Vim help. So maybe you have to put set ``keywordprg=:help`` in your
vimrc. But manpages can be very useful too for example when writing Bash
scripts. So maybe you want to be able to toggle between the Vim help and
manpages. You could put the following in your vimrc for toggling
(replace with a keystroke you like) …

.. code:: vim

    nnoremap <yourkey> :if &keywordprg == ":help" <BAR> set keywordprg=man <BAR>
        else <BAR> set keywordprg=:help <BAR> endif <BAR> set keywordprg?<CR>

Fuentes:

- Reddit: `Vim help and keyworddprg <https://www.reddit.com/r/vimdailytips/comments/iruu9s/vim_help_and_keywordprg/>`_


Como salvar un fichero protegido si no lo hemos editado como root
------------------------------------------------------------------------

Hay que hacer:

.. code:: vim

    :w !sudo tee %

**Explicación**: La orden ``:w !sudo tee %`` pasará el contenido del
*buffer* actual al comando ``sudo tee %s``, donde ``%`` es el nombre del
fichero actual. Obviamente, nos pedirá la contraseña para poder ejecutar
el comando ``sudo``.

Para entender ``tee``, podemos pensar en este comando como un una unión
de tubería con una entrada y dos salidas. Todo lo que se le pasa a la
entrada estándar de ``tee`` se escribe en el fichero que se le pasa como
parámetro y **también** en la salida estándar, lo que permite seguir
procesando los datos con otro comando.

Por ejemplo, la orden ``ps -ax | tee processes.txt | grep 'foo'`` lista
los procesos, los escribe en el fichero ``processes.txt`` y luego los
filtra usando ``grep``:

.. code::

    ╭───────────╮      ╭────────────╮     ╭─────────────╮
    │           └──────┘            └─────┘             │
    │  ps -ax   ┌──────┐  tee       ┌─────┐  grep 'foo' │
    │           │      │            │     │             │
    ╰───────────╯      ╰─────┐ ┌────╯     ╰─────────────╯
                             │ │
                      ╒══════╛ ╘══════╕
                      │               │
                      │ processes.txt │
                      │             ┌─┤
                      └─────────────┴─╯

En esta situación, sin embargo, ignoramos la mitad de lo que hace
``tee``, ya que descartamos la salida estándar final. Solo usamos
``tee`` para poder ejecutarlo con ``sudo`` y que pueda sobreescribir el
fichero original. La ventaja es que si nos equivocamos con la
contraseña, ``sudo`` fallará y el siguiente comando en el *pipeline*
nunca se ejecutará, impidiendo así que borremos el contenido del
fichero.

Fuentes:

- Stack Overflow: `How does the vim "write with sudo" trick work <https://stackoverflow.com/questions/2600783/>`_


Change gvim GTK file browser the default file mask wildcard (glob)
------------------------------------------------------------------------

The ``browsefilter`` variable is a convenient way to add custom glob
like filters for the graphical :browse dialog and select only the
relevant filetypes for display.

For MS-Windows and GTK, you can modify the filters that are used in the
browse dialog. By setting the ``g:browsefilter`` or ``b:browsefilter``
variables, you can change the filters globally or locally to the buffer.
The variable is set to a string in the format
``"{filter label}\t{pattern};{pattern}\n"`` where ``{filter label}`` is
the text that appears in the “Files of Type” comboBox, and ``{pattern}``
is the pattern which filters the filenames. Several patterns can be
given, separated by ``';'``.

For example, to have only Vim files in the dialog, you could use the
following command:

.. code:: vim

    let g:browsefilter = "Vim Scripts\t*.vim\nVim Startup Files\t*vimrc\n"

You can override the filter setting on a per-buffer basis by setting the
``b:browsefilter`` variable. You would most likely set
``b:browsefilter`` in a **filetype plugin**, so that the browse dialog
would contain entries related to the type of file you are currently
editing. Disadvantage: This makes it difficult to start editing a file
of a different type.

To avoid setting browsefilter when Vim does not actually support it, you
can use has(“browsefilter”):

.. code:: vim

    if has("browsefilter")
        let g:browsefilter = "whatever"
    endif

Fuentes:

- Stack Overflow: `How to change in gvim GTK file browser the default file mask wildcard <https://vi.stackexchange.com/questions/22905/>`_


Cómo posicionarse en una posición u *offset* dentro de una línea
------------------------------------------------------------------------

En modo normal, escribir el número de línea y luego el carácter ``|``,
por ejemplo, para ir a la posición 15 de esta línea (la ``i`` de ir),
escribe ``16|``.

Si no hay suficiente espacio para llegar a esa posición, se sitúa lo más
cerca que pueda


Como hacer *scroll* por el fichero sin mover el cursor
------------------------------------------------------------------------

Para esto Vim tiene unos cuantos comandos:

- :keys:`ctrl+y` Mueve la pantalla una línea hacia arriba

- :keys:`ctrl+e` Mueve la pantalla una línea hacia abajo

- :keys:`ctrl+u` Mueve la pantalla hacia arriba ½ página

- :keys:`ctrl+d` Mueve la pantalla hacia abajo ½ página

- :keys:`ctrl+b` Mueve la pantalla hacia una página entera hacia arriba

- :keys:`ctrl+f` Mueve la pantalla hacia una página entera hacia abajo

- ``zz``: Posiciona la línea actual en el centro de la pantalla

Fuentes:

- Coding potions: `Comandos de Vim para movimientos entre líneas del fichero <https://codingpotions.com/vim-movimientos-verticales/>`_


Cómo posicionar la línea actual en el centro de la pantalla
------------------------------------------------------------------------

Pulsando dos veces zeta: ``zz``. Centra el cursor en mitad de la
pantalla sin moverlo de la línea que estaba.

Fuentes:

- Coding potions: `Comandos de Vim para movimientos entre líneas del fichero <https://codingpotions.com/vim-movimientos-verticales/>`_


Marcas especiales definidas automáticamente por Vim
------------------------------------------------------------------------

Alguna de las más usadas son:

+---------------+-----------------------------------------------------+
| Marca         | Significado                                         |
+===============+=====================================================+
| ``.``         | Posición del ultimo cambio hecho en el *buffer*     |
|               | actual                                              |
+---------------+-----------------------------------------------------+
| ``"``         | Posición en la cual se salvó por última vez este    |
|               | *buffer*                                            |
+---------------+-----------------------------------------------------+
| ``0``         | La posición del último fichero editado al salir de  |
|               | Vim                                                 |
+---------------+-----------------------------------------------------+
| ``1``         | Igual que ``0``, pero el fichero anterior (igual    |
|               | con ``2`` etc.)                                     |
+---------------+-----------------------------------------------------+
| ``''``        | La posición anterior desde la que se saltó          |
+---------------+-----------------------------------------------------+
| ``[`` o ``]`` | Inicio o fin del último texto cambiado o pegado     |
+---------------+-----------------------------------------------------+
| ``<`` o ``>`` | Inicio o fin de la última selección visual          |
+---------------+-----------------------------------------------------+

El listado completo con ``:help '[`` y siguientes.

Fuentes:

- Vim Tips: `Using marks <https://vim.fandom.com/wiki/Using_marks>`_



Cómo cambiar el tipo de fichero de DOS a Unix en Vim
------------------------------------------------------------------------

Con el fichero abierto en un *buffer* de Vim, hacer ``set ff=unix`` y
luego salvar (``ff`` es por *file format*).

Fuentes:

- HashRocket: `Change DOS to Unix text file format in VIM`_


Cómo poner la línea actual en la parte superior/central/inferior
------------------------------------------------------------------------

-  Con :keys:`z+enter` o ``zt`` ponemos la línea actual como la primera
línea de la pantalla.

-  Con ``z.`` o ``zz`` ponemos la línea actual en el centro de la
pantalla.

-  Con ``z-`` o ``zb`` ponemos la línea actual como la última línea de
la pantalla.


Cómo hacer que Vim cargue automáticamente el fichero ``tags``
------------------------------------------------------------------------

Añadir la siguiente linea al fichero ``~/.vimrc``:

.. code::

    set tags=./tags;,tags;

Significa: Busca el fichero ``tags`` en el directorio del fichero
actual, luego asciende por la ruta hasta el directorio de trabajo, luego
sigue hasta el directorio raíz.

Fuentes:

- Stack Overflow: `Automatically load a tag file from a directory ... <https://stackoverflow.com/questions/19330843/>`_


Cómo ejecutar Vim y posicionar el cursor en la primera búsqueda
------------------------------------------------------------------------

Al llamar a Vim, hay que usar un parámetro de la forma
``+/<expresión>``, donde la expresión es una expresión regular para lo
que estamos buscando. Si es una expresión compleja, es mejor
entrecomillarla para que la *shell* no intente interpretarla. Por
ejemplo, para abrir el fichero ``recetas.txt`` y ponernos en la primera
línea que contenga la palabra ``pollo`` seguida de ``limón``, haríamos:

.. code:: shell

    vim  "+/pollo.+limón" recetas.txt

Fuentes:

- Stack Overflow: `Open vim file with cursor on first search pattern`_ 


Cómo editar una macro ya grabada en Vim
---------------------------------------

Una macro no es más que el contenido en un registro. Si queremos cambiar
el registro grabado en la letra ``q``, es simplemente el registro
``@q``. Para simplemente ver el contenido de la macro ``q``:

.. code::

    :echo @q

Igual que cualquier otro registro. También se puede usar ``:registers``
para ver todos los registros.

Ahora, para editarlo, se puede hacer de varias maneras. La más sencilla
es simplemente volver a asignar el contenido al registro, como en el
siguiente ejemplo:

.. code::

    :let @a='iasd<1b>'

La parte que se muestra como ``<1b>`` no es literalmente ese texto; es
el código para ``Escape`` (también se puede mostrar como ``^[``,
dependiendo de tu configuración). Para insertarlo hay que usar la
combinación :keys:`ctrl+v` y luego :keys:`esc`

La macro del ejemplo pasa a modo de inserción (``i``), inserta el texto
``asd``, y pulsa ``Escape`` para volver al modo normal ``<1b>``.

Aunque es factible hacerlo así para macros cortas, no es práctico para
macros más extensas. En estos casos es mejor iniciar un nuevo *buffer*,
con ``:split`` o ``:tabnew``, insertar en él el contenido del registro,
editarlo y luego volver a asignarlo al registro.

Podemos insertar el contenido del registro ``a`` con:

.. code::

    "ap

Tras realizar los cambios que consideremos oportunos, copiaremos
(*yank*) el contenido del *buffer* de regreso al registro ``a`` con:

.. code::

    ^v$"ay

Explicado:

- ``^`` ir al principio de la línea

- ``v`` pasa a modo visual

- ``$`` para ir al final de la línea

- ``"ay`` pega (*yank*) el texto seleccionado en el registro ``a``

.. _How to replace a character by a newline in Vim: https://stackoverflow.com/questions/71323/how-to-replace-a-character-by-a-newline-in-vim
Cómo reemplazar un carácter por un salto de línea en Vim
--------------------------------------------------------

Hay que usar ``\r`` como reemplazo, **no** ``\n``.

Ojo, que para buscar si que se una ``\n``. El siguiente ejemplo
sustituye cada salto de línea por dos saltos de línea:

.. code::

    :%s/\n/\r\r/g

Fuentes:

- Stack Overflow: `How to replace a character by a newline in Vim`_


.. _Change DOS to Unix text file format in VIM: https://til.hashrocket.com/posts/hu3jlszfrf-change-dos-to-unix-text-file-format-in-vim
.. _How to replace a character by a newline in Vim: https://stackoverflow.com/questions/71323/how-to-replace-a-character-by-a-newline-in-vim
.. _Open vim file with cursor on first search pattern: https://stackoverflow.com/questions/39232615/
