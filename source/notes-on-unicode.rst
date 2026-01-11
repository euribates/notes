Unicode
========================================================================

.. tags:: linux,unicode,graphics


Qué es Unicode
------------------------------------------------------------------------

**Unicode** es un estándar de codificación de caracteres diseñado para
facilitar el tratamiento informático, transmisión, y visualización de
textos de numerosos idiomas y disciplinas técnicas, además de textos
clásicos de lenguas muertas. El término Unicode proviene de los tres
objetivos perseguidos: universalidad, uniformidad, y unicidad.

Unicode define cada carácter o símbolo mediante un nombre e
identificador numérico, el **punto de código** (``code point``). Además
incluye otras informaciones para el uso correcto de cada carácter, como
sistema de escritura, categoría, direccionalidad, mayúsculas y otros
atributos. Unicode trata los caracteres alfabéticos, ideográficos y
símbolos de forma equivalente, lo que significa que se pueden mezclar en
un mismo texto sin utilizar marcas o caracteres de control.

Por ejemplo, el símbolo ``a`` tiene el código de punto :math:`97`. El
``code point`` para el carácter ``✓`` (*Checkmark*) es el :math:`10003`
(:math:`2713`, en hexadecimal). Estos códigos son universales y únicos.
Obsérvese que es este momento no nos estamos preocupando de como se van
a almacenar estos números, Unicode simplemente asigna punto de código
únicos a determinado símbolos gráficos de alfabetos, incluyendo
escrituras históricas extintas, utilizadas con fines académicos, como el
`cuneiforme <https://es.wikipedia.org/wiki/Escritura_cuneiforme>`__ o el
`rúnico <https://es.wikipedia.org/wiki/Alfabeto_r%C3%BAnico>`__,
sistemas ideográficos y otras colecciones de símbolos, como los
utilizados en matemáticas, tecnología, música, iconografía, etc.

Fuentes:

-  `Todo sobre Unicode (en realidad lo mínimo indispensable) · El Blog
de pmoracho <https://pmoracho.github.io/blog/2019/06/04/Unicode/>`__

-  `Unicode: Lo que necesitas saber como programador de Python :: Python
Brasil 2022 <https://www.youtube.com/watch?v=sYWZ23N2Jqg>`__

Caracteres Unicode para el dibujo de cajas (*Box Drawing*)
------------------------------------------------------------------------

Official Unicode Consortium code chart (PDF)

+---------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| Base    | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
+=========+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+
| U+250x  | ─ | ━ | │ | ┃ | ┄ | ┅ | ┆ | ┇ | ┈ | ┉ | ┊ | ┋ | ┌ | ┍ | ┎ | ┏ |
+---------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| U+251x  | ┐ | ┑ | ┒ | ┓ | └ | ┕ | ┖ | ┗ | ┘ | ┙ | ┚ | ┛ | ├ | ┝ | ┞ | ┟ |
+---------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| U+252x  | ┠ | ┡ | ┢ | ┣ | ┤ | ┥ | ┦ | ┧ | ┨ | ┩ | ┪ | ┫ | ┬ | ┭ | ┮ | ┯ |
+---------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| U+253x  | ┰ | ┱ | ┲ | ┳ | ┴ | ┵ | ┶ | ┷ | ┸ | ┹ | ┺ | ┻ | ┼ | ┽ | ┾ | ┿ |
+---------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| U+254x  | ╀ | ╁ | ╂ | ╃ | ╄ | ╅ | ╆ | ╇ | ╈ | ╉ | ╊ | ╋ | ╌ | ╍ | ╎ | ╏ |
+---------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| U+255x  | ═ | ║ | ╒ | ╓ | ╔ | ╕ | ╖ | ╗ | ╘ | ╙ | ╚ | ╛ | ╜ | ╝ | ╞ | ╟ |
+---------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| U+256x  | ╠ | ╡ | ╢ | ╣ | ╤ | ╥ | ╦ | ╧ | ╨ | ╩ | ╪ | ╫ | ╬ | ╭ | ╮ | ╯ |
+---------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| U+257x  | ╰ | ╱ | ╲ | ╳ | ╴ | ╵ | ╶ | ╷ | ╸ | ╹ | ╺ | ╻ | ╼ | ╽ | ╾ | ╿ |
+---------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+

Símbolos tipográficos útiles en Unicode
------------------------------------------------------------------------

Miscelanea
~~~~~~~~~~

