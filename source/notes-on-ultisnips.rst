Ultisnips
========================================================================

.. tags:: vim,python,development


UltiSnips y Python
------------------------------------------------------------------------

Para usar **UltiSnips** hay que tener Python activo y usar vim desde la
versión 7 en adelante. Para saber si Python está activo podemos usar:

.. code::

    :echo has("python")

o

.. code::

    :echo has("python3")

Alguno de los dos debería retornar un :math:`1`. UltiSnips intenta
determinar automáticamente la versión de Python que debe usar, pero si
por la que sea queremos forzarla podemos hacer:

.. code::

    let g:UltiSnipsUsePythonVersion = 3


Cómo crear tus propios *snippets*
------------------------------------------------------------------------

Puedes usar ``:UltiSnipsEdit`` para crear o editar un fichero
personalizado, basándose en el tipo de fichero que estés editando en ese
momento. Cuando salves el fichero de *snippets*, los cambios estarán
disponibles de inmediato.

Los *snippets* personalizados se almacenan en la carpeta
``$HOME/.vim/UltiSnips``, con el nombre ``{language}.snippets``, por
ejemplo los *snippets* personales para javascript se encuentran en:

``$HOME/.vim/UltiSnips/javascript.snippets``


Qué son los *spippets*
------------------------------------------------------------------------

Los **Snippets** son pequeñas plantillas de texto que se pueden incluir
en el texto que estés editando usando solo un par de pulsaciones de
teclas.

Vamos a escribir un pequeño *snippet* para incluir mi firma de correo
electrónico usando solo cuatro pulsaciones:

.. code::

    snippet sig "Email signature" b
        Juan Ignacio Rodríguez de León

        --
        Saludos desde las Islas Canarias
        email: menganito@invented-email.com
        phone: xxx-xxx-xxx
    endsnippet

El texto a ser insertado es todo lo incluido desde la palabra
``snippet`` hasta ``endsnipet``. La palabra clave inicial, ``snippet``,
tiene además tres parámetros:

1) El primero es lo que se conoce como el **disparador** o **trigger**,
es la secuencia de caracteres que provocarán la ejecución del
*snippet*. En este caso es la secuencia de caracteres ``sig``, de
forma que para activar la secuencia escribiré ``sig`` y luego pulsare
la tecla :keys:`++tab++`.

Generalmente solo se usa una palabra como disparador, pero se pueden
usar varias separadas por espacios, pero en ese caso hay que
entrecomillar todo el disparador.

2) El segundo parámetro es simplemente una descripción textual del
*snippet*. Es opcional, pero resulta una buena práctica usar un texto
corto pero descriptivo que nos sirva para diferenciar los *snippets*
entre si. También resulta muy útil si tenemos varios *snippets* que
comparte un mismo disparador; en estos casos, *Ultisnips* nos mostrará
una lista de los posibles *snippets* disponibles, usando sus
descripciones, para que el usuario pueda seleccionar el que quiere
usar.

Ejemplo: Escribir dos *snippets* con el mismo *trigger*. Intentar
dispararlo y comprobar que te muestra las opciones disponibles.

.. code::

    snippet sig "Email personal" b
        Juan Ignacio Rodríguez de León

        --
        Saludos desde las Islas Canarias
        email: menganito@invented-email.com
        phone: xxx-xxx-xxx
    endsnippet

    snippet sig "Email trabajo" b
        D. Juan Ignacio Rodríguez de León

        --
        email: mira.que.serio@invented-email.com
        web: http://megaempresa.com/
    endsnippet

3) El tercer y último parámetro son las opciones. Se verán con más
detalle en otra sección, pero para este ejemplo, solo aclarar que la
opción ``b`` (de *begin*) significa que esta regla solo se disparará
si el *snippet* está escrito **al principio de la línea**.

*Snippets* estáticos y dinámicos
------------------------------------------------------------------------

So, for the moment, we only can use this to include some static code.
but snippets could be more elaborated.

Tab Stops and placeholders
~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's see another example. Imagine in your code you need to define
several times some ``user`` entries like this:

.. code:: js

    jileon = {
        "login": "fulanito",
        "uid": 115,
        "gid": 15,
        "email": "fulanito@invented-email.com",
    }

We could make this snippet to help us:

.. code::

    snippet user "User python dict"
        $1 = {
            "login": "$1",
            "uid": $2,
            "gid": $3,
            "email": "$1@invented-email.com",
        }
    endsnippet

Los códigos ``$1``, ``$2``, ``$3``, etc. tienen un significado especial
en *Ultisnips*. Se conocen como *TabStops*. Cunado disparamos el
*snippet*, podemos empezar a escribir directamente el *login* del
usuario, porque el cursor se ha posicionado automáticamente en la
primera posición, es decir, en el *tabstop* `$1`.

