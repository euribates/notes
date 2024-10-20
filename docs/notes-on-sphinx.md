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

## Qué es un rol

Un **rol** es un mecanismo que proporciona |RST| para poder ser extendido, igual
que las directivas. En el caso de rol, estaríamos trabajando a nivel de elemento
en línea. Normalmente se ejecutan como:

```
:rolename:`content`
```

Por ejemplo, para incluir un fragmento de texto en línea que queremos en formato
de código usaremos el rol `code`:

```
Si queremos incrementas la variable :code:`a`, haremos :code:`a = a + 1`.
```

Existen múltiples roles predefinidos ya en Sphinx, como `math` para incluir
expresiones matemáticas, `abbr` para abrebiaturas

## Qué es una directiva

Un **rol** es un mecanismo que proporciona |RST| para poder ser extendido, igual
que los roles. En el caso de la directiva, estaríamos trabajando a nivel de bloque.

Las directivas son la forma mas potente de ampliar las posibilidades de
ReEstructuredText. El sistema define un conjunto de varias directivas
predefinidas, y este conjunto puede ser ampliado con directivas de terceras
partes.

Las características principales de las directivas son:

 - Tiene un _nombre único_

 - Pueden (o no) aceptar _argumentos_ 

 - Tener (o no) _opciones_

 - Tener (o no) _contenidos_

Un ejemplo de directiva es `toctree`, que se genera en la pagina de
`index.rst` por defecto al crear el proyecto. Todas las directivas se ejecutan
escribiendo antes dos puntos (No el caracter `:`, sino dos veces el caracter
`.`), seguidos de dos veces el caracter _dos puntos_. Suena más confuso de lo
que es; si quieremos ejecutar `toctree`, escribimos:

```
.. toctree::
```

Cada directiva define los argumentos que acepta (Puede no aceptar ninguno). En
caso de que se definan estos argumentos, deben especificarse después del nombre
de la directiva. Las opciones vendrían en la o las líneas a continuación, en
forma de "lista de campos" o cadenas con la forma `:<nombre>: <valor>`. Por
ejemplo, `maxtree` es un ejemplo de opción para la directiva `toctree`.

Después de las opciones, tiene que venir una línea en blanco y luego,
opcionalmente, el contenido. No todas las directivas tienen que aceptar un
contenido, pero si este es el caso, el contenido **tiene que estar indentado en el
mismo nivel que las opciones**. Esta seria la forma general:

```
.. <directiva>:: [<argumento 1> <argumento 2>...]
    :opcion1: valor1
    :opcion2: valor 2
    
    <contenido>
```

## Cómo añadir contenido a la documentación.

Debemos especifica los ficheros a incluir como parte del contenido de la
directiva `tocfree`. El siguiente ejemplo añade dos ficheros:

```
.. toctree::
   :maxdepth: 2

   usage/installation
   usage/quickstart
   ...
```

De esta forma `toctree` aprende no solo donde están los contenidos, sino el
orden en que deben ser presentados y la estructura jerárquica de los mismos. No
es necesario normalmente especificar la extensión del archivo, se buscara el
ficheros con extensiones como `.rst` o `.md`.

## Como crear un glosario en Sphinx

Crearemos un fichero `glosario.rst`, por ejemplos. Lo incluimos en algun
`toctree` para que Sphinx lo integre en la documentación. Dentro de este fichero
usaremos la directiva `glossary`. El contenido de esta directiva debe ser una
lista de definiciones en formato ResetructuredText, como en el siguiente
ejemplo:

```
.. glossary::
   :sorted:

   Bulbasaur

      **Bulbasaur** es un pokémon de tipo planta y veneno introducido en la
      primera generación. Es uno de los Pokémon iniciales que pueden seleccionar
      los jugadores al comenzar su aventura en la región de Kanto

   Charizard

      **Charizard** es un Pokémon de tipo fuego/volador. Es la tercera y última
      etapa de Charmander. Es uno de los Pokémon más conocidos. Aparece por
      primera vez en Pokémon Red y Blue.

   ...
```
    
 

## Cómo usar Markdown en Sphinx

Para poder usar MarkDown, Sphinx utiliza una extensión de terceros llamada
[**MyST-Parser**](https://myst-parser.readthedocs.io/en/latest/). MyST-Parser es
un puente (_bridge_) hacia `markdown-it-py`, un paquete Python package para
parsear la variante de Markdown conocica como `CommonMark Markdown`. MyST-Parser
requiere Sphinx 2.1 o superior.

Para configurar un proyecto Sphinx para que pueda usar esta variante de
MarkDown, los pasos a seguir son:

- Instala el parser `MyST-Parser`:

    ```
    pip install --upgrade myst-parser
    ```

- Ańadelo a la lista de extensiones:

    ```python
    extensions = ['myst_parser']
    ```
   
Si se quiere usar ficheros Markdown pero con extensiones diferentes a `.md`,
debemos incluir esas extensiones en la variable `source_suffix`. El siguiente
ejemplo configura Sphinx para que procese como MarkDown los ficheros con
extensiones tanto `.md` como `.txt`:

```python
    source_suffix = {
        '.rst': 'restructuredtext',
        '.txt': 'markdown',
        '.md': 'markdown',
    }
```

Se puede configurar `MyST-Parser` para permitir sintaxis personalizada que en
principio CommonMark no soportaría. Hay más información en la documentación del
paquete.

## Cómo poner notas a pie de página con Sphinx

Para las notas a pie de página, hay que usar `[#]_` para marcar la ubicación de
la llamada a la nota, y luego, al final del documento, añadimos una directiva
`rubric`, como en en siguiente ejemplo:

```
    Porque patatín [#]_ ... y patatán  [#]_ ...

    .. rubric:: Notas

    .. [#] Texto de la primera nota.
    .. [#] Texto de la segunda nota.

```

## Ańadir enlaces en Sphinx

Se puede incluir enlaces a localizaciones dentro del mismo documento, a otras
localizaciones en otro documento, o a sitios web externos

### Enlaces a secciones dentro del mismo documento

Se puede enlazar a cualquier encabezado del documento usando el comand `:ref:`,
usando el propio texto de la cabecera como parámetro, como en el siguiente
ejemplo:

```
:ref:`Cross-References to Locations in the Same Document`
````

Para esto tenemos que tener habilitada la extensión
`sphinx.ext.autosectionlabel`.

Si no queremos usar las secciones, podemos enlazar a cualquier parte del
documentos usando una referencia manual:

```
    Bla bla ... Bla.

    .. _Quiero referenciar aquí

    Ble ble ... ble.

    Para incluir un enlace a la referencia usando  :ref:`Quiero referenciar aquí`
```

### Enlaces a páginas externas

Para enlazar a una URL externa, podemos usar esta sintaxis:

```
`Link text <link URL>`_
```

Por ejemplo:

`Python <http://python.org/>`_

También podemos separar en dos el texto del enlace y la definición de la URL destino:

```
Aprende e programar en `Python`_.

.. _Python: http://python.org/






