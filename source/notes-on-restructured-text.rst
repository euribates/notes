Restructured-text
========================================================================


Sobre ReStructeredText
----------------------

**ReStructured Text** es un lenguaje de marcas ligero creado para
escribir textos con formato definido de manera cómoda y rápida. Es parte
del proyecto `Docutils`_ dentro de la comunidad de Python, y es
formalizado por el grupo Python Doc-SIG (*Documentation Special Interest
Group*).  Tiene la principal ventaja de que ese texto puede usarse para
generar documentos equivalentes en HTML, LaTeX, docbook, etc.

A menudo, el término Restructured Text es abreviado a ReST o reST [1]_.


Matemáticas en reStructuredText con LaTeX
------------------------------------------------------------------------

La sintaxis es la misma que se usa en los ficheros latex Math, pero sin
las marcas de ``$``. En vez de eso, se engloba la expresión matemática
con la directiva ``math``:

Así, este código ReST:

.. code::

    .. math::
        \frac{ \sum_{t=0}^{N}f(t,k) }{N}

Se ve:

.. math::
    \frac{ \sum_{t=0}^{N}f(t,k) }{N}


También existe la versión en *rol* para expresiones matemáticas
en línea. El siguiente testo ReST:

.. code::

    La formula es :math:`\sum_{t=0}^{N}f(t,k)`.

Se ve:

    La formula es :math:`\sum_{t=0}^{N}f(t,k)`.

Obsérvese el uso de las comillas inversas para delimitar la formula.

Fuentes:

- StackOverflow: `Math in restructured text with Latex <https://stackoverflow.com/questions/3610551/math-in-restructuredtext-with-latex>`_

.. _[1]: NO confunfir con el acrónimo REST: *Representational State
   Transfer*, con el que no tiene nada que ver.

.. _DocUtils: https://www.docutils.org/