.. code::

    jileon = {
        "login": "menganito",
        "uid": ,
        "gid": ,
        "email": "menganito@invented-email.com",
    }

Las marcas se pueden usar en varios sitios. La primera ocurrencia
marca el sitio donde se posiciona el cursor para empezar a escribir. El
resto de las ocurrencias se llaman **espejos** o **Mirrors** porque
reflejan los cambios realizados en la primera marca.

Para verlo, vamos a hacer otro *snippet* para facilitar la escritura
de enlaces a una URL en HTML, de este estilo:

.. code:: html

    <a href="http://www.python.org/">\ http://www.python.org\ <a>

Se podríoa hacer así:

.. code::

    snippet link "Link to a URL"
        <a href="$1">$1</a>
    endsnippet


.. note:: Asociación de los snippets por tipo de fichero

   La orden ``UltiSnipsEdit`` abre una ventana nueva con el fichero
   de *snippets* personalizado para el tipo de archivo que estes
   editando en ese momento. Además, hay una variable de configuración
   llamada ``g:UltiSnipsEditSplit`` que puede valer ``normal`` (que
   es el valor por defecto), ``horizontal`` o ``vertical``, que define
   de que modo se abre la nueva ventana.


Cómo definir las opciones de un *snippet*
------------------------------------------------------------------------

Las opciones controlan el comportamiento de cada *snippet*. Se especifican
con un único caracter. Popdemos combinar las opciones/caracteres para
formar una palabra combinada.

Las opciones actualmente soportadas son:

- ``b``: Inicio (*begin*) de la línea. El *snippet* solo se
  activará con la tecla :keys:`tab` solo si está al principio
  de la línea. Por defecto se activa en cualquier posición en la
  línea.

- ``i``: In-word expansion - By default a snippet is expanded only if
  the tab trigger is the first word on the line or is preceded by one or
  more whitespace characters. A snippet with this option is expanded
  regardless of the preceding character. In other words, **the snippet
  can be triggered in the middle of a word**.

- ``w``: Word boundary - With this option, the snippet is expanded if
  both tab trigger start and end matches a word boundary. In other words
  the tab trigger must be **preceded and followed by non-word
  characters**. Word characters are defined by the 'iskeyword' setting.
  Use this option, for example, to permit expansion where the tab
  trigger follows punctuation without expanding suffixes of larger
  words.

- ``r``: Regular expression - Wih this option, the tab trigger is
  expected to be **a python regular expression**. The snippet is
  expanded if the recently typed characters match the regular
  expression. Note: The regular expression **MUST** be quoted (or
  surrounded with another character) like a multi-word tab trigger (see
  above) whether it has spaces or not. A resulting match is passed to
  any python code blocks in the snippet definition as the local variable
  "match".

- ``t``: Normalmente el tabulador pulsado para disparar el *snippet* se
  descarta, pero con esta opción, se mantiene.

- ``s``: **Remove whitespace immediately before the cursor at the end of
  a line before jumping to the next tabstop**. This is useful if there
  is a tabstop with optional text at the end of a line.

- ``m``: **Trim all whitespaces from right side of snippet lines**.
  Useful when snippet contains empty lines which should remain empty
  after expanding. Without this option empty lines in snippets
  definition will have indentation too.

- ``e``: Custom context snippet - With this option expansion of snippet
  can be controlled not only by previous characters in line, but by any
  given python expression. This option can be specified along with other
  options, like ``b``. See ``UltiSnips-custom-context-snippets`` in help
  for more info.

- ``A``: El *snippet* se dispara automáticamente, sin necesidad de
  dispararlo con la tecla ++tab++.

Fuentes e información adicional
------------------------------------------------------------------------

- Silver's Castle UltiSnips screencast

  - `UltiSnips Screencast Episode 1 <https://www.sirver.net/blog/2011/12/30/first-episode-of-ultisnips-screencast/>`_

  - `UltiSnips Screencast Episode 2 <https://www.sirver.net/blog/2012/01/08/second-episode-of-ultisnips-screencast/>`_:

- `How I'm able to take notes in mathematics lectures using LaTeX and Vim <https://castel.dev/post/lecture-notes-1/>`_

- `A modern vim plugin for editing LaTeX files <https://github.com/lervag/vimtex>`_

- `UltiSnippets screencast <https://www.youtube.com/watch?v=f_WQxYgK0Pk>`_

- `Using selected text in UltiSnips snippets <http://vimcasts.org/episodes/ultisnips-visual-placeholder/>`
