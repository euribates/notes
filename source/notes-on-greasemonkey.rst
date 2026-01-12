Greasemonkey
========================================================================

.. tags:: development,web,javascript


Qué es Greasemonkey
-------------------

`Greasemonkey <https://www.greasespot.net/>`__ es una extensión para el
navegador Mozilla Firefox e Iceweasel que permite, por medio de pequeñas
porciones de código creadas por usuarios, modificar el comportamiento de
páginas web específicas. Con esta extensión es posible mejorar la
experiencia de lectura de un sitio web, hacerlo más utilizable, añadir
nuevas funciones a las páginas web, corregir errores, mejorar servicios
de búsquedas y muchas cosas más.

Hola, mundo en Greasemonkey
---------------------------

Pues algo así:

.. code:: javascript

    // ==UserScript==
    // @name testName
    // @namespace anonDeveloper
    // @description This script will automagically blah blah blah
    // @include *
    // ==/UserScript==
    alert('Hello world!');

Salvar el fichero como ``'hola.user.js'``.

Fuentes:

- `Greasemonkey - Wikipedia, la enciclopedia
libre <https://es.wikipedia.org/wiki/Greasemonkey>`__
