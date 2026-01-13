PyTest
========================================================================


Como ejecutar pytest y que incluya el directorio actual en el *path*
-----------------------------------------------------------------------

Si ejecutamos directamente el comando ``pytest``, este solo considera el
contenido normal del path, que normalmente no incliye el directorio
actual. La forma más fácil de solucionarlo es ejecutarlo llamando
primero al interprete de python. Como el comportamiento por defecto del
interprete es incluir la carpeta actual en el path, en la fase de `test
recovery <https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#test-discovery>`__
encontrara los módulos o paquetes que esten en el directorio actual.

Por ejemplo, si tenemos las siguiente estructura en el directorio
actual:

.. code::

    .
    ├── a
    │   ├── alfa.py
    │   ├── __init__.py
    ├── b
    │   ├── beta.py
    │   ├── __init__.py
    └── tests
    ├── a
    │   └── test_alfa.py
    └── b
    └── test_beta.py

Si ejecutamos ``pytest`` directamente, si el directorio actual no está
incluido en el ``path``, obtendremos errores de tipo ``ImportError``; se
queja de que no puede encontrar los directorio ``a`` o ``b``:

.. code::

    collecting ...
    ―――――――――――――――――――――――――――――――― ERROR collecting tests/a/test_alfa.py ―――――――――――――――――――――――――――――――――
    ImportError while importing test module '/home/jileon/labos/lab-pytest/tests/a/test_alfa.py'.
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    tests/a/test_alfa.py:3: in <module>
    from a import alfa
    E   ImportError: No module named a

    ―――――――――――――――――――――――――――――――― ERROR collecting tests/b/test_beta.py ―――――――――――――――――――――――――――――――――
    ImportError while importing test module '/home/jileon/labos/lab-pytest/tests/b/test_beta.py'.
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    tests/b/test_beta.py:3: in <module>
    from b import beta
    E   ImportError: No module named b

Sin embargo, si lo ejecutamos a través del intérprete, como el
directorio actual (``.``) se incorpora al ``path`` por defecto, no tiene
ningún problema a la hora de encontrar los módulos ``a`` y ``b``:

.. code:: shell

    collecting ...
    tests/a/test_alfa.py ✓                           50% █████
    tests/b/test_beta.py ✓                          100% ██████████


How to get the putput of the test even if the test doesn’t fail
-----------------------------------------------------------------------

pytest captures the stdout from individual tests and displays them only
on certain conditions, along with the summary of the tests it prints by
default. Extra summary info can be shown using the ``-r`` option:

.. code:: shell

    pytest -rP

shows the captured output of passed tests.

.. code:: shell

    pytest -rx

shows the captured output of failed tests (default behaviour).

The formatting of the output is prettier with ``-r`` than with ``-s``.

Fuentes: `How can I see normal print output created during pytest run <https://stackoverflow.com/questions/14405063/how-can-i-see-normal-print-output-created-during-pytest-run?rq=1>`_
