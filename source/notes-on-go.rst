Go Language
========================================================================

.. tags:: go, development

.. contents:: Relación de contenidos
    :depth: 3

Sobre Go (Golang)
------------------------------------------------------------------------

:index:`Go` es un lenguaje de programación de sistemas, de código
abierto, desarrollado inicialmente por Google. 

.. admonition:: 

   Aunque el nombre oficial del lenguaje es **Go**, también se le llama
   frecuentemente **Golang**. La razón de esto es que el dominio
   ``go.org`` no estaba disponible y optaron por ``golang.org``, aunque
   ahora mismo la página oficial es `go.dev`_. El uso de ``golang`` se
   sigue usando ampliamente, especialmente a la hora de usar motores de
   búsqueda, ya que `go` es una palabra demasiado común.


El lenguaje Go comenzó como un proyecto interno de Google que se hizo
público en 2009. `Robert Griesemer`_, `Ken Thompson`_ y `Rob Pike`_
diseñaron Go como un lenguaje para programadores profesionales que
desean crear software **confiable, robusto y eficiente**, fácil de
administrar.  Diseñaron Go pensando en la simplicidad, aunque esto
significara que no sería un lenguaje de programación para todos ni para
cualquier propósito.  La siguiente figura muestra los lenguajes de
programación que influyeron directa o indirectamente en Go. Por ejemplo,
la sintaxis de Go se parece a la de `C`_, mientras que el concepto de
paquete se inspira en `Modula`_.

.. graphviz::

   digraph foo {
      rankdir=LR;
      "Algol 60" -> "C";
      "Algol 60" -> Pascal;
      Pascal -> "Modula-2";
      "Modula-2" -> Oberon;
      Oberon -> "Go";
      "C" -> "Go";
   }


El resultado fue un lenguaje de programación con herramientas y
una biblioteca estándar. Además de su sintaxis y herramientas,
se obtiene una completa biblioteca estándar y un sistema de tipos que
intenta evitar errores comunes, como conversiones de tipo implícitas,
variables sin usar y paquetes sin usar. El compilador de Go detecta la
mayoría de estos errores y se niega a compilar hasta que se corrijan.
Además, el compilador de Go puede encontrar errores más difíciles de
detectar, como condiciones de carrera.


Ventajas de Go
------------------------------------------------------------------------

- Fácil de leer, sintaxis similar a la de `C`_.

- Soporta Unicode

- Tiene recolector automático de basura (*grabage recollector*), por lo que no hace falta
  gestionar la memoria de forma manual.

- Solo tiene 25 palabras reservadas

- Implementación de concurrencia nativa, usando *gorutinas*
  (*goroutines*) y canales (*channels*).

- Amplia librería estándar.

- Librerías de terceros, como `Cobra`_ o `viper`_.

- El código Go es muy predecible y está diseñado para redurir
  al mínimo los efectos paralelos

- Aunque soporta punteros, no permite aritmética con ellos (A menos que
  se use un paquete específico para ello, y que no se recomienda a no
  ser que sepas muy bien lo que estas haciendo).

- Aunque no es orientado a objetos, implementa el concepto de
  *interfaces*, con el que se pueden imitar varios conceptos de OOP
  como polimorfismo, encapsulación o composición (Pero no existe
  clases ni herencia).

- Soporte para variables genéricas.

Cómo usar la documtación y ayuda de Go (``go doc``)
------------------------------------------------------------------------

Go incluye una gran cantidad de herramientas que facilitan la vida del
programador. Dos de estas herramientas son el subcomando `go doc` y la
utilidad `godoc`, que permiten consultar la documentación de las
funciones y paquetes de Go sin necesidad de conexión a Internet.

El comando ``go doc`` se ejecuta como una aplicación de línea de
comandos normal que muestra su salida en la terminal. Es similar al
comando `man(1)` de UNIX, pero solo para funciones y paquetes de Go.
Por lo tanto, para obtener información sobre la función `Printf()` del
paquete `fmt`, ejecuta el siguiente comando:

.. code:: shell

    $ go doc fmt.Printf

Tambien se puede obtener información de todo el módulo `fmt``:

.. code:: shell

    $ go doc fmt

Para usar godoc:

.. code::

    $ godoc -http :8910

Y abrir un *browser* apuntando a <http://localhost:8910/>. Obviamente se
puede elegir otro puerto sin problema. Si no se especifica ningún
puerto, se usa el :math:`6060`.

Hola, Mundo en Go
------------------------------------------------------------------------

El siguiente código es el ejemplo del típico programa *hola, mundo* en
Go:

.. code:: go

    package main

    import ("fmt")

    func main() {
        fmt.Println("Hello, Word!")
        }

Si hemos guardado el fichero anterior como ``hola-mundo.go``, podemos
compilarlo y ejecutarlo con:

.. code:: shell

    $ go run hola-mundo.go

Veremos que la primera vez tarda un poco, porque tiene que compilar el
ejecutable, pero la siguiente ejecución es mucho más rápida.

Todos los programas de Go comienzan con una declaración de módulo o
paquete (*package*). En este caso, el nombre del paquete es ``main``,
que tiene un significado especial en Go: los programas Go autónomos
deben usar el paquete ``main``.

La palabra clave ``import`` permite incluir funcionalidades de paquetes
existentes. En nuestro caso, solo necesitamos algunas funcionalidades
del paquete ``fmt``, que pertenece a la biblioteca estándar de Go. Este
implementa funciones de entrada y salida formateadas, análogas a
``printf()`` y ``scanf()`` de `C`_.

El siguiente paso es la declaración de la función ``main()``.  Go
considera esta función como el punto de entrada de la aplicación. En
otras palabras, comienza la ejecución del programa con el código que se
encuentre en la función ``main()`` del paquete ``main``.

En resumen, hay **dos características** que hacen que ``hola-mundo.go``
sea un archivo fuente que puede generar un binario ejecutable: el nombre
del paquete, que debe ser ``main``, y la presencia de la función
``main()``.




.. _Cobra: https://cobra.dev/
.. _Viper: https://pkg.go.dev/github.com/spf13/viper
.. _Robert Griesemer: https://en.wikipedia.org/wiki/Robert_Griesemer
.. _Rob Pike: https://en.wikipedia.org/wiki/Rob_Pike
.. _Ken Thompson: https://en.wikipedia.org/wiki/Ken_Thompson
.. _C: https://en.wikipedia.org/wiki/C_(programming_language)
.. _Modula: https://en.wikipedia.org/wiki/Modula
.. _go.dev: https://go.dev/
