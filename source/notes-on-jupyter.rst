Jupyter
========================================================================

.. tags:: python,ia,science,bigdata

.. contents:: Relación de contenidos
    :depth: 3

Qué es Jupyter
------------------------------------------------------------------------

:index:`Jupyter` es una plataforma agnóstica, que soporta varios entornos de
ejecución (también conocidos como núcleos) en varias docenas de
lenguajes, entre los que se encuentran Julia, R, Haskell, Ruby y, por
supuesto :doc:`notes-on-python` (a través del kernel de IPython).

El nombre del proyecto Jupyter es una referencia a los tres lenguajes de
programación principales originalmente soportados por Jupyter: Julia,
Python y R, y también un homenaje a los cuadernos de Galileo que
registran el descubrimiento de los satélites de Júpiter. El proyecto
Jupyter ha desarrollado y respaldado los productos de computación
interactiva Jupyter Notebook, JupyterHub y JupyterLab, la versión de
próxima generación de Jupyter Notebook.


Formas de extender Jupyter
------------------------------------------------------------------------

- Source: https://mindtrove.info/4-ways-to-extend-jupyter-notebook/

Tutorial: Advanced Jupyter Notebooks
------------------------------------------------------------------------

- https://www.dataquest.io/blog/advanced-jupyter-notebooks-tutorial/

With tips about debugging, executing different languages, extensions,
working with databases and styling notebooks, among other thigs.

Jupyter Magics con SQL
-----------------------------------------------------------------------

- https://towardsdatascience.com/jupyter-magics-with-sql-921370099589

Jupyter/IPython notebooks can be used for an interactive data analysis
with SQL on a relational database. This fuses together the advantages of
using Jupyter, a well-established platform for data analysis, with the
ease of use of SQL and the performance of SQL engines.

Nóciones básicas de Latex
-----------------------------------------------------------------------

- http://www.malinc.se/math/latex/basiccodeen.php

10 Simple hacks to speed up your Data Analysis in Python
-----------------------------------------------------------------------

- https://towardsdatascience.com/10-simple-hacks-to-speed-up-your-data-analysis-in-python-ec18c6396e6b


Cómo definir el tamaño de las columnas de Pandas en Jupyter
------------------------------------------------------------------------

Por defecto, Jupyter muestra las columnas de los *Dataframes* en un tamaño fijo, pero se le
puede indicar que ajuste el ancho de las columnas para que se vea todo su contenido con la
siguiente llamada:

.. code:: python

    import pandas as pd

    pd.set_option('display.max_colwidth', None)

Fuente: `Pandas How to Set Column Widths`_ - Statology_

.. _statology: https://www.statology.org/
.. _Pandas How to Set Column Widths: https://www.statology.org/pandas-column-width/
