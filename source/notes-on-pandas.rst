Pandas
========================================================================

.. tags:: python,pandas,math


Notas sobre :index:`Pandas`
------------------------------------------------------------------------

La librería **Pandas** es una biblioteca de código abierto muy popular
entre los desarrolladores de Python, especialmente en los campos de la
`ciencia de datos`_ y el aprendizaje automático, porque proporciona
estructuras de datos muy potentes y flexibles.

Pandas surge por la necesidad de tener una biblioteca con todas las
funciones necesarias para cargar datos, limpiarlos, modelarlos,
analizarlos, manipularlos y prepararlos.


Usar pandas para hacer un (inner) join
------------------------------------------------------------------------

**tldr**: Usa la función `merge`_ de
pandas.


Supongamos las siguientes tablas:

.. code:: python

    pesos = pd.DataFrame.from_dict({
        'palabra': ['economia', 'educacion', 'turismo', 'videojuego'],
        'pesos': [.12, .33, .88, -0.73]
        })

== ========== =====
\  palabra    pesos
== ========== =====
0  economia   0.12
1  educacion  0.33
2  turismo    0.88
3  videojuego -0.73
== ========== =====

.. code:: python

    muestra = pd.DataFrame.from_dict({
        'palabra': ['el', 'videojuego', 'del', 'gran', 'turismo', 'es', 'fantastico'],
        'total': [1, 1, 1, 1, 1, 1, 1]
        })

== ========== =====
\  palabra    total
== ========== =====
0  el         1
1  videojuego 1
2  del        1
3  gran       1
4  turismo    1
5  es         1
6  fantastico 1
== ========== =====

Podemos hacer un *join* usando la función ``merge``. Los dos primeros
parámetros son obligatorios y son los *dataframes* con los datos. Si la
columna por la que queremos hacer el *join* se llama igual en ambos
*dataframes*, podemos usar el parámetro opcional ``on``:

.. code:: python

    pd.merge(pesos, muestra, on='palabra')

El resultado debería ser:

== ========== ===== =====
\  palabra    pesos total
== ========== ===== =====
0  turismo    0.88  1
1  videojuego -0.73 1
== ========== ===== =====

Si los nombres de las columnas no coinciden, podemos usar los dos
parámetros opcionales ``left_on`` y ``right_on``. Vamos a redefinir el
*dataframe* ``muestra`` para cambiar el nombre de la columna de
``palabra`` a ``termino``:

.. code:: python

    muestra = pd.DataFrame.from_dict({
        'termino': ['el', 'videojuego', 'del', 'gran', 'turismo', 'es', 'fantástico'],
        'total': [1, 1, 1, 1, 1, 1, 1]
        })

== ========== =====
\  termino    total
== ========== =====
0  el         1
1  videojuego 1
2  del        1
3  gran       1
4  turismo    1
5  es         1
6  fantástico 1
== ========== =====

.. code:: python

    pd.merge(pesos, muestra, left_on='palabra', right_on='termino')

== ========== ===== ========== =====
\  palabra    pesos termino    total
== ========== ===== ========== =====
0  turismo    0.88  turismo    1
1  videojuego -0.73 videojuego 1
== ========== ===== ========== =====

Fuente:

- `Joins in Pandas`_


Como saber si una serie de Pandas tiene valores NaN
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pandas ofrece un atributo que nos da justo esa información, llamado
`hasnans`_:

.. code:: python

    series = pd.Series([2, 4, 6, "sadf", np.nan])
    assert series.hasnans is True


25 funciones de Pandas
------------------------------------------------------------------------

Fuente: https://towardsdatascience.com/25-pandas-functions-you-didnt-know-existed-p-guarantee-0-8-1a05dcaad5d0

Cheatsheets
------------------------------------------------------------------------

-  `Python <http://www.utc.fr/~jlaforet/Suppl/python-cheatsheets.pdf>`_
-  `Numpy <https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Numpy_Python_Cheat_Sheet.pdf>`_
-  `Pandas <https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf>`_


Cómo crear un *DataFrame* de pandas a partir de una tabla Html
------------------------------------------------------------------------

The basic usage is of pandas ``read_html`` is pretty simple and works
well on many Wikipedia pages since the tables are not complicated. To
get started, I am including some extra imports we will use for data
cleaning for more complicated examples:

.. code:: python

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from unicodedata import normalize

    table_MN = pd.read_html("https://en.wikipedia.org/wiki/Minnesota")

The unique point here is that ``table_MN`` is a list of all the tables
on the page:

.. code:: python

    print(f"Total tables: {len(table_MN)}")
    Total tables: 38

