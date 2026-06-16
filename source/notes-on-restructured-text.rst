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

Imágenes y figuras con ReestructuredText
------------------------------------------------------------------------

La directiva ``image`` se utiliza con un argumento obligatorio: el
directorio o dirección donde se ubica la imagen. Por ejemplo, aquí
debajo se muestra una imagen:

.. image:: reestructured-text/incredibles.jpeg

Con eso basta para que reST pueda ir por la imagen y colocarla en el HTML
final. No obstante, y dependiendo del ancho de la salida, el contenido
puede desbordar los márgenes disponibles. Esto pasa porque reST no le hace
ningún tipo de procesamiento o escalado a la imagen por defecto. 


La directiva acepta varias opciones que permiten darle formato a la imagen:

- ``height``: es el alto de la imagen, utilizado para reservar espacio
  vertical para la imagen. Cuando se utiliza en conjunto con la opción
  de ``scale``, ambos se aplican (por ejemplo, escala al 40% de 100px da
  40px). 

- ``width``: es el ancho de la imagen, y puede ser en términos absolutos
  o en porcentaje. De manera análoga a la altura, se combina con la opción
  de escala.

- ``scale``: es un factor de escalamiento, en porcentaje, que se aplicará a
  la imagen (el símbolo de porcentaje puede omitirse). El valor
  predeterminado es 100% (sin escalamiento).

- ``align``: la alineación de la imagen, puede tener los siguientes
  valores: ``top``, ``middle``, ``bottom``, ``left``, ``center``, o
  ``right``. Los primeros tres valores hacen referencia a la alineación
  vertical, mientras que los últimos tres hacen referencia a su posición
  horizontal.

- ``alt``: es un texto alternativo a utilizar en caso de que no se pueda
  desplegar la imagen. También es el texto que se lee por aplicaciones de
  asistencia visual.

- ``target``: convierte la imagen en un enlace hacia la URL especificada.

Una **figura** es una imagen con una leyenda debajo. Su sintaxis es
similar a la de ``image``, y acepta las mismas opciones, solo que agrega
el contenido de la directiva, que corresponde a la leyenda que se
colocará debajo de la imagen:

Veamos la misma imagen anterior, pero con un ancho limitado a 500 píxeles:



.. figure:: reestructured-text/incredibles.jpeg
    :width: 50%
    :align: center

    Los Increibles

Qué en ReST sería:


.. code::

    .. figure:: reestructured-text/incredibles.jpeg
       :width: 50%
       :align: right

       Los Increibles



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

.. [1] NO confunfir con el acrónimo REST: *Representational State
   Transfer*, con el que no tiene nada que ver.

.. _DocUtils: https://www.docutils.org/


