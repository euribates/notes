PyPi (*Python Package Index*)
========================================================================

Notes on Pacaking and distributing projects in Pipy

How to include command line scripts
-----------------------------------------------------------------------

Although setup() supports a ``scripts`` keyword for pointing to pre-made
scripts to install, the recommended approach to achieve cross-platform
compatibility is to use ``entry points``:

.. code::

    entry_points

    entry_points={
        ...
    },

Use this keyword to specify any plugins that your project provides for
any named entry points that may be defined by your project or others
that you depend on.

The most commonly used entry point is **console scripts**:

.. code::

    console_scripts

    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },

Use ``console_script`` entry points to register your script interfaces.

You can then let the toolchain handle the work of turning these
interfaces into actual scripts. The scripts will be generated during the
install of your distribution.

Working in development mode
-----------------------------------------------------------------------

Although not required, it’s common to locally install your project in
“editable” or “develop” mode while you’re working on it. This allows your
project to be both installed and editable in project form.

Assuming you’re in the root of your project directory, then run:

.. code:: shell

    python -m pip install -e .

Although somewhat cryptic, ``-e`` is short for ``--editable``, and ``.``
refers to the current working directory, so together, it means to install
the current directory (i.e. your project) in editable mode. This will also
install any dependencies declared with ``install_requires`` and any
scripts declared with ``console_scripts``. Dependencies will be installed
in the usual, non-editable mode.