== ========== =============================
S  code point Desc
== ========== =============================
⚠  ``26A0``   Warning sign
✓  ``2713``   Check mark
✅ ``2705``   White heavy check mark
⚡ ``26A1``   High voltage sign
☎  ``9742``   Phone (Black)
✉  ``9993``   Envelope
✖  ``2716``   Heavy multiplication
✗  ``2717``   Cross mark
⛔ ``26D4``   No entry
§  ``00A7``   Section
¶  ``00B6``   Paragraph
·  ``00B7``   Middle dot
†  ``2020``   Dagger
‡  ``2021``   Double dagger
•  ``2022``   Bullet
…  ``2026``   Ellipsis
←  ``2190``   Left arrow
↑  ``2191``   Up arrow
→  ``2192``   Right arrow
↓  ``2193``   Down arrow
►  ``25BA``   Black right-pointing poi nter
◄  ``25C4``   Black left-pointing pointer
▲  ``25B2``   Black up-pointing triangle
▼  ``25BC``   Black down-pointing triangle
△  ``25B3``   White up-pointing triangle
▽  ``25BD``   White down-pointing triangle
☐  ``2610``   Ballot box
☑  ``2611``   Ballot box check
☒  ``2612``   Ballot box X
★  ``2605``   Black star
☆  ``2606``   White star
□  ``25A1``   Square
☠  ``2620``   Skull and crossbones
== ========== =============================

Lógica
~~~~~~

= ========== ============
S code point Desc
= ========== ============
¬ ``00AC``   Logical NOT
∧ ``2227``   Logical AND
∨ ``2228``   Logical OR
∎ ``220E``   End of proof
∴ ``2234``   Therefore
∵ ``2235``   Because
∀ ``2200``   For all
∃ ``2203``   Exists
∄ ``2204``   Not Exists
= ========== ============

Fracciones
~~~~~~~~~~

= ========== ==============
S code point Fractions
= ========== ==============
½ ``00BD``   one-half
⅓ ``2153``   one-third
⅔ ``2154``   two-thirds
¼ ``00BC``   one-quarter
¾ ``00BE``   three-quarters
⅕ ``2155``   one-fifth
⅖ ``2156``   two-fifths
⅗ ``2157``   three-fifths
⅘ ``2158``   four-fifths
⅙ ``2159``   one-sixth
⅚ ``215A``   five-sixths
⅐ ``2150``   one-seventh
⅛ ``215B``   one-eighth
⅜ ``215C``   three-eighths
⅝ ``215D``   five-eighths
⅞ ``215E``   seven-eighths
⅑ ``2151``   one-ninth
⅒ ``2152``   one-tenth
= ========== ==============

Power symbols
~~~~~~~~~~~~~

= ========== ============
S code point Fractions
= ========== ============
⏻ ``23FB``   Power
⏼ ``23FC``   Toggle power
⏽ ``23FD``   Power on
⭘ ``2B58``   Power off
⏾ ``23FE``   Sleep mode
= ========== ============

Social Networking
~~~~~~~~~~~~~~~~~

== ========== ===========
S  code point Fractions
== ========== ===========
👍 ``1F44D``  Thumbs Up
👎 ``1F44E``  Thumbs Down
== ========== ===========

Fuente: `Unicode List of useful sym`_

.. _Unicode List of useful sym: https://en.wikibooks.org/wiki/Unicode/List_of_useful_symbols

UTF-16
------------------------------------------------------------------------

**UTF-16**, es una forma de codificación de caracteres Unicode
utilizando símbolos de longitud variable, pero usando palabras de 16
bits, en vez de bytes. Para codificado un ``code point`` su usan 1 o 2
palabras de 16 bits por carácter Unicode (2 o 4 bytes).

Por ejemplo, el texto "Hello", un UTF-16, se codifica, (usando
hexadecimal), como:

.. code::

    0048 0065 006C 006C 006F
    ---- ---- ---- ---- ----
    H    e    l    l    o

UTF-8
-----

UTF-8 es un sistema (De entre otros varios posibles, como el UTF-16)
para almacenar los *code points* de Unicode, usando bytes de 8 bits, en
vez de palabras de 18 bits. En UTF-8, cada punto de código de 0-127 se
almacena en un solo byte. Sólo los puntos de código 128 y superiores se
almacenan utilizando 2, 3, y de hecho, hasta 6 bytes.

Esto tiene el efecto secundario –y deseado– de que el texto en inglés se
ve **exactamente igual en UTF-8 que en ASCII**,

Específicamente, "Hello", que era ``00480065006C006C006F`` en UTF-16,
se almacenará como ``48656C6C6F`` en UTF-8, que es lo mismo que se
almacenaba en ASCII, ANSI, y en todos los juegos de caracteres OEM.

Cosas que hay que tener en cuenta al trabajar con UTF-8
------------------------------------------------------------------------

**NO se puede** determinar la longitud de una cadena de texto
simplemente contando los bytes.

**NO se puede** saltar directamente a una posición aleatoria dentro de
una cadena de texto y asumir que a partir de ahí se puede leer texto;
podríamos estar en medio de un carácter que usara más de un byte, y eso
provoca que el resto se interprete incorrectamente.

**No se puede** dividir u obtener una subcadena de texto cortando en una
posición aleatoria, por las mismas razones que el punto anterior.