With **38** tables, it can be challenging to find the one you need. To
make the table selection easier, use the ``match`` parameter to select a
subset of tables. We can use the caption "Election results from
statewide races" to select the table:

.. code:: python

    table_MN = pd.read_html(
        "https://en.wikipedia.org/wiki/Minnesota",
        match="Election results from statewide races"
        )
    assert len(table_MN) == 1

Source: `Reading HTML tables with Pandas - Practical Business <https://pbpython.com/pandas-html-table.html>`_

Diferentes formas de crear un *Dataframe*
------------------------------------------------------------------------

Existe muchas formas diferentes de crear un *DataFrame*:

-  A partir de una **lista da listas**:

  .. code:: python
  
      data = [['tom', 10], ['nick', 15], ['juli', 14]]
      df = pd.DataFrame(data, columns = ['Name', 'Age'])

- A partir de un **diccionario de listas**:

  To create DataFrame from dict of narray/list, all the narray must be
  of **same length**. If index is passed then the length index should be
  equal to the length of arrays. If no index is passed, then by default,
  index will be ``range(n)`` where ``n`` is the array length.

  .. code:: python

      data = {'Name':['Tom', 'nick', 'krish', 'jack'], 'Age':[20, 21, 19, 18]}
      df = pd.DataFrame(data)

- Creates a indexes DataFrame **using arrays**:

  .. code:: python
  
      data = {'Name':['Tom', 'Jack', 'nick', 'juli'], 'marks':[99, 98, 95, 90]}
      df = pd.DataFrame(data, index =['rank1', 'rank2', 'rank3', 'rank4'])

- A partir de una **lista de diccionario**:

  Pandas DataFrame can be created by passing lists of dictionaries as a
  input data. By default dictionary keys taken as columns.

  .. code:: python
  
      data = [{'a': 1, 'b': 2, 'c':3}, {'a':10, 'b': 20, 'c': 30}]
      df = pd.DataFrame(data)

- Creating DataFrame **from Dicts of series**:

  To create DataFrame from Dicts of series, dictionary can be passed to
  form a DataFrame. The resultant index is the union of all the series
  of passed indexed.

.. code:: python

    d = {
    'one' : pd.Series([10, 20, 30, 40], index =['a', 'b', 'c', 'd']),
    'two' : pd.Series([10, 20, 30, 40], index =['a', 'b', 'c', 'd'])
    }
    df = pd.DataFrame(d)

- A partir de un **fichero CSV**:

  Sólo hay que llamar el método ``load_csv``.

  .. code:: python
  
      df = pd.read_csv('example.csv')

  Funciona también con URLS:

  .. code:: python

      df = pd.read_csv('http://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv')

  Si el fichero CVS no tiene una primera línea con cabeceras:

  .. code:: python

      df = pd.read_csv('example.csv', header=None)

- A partir de una **consulta a la base de datos**:

  .. code:: python

      db = MySQLdb.connect(host='localhost', db='comics', user='stan.lee', passwd='mske')
      df1 = pd.read_sql_query(sql, db, index_col='holding_id')


Cómo cambiar el tamaño de las imágenees creadas con matplotlib
------------------------------------------------------------------------

Hay que usar el parámetro ``figsize``, pero la clave es que hay que
hacerlo antes de empezar a dibujar:

.. code:: python

    from matplotlib import pyplot as plt
    plt.figure(figsize=(1,1))
    x = [1,2,3]
    plt.plot(x, x)
    plt.show()


Cómo usar una columna de un *DataFrame* como índice
------------------------------------------------------------------------

Pandas ``set_index()`` is a method to set a List, Series or Data frame
as an index of a Data Frame. The index object is an immutable array.
Indexing allows us to access a row or column using the label.

The syntax for Pandas Set Index is following.

DataFrame.set_index(keys, drop=True, append=False, inplace=False,
verify_integrity=False) Set the DataFrame index (row labels) using one
or more existing columns. By default yields the new object.

- ``keys``: Column name or list of a column name.

- ``drop``: It’s a Boolean value which drops the column used for the
    index if True.

- ``append``: It appends the column to the existing index column if
True.

- ``inplace``: It makes the changes in the DataFrame if True.

- ``verify_integrity``: It checks the new index column for duplicates if
  True.

We will use Real data which can be found on the following google doc
link:

- https://docs.google.com/spreadsheets/d/1zeeZQzFoHE2j_ZrqDkVJK9eF7OH1yvg75c8S-aBcxaU/edit#gid=0

Okay, now we will use the ``read_csv()`` method:

.. code:: python

    data = pd.read_csv('data.csv', skiprows=4)

Remember that the index data is **immutable** and we can not be able to
change that in any circumstances.

Cómo añadir una columna a un *DataFrame*
------------------------------------------------------------------------

