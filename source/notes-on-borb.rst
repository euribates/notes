Borb
========================================================================

Qué es Borb
------------------------------------------------------------------------

**Borb** es una librería en Python para generar PDF, desarrollada por
Joris Schellekens.

El “hola, mundo” en Borb
------------------------------------------------------------------------

.. code:: python

    from borb.pdf import Document, Page, PageLayout, Paragraph, PDF, SingleColumnLayout
 
    d: Document = Document()                           # Create an empty Document
    p: Page = Page()                                   # Create an empty Page
    d.append_page(p)
    l: PageLayout = SingleColumnLayout(p)              # Create a PageLayout
    l.append_layout_element(Paragraph("Hello World!")) # Add a Paragraph
    PDF.write(what=d, where_to="hello-world.pdf")      # Write the PDF

.. warning:: NO USAR: Realiza conexiones a un servidor

   Aparentemente con propósitos
   estadísticos, pero vete tu a saber. Mejor usar `fpdf2`_.


Componentes de Borb
------------------------------------------------------------------------

En el paquete ``orb.pdf`` están contenidas las clases y funciones que
permiten crear y modificar documentos PDF:

-  ``Document``: Representa un documento PDF.

-  ``Page``: Representa una página individual dentro de un PDF.

-  ``PageLayout``: Una clase abstracta que define como se distribuye el
   contenido dentro de una página .

-  ``SingleColumnLayout``: Una implmentación concreta de ``PageLayout``,
   que distribuye los contenidos un una única columna.

-  ``Paragraph``: El bloque básico de funcionalidad que nos permite
   añadir contenido textual a un PDF.

-  ``PDF``: Proporciona la capacidad de escribir un onjeto ``Document``
   a un archivo.


.. _fpdf2: https://pypi.org/project/fpdf2/
