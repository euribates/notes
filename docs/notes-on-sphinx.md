---
title: Notas sobre Sphinx
tags:
    - Python
    - Documentación
---

## Sobre Sphinx

**Sphinx** es una conunto de utilidades/libreria para crear documentación atractiva.

Algunas de sus características más interesantes son:

- Formatos de salida: Html, Latex/Pdf, ePub, Texinfo, manual pages o texto plano.

- Referencias cruzadas, enlaces automáticos a funciones, clases, glosario de términos, etc.

- Estructura jerárquica. Documentación en forma de árbol con enlaces automáticos a
  páginas hermas, padres e hijos.

- Índices automáticos

- Coloreado sintáctico del código, usando [Pygments](https://pygments.org/)

- Extensiones: Testeo  automárico de fragmentos de código, inclusion de las _docstrings_
  en el caso de Python, y muchas atras extensiones de terceros. La mayoría de las
  extensiones se pueden instalar con `pip`.


Sphinx usa por defecto [reStructuredText markup
language](https://docutils.sourceforge.io/rst.html), pero puede también trabajar con [MyST
markdown](https://jupyterbook.org/en/stable/content/myst.html) --que es un superconjunto
de Markdown--, usando una extensión (ver nota correspondiente).

## Empezar un projecto con Sphinx

Conviene crear un entorno virtual para eso, con la herramienta que prefieras. Aquí vamos a
usar `venv`, disponible en la librería estándar de Python desde la versión 3.3:

```python
python -m venv .venv
source .venv/bin/activate
python -m pip istall sphinx
```

Podemos verificar la instlación con:

```shell
sphinx-build --version
```

Agora podemos empezar escribiendo un fichero `README.rst` con la descripción del proyecto.
Por ejemplo:

```rest
Ejemplo de documento con Sphinx
===============================

Con **Sphinx** Podemos crear una documentación fat-tas-ti-bu-lo-sa.
```

El siguiente paso es crear el proyecto Sphinx en si. Usaremos el comando
`sphinx-quickstart <carpeta>`, por ejemplo:

```shell
sphinx-quickstart docs
```

Este _script_ nos preguntará una serie de datos:

- Si queremos carpetas separadas para la documentación y las salidas (Por defecto no, pero
  se recomienda que si)

- El nombre del proyecto

- El nombre del autor

- La versión, por ejemplo `0.1`

- El lenguaje del proyecto (Usar `es` para Español)

Después de contestar, nos habrá creado una estructura similar a esta:

```
├── docs
│   ├── build
│   ├── make.bat
│   ├── Makefile
│   └── source
│       ├── conf.py
│       ├── index.rst
│       ├── _static
│       └── _templates
└── README.rst
```

Cuyas carpetas y ficheros sirven para diferentes propósitos:

- `build` es la carpeta donde se generarán los productos finales producidos, sean
  estos ficheros _html_, _latex_, _epub_, etc.

- `make.bat` y `Makefile` son para ser usados con la herramienta `make`

- `source/conf.py` es el fichero de configuración del proyecto

- `source/index.rst` es el fichero inicial o raiz, a partir del cual se genera
  todo el árbol de documentación

Con este esquema inicial, ya podemos generar nuestra primera versión de la documentación:

```shell
sphinx-build -b html docs/source docs/build/html
```

Que debe producir una salida similar a:

```
Ejecutando Sphinx v6.1.3
cargando traducciones [es]... hecho
creando directorio de salida... hecho
compilando [mo]: los objetivos para 0 los archivos po que estan desactualizados
escribiendo salida... 
compilando [html]: los objetivos para 1 los archivos fuentes que estan desactualizados
actualizando ambiente: [nueva configuración] 1añadido, 0 cambiado, 0 removido
leyendo fuentes... [100%] index                                                                                  
buscando por archivos no actualizados... no encontrado
preparando ambiente... hecho
verificando consistencia... hecho
preparando documentos... hecho
escribiendo salida... [100%] index                                                                               
generando índices... genindex hecho
escribiendo páginas adicionales... search hecho
copiar archivos estáticos... hecho
copiando archivos extras... hecho
volcar el índice de búsqueda en Spanish (code: es)... hecho
volcar inventario de objetos... hecho
construir éxitoso.
```

Ahorapodemos abrir con nuestro navegador favorito las páginas en
`docs/build/html/index.html`. Deberia verse algo como:

![Primera versión de nuestra documentación](sphinx/first-impression.png)

El fichero `index.rst` ha sido creado automáticamente, podemos editarlo. Aquí podemos
ver el uso de algunas de las caraterísticas de ReEstructuredText:

```rest

.. lab-sphibx documentation master file, created by
   sphinx-quickstart on Fri Mar 17 11:43:17 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to lab-sphibx's documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```


- Una cabecera de sección usando `===` debajo de la línea

- Uso de la **directiva** `toctree` para crear el índice o tabla de contenidos.
  (

- Y una nota de aviso, en forma de una de las **directivas** disponibles.


    an inline external link,

    and a note admonition (one of the available directives)
autor del 
- Dos ejemplos de marcado: Énfasis fuerte (normálmente con negritas) usando `**`
  y énfasis normal (normalmente itálicas) con `*`. 


## Qué es una directiva

Las directivas son una forma muy potente de ampliar las posibilidades de ReEstructuredText.
El sistema define un conjunto de varias directivas predefinidas, y este conjunto puede ser
ampliado con directivas de terceras partes.

Las directivas pueden aceptar argumentos y/o tener opciones. y/o contenidos.
Un ejemplo de directiva es `.. toctree`, que se genera en la pagina de `index.rst` por
defecto al crear el proyectp. Todas las directivas se ejecutan escribiendo antes los dos
puntos (No el caracter `:`, sino dos veces el caracter `.`)

Cada directiva define los argumentos que acepta (Puede no aceptar ninguno). En caso de que
se definan estos argumentos, deben especificarse después del nombre de la directiva. Las
opciones vendrían en la o las líneas a continuación, en forma de "lista de campos" o cadenas
con la forma `<nombre>: <valor>`. Por ejemplo, `maxtree` es un ejemplo de opción para la
directiva `toctree`.

Después de las opciones, tiene que venir una línea en blanco y luego, opcionalmente, el
contenido. No todas las directivas tienen que aceptar un contenido, pero si este es el caso,
el contendo tiene que estar indentado en el mismo nivel que las opciones


Esta seria la forma general:

```
.. <directiva> [<opcion 1> <opcion 2>...]
    opcion1: valor1
    opcion2: valor 2
    ...
    <contenido>

## Cómo añadir contenido a la documentación.

Debemos especifica los ficheros a incluir como
parte del contenido de la directiva `tocfree`. El siguiente
ejemplo añade dos ficheros:

```
.. toctree::
   :maxdepth: 2

   usage/installation
   usage/quickstart
   ...
```

De esta forma `toctree` aprende no solo donde están los contenidos, sino el orden
en que deben ser presentados y la estructura jerárquica de los mismos.

## Como crear un glosario

Usaremos el rol


Markdown

Markdown is a lightweight markup language with a simplistic plain text formatting syntax. It exists in many syntactically different flavors. To support Markdown-based documentation, Sphinx can use MyST-Parser. MyST-Parser is a Docutils bridge to markdown-it-py, a Python package for parsing the CommonMark Markdown flavor.
Configuration

To configure your Sphinx project for Markdown support, proceed as follows:

    Install the Markdown parser MyST-Parser:

    pip install --upgrade myst-parser

    Add myst_parser to the list of configured extensions:

    extensions = ['myst_parser']

    Note

    MyST-Parser requires Sphinx 2.1 or newer.

    If you want to use Markdown files with extensions other than .md, adjust the source_suffix variable. The following example configures Sphinx to parse all files with the extensions .md and .txt as Markdown:

    source_suffix = {
        '.rst': 'restructuredtext',
        '.txt': 'markdown',
        '.md': 'markdown',
    }

    You can further configure MyST-Parser to allow custom syntax that standard CommonMark doesn’t support. Read more in the MyST-Parser documentation.