A partir de Pandas 0.16.0, se puede usar el método ``assign``, que añade
columnas nuevas al **DataFrame**, devolviendo una copia del nuevo con las
nuevas columnas. El siguiente código:

.. code:: python

    d = pd.DataFrame({'a': [1, 2, 7], 'b': [3, 4, 21]})
    d = d.assign(suma=d['a']+d['b'])
    d = d.assign(media=d.suma/2)

Devuelve:

===== = == ==== =====
index a b  suma media
===== = == ==== =====
0     1 3  4    2.0
1     2 4  6    3.0
2     7 21 28   14.0
===== = == ==== =====

Cómo visualizar datos
------------------------------------------------------------------------

We use the standard convention for referencing the matplotlib API:

.. code:: python

    import matplotlib.pyplot as plt
    plt.close('all')

Cómo usar plot
------------------------------------------------------------------------

The plot method on Series and DataFrame is just a simple wrapper around
plt.plot():

Example using series:

.. code:: python

    ts = pd.Series(
        np.random.randn(1000),
        index=pd.date_range('1/1/2000', periods=1000),
        )
    ts = ts.cumsum()
    ts.plot()

.. figure:: ./pandas/plot.png
   :alt: Example of Series plot

En un *dataFrame*, el método ``plot()`` es una forma muy cómoda de
representar todas las columnas con sus etiquetas:

.. code:: python

    df = pd.DataFrame(
        np.random.randn(1000, 4),
        index=ts.index,
        columns=list('ABCD'),
        )
    df = df.cumsum()
    plt.figure()
    df.plot()

.. figure:: ./pandas/sample-dataframe-plot.png
   :alt: Ejemplo de una llamada al método plot


Como hacer un select o filtrado por columnas un Pandas
------------------------------------------------------------------------

Para filtrar con condiciones, escribimos la condición dentro de
corchetes. Por ejemplo, si deseamos mostrar a los que tienen en la
columna ``votos`` un valor superior o igual a doscientos mil, podemos
escribir:

.. code:: python

    df[df.votes>200000]

La expresión dentro de los corchetes, al evaluarse, devuelve un vector
de valores *booleanos*, según la expresión indicada. Al usar esa matriz
como índices, se eliminan todas las filas para las que el valor lógico
correspondiente sea false.

Si queremos filtrar por dos o más condiciones, podemos combinar los
vectores booleanos usando operadores lógicos (``&`` para ``and`` y ``|``
para ``or``) y usar el vector resultante para realizar el filtrado. El
siguiente ejemplo selecciona las filas en las que el campo ``county`` es
``Manhattan`` y el campo ``party`` es ``Democrat``:

.. code:: python

    df[(df.county=='Manhattan') & (df.party=='Democrat')])


Cómo renombrar columnas en Pandas
------------------------------------------------------------------------

Para renombre una columna en Pandas usaremos el método
`rename`_. Acepta un parámetro, ``columns``, que puede ser o una función o un
diccionario, y que es la responsable de *mapear* los nombres originales
con los nuevos. Si usamos un diccionario, por ejemplo, para cada una de
sus entradas, la clave se corresponde con el nombre de la columna
original, mientras que el valor será el nuevo nombre de la columna.

Tiene un parámetro opcional, ``inplace``, que hará el cambio modificando
el propio *dataframe*. Si está a ``False`` (El valor por defecto),
devolverá una copia del *dataframe* con los nombres de las columnas
modificados.

.. code:: python

    df = pd.DataFrame({'a': [1,2,3], 'b': [4,5,6]})
    new_df = df.rename(columns={'a': 'Alfa', 'b': 'Beta'}, inplace=False)
    print(new_df)

Debería devolver:

== ==== ====
\  Alfa Beta
== ==== ====
0  1    4
1  2    5
2  3    6
== ==== ====

Cómo ordenar las filas de un DataFrame
------------------------------------------------------------------------

Hay varios métodos, el más simple es usar el método ``sort_values``. Con
el parámetro ``by`` indicamos las columnas por las que queremos ordenar,
y con el parámetro ``ascending``, que es un booleano, indicamos el
sentido de la ordenación.

Por ejemplo:

.. code:: Python

    df.sort_values(by='column_name', ascending=True)

.. _hasnans: https://pandas.pydata.org/docs/reference/api/pandas.Series.hasnans.html#pandas.Series.hasnans
.. _ciencia de datos: https://es.wikipedia.org/wiki/Ciencia_de_datos
.. _`merge`: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
.. _`Joins in Pandas`: https://www.analyticsvidhya.com/blog/2020/02/joins-in-pandas-master-the-different-types-of-joins-in-python/
.. _rename: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html
