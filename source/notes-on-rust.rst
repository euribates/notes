Rust
========================================================================

.. tags:: rust,development,devops


Sobre Rust
-----------------------------------------------------------------------

Rust es un lenguaje de programación compilado, de propósito general y
multiparadigma que está siendo desarrollado por la `Fundación
Rust <https://foundation.rust-lang.org/>`__.

Soporta programación funcional pura, por procedimientos, imperativa y
orientada a objetos.

Rust es desarrollado de forma totalmente abierta y busca la opinión y
contribución de la comunidad. El diseño del lenguaje se ha ido
perfeccionando a través de las experiencias en el desarrollo del motor
de navegador Servo, y el propio compilador de Rust. Aunque es
desarrollado y patrocinado por Mozilla y Samsung, es un proyecto
comunitario. Gran parte de las contribuciones proceden de los miembros
de la comunidad.

En 2022, Rust se convirtió en el tercer lenguaje de programación usado
en el núcleo Linux, después de C y ensamblador.

Instalar el compilador de Rust y el resto de herramientas
-----------------------------------------------------------------------

Para instalar Rust, vamos a descargar una utilidad de línea de comandos
llamada ``rustup``, que nos permite gestionar las versiones de Rust y
herramientas vinculadas.

.. code:: shell

    curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh

También nos hace falta un *linker*, la forma más fácil en Linux es
instalar el compilador de C que viene con uno incorporado. Para ello:

.. code:: shell

    sudo apt install build-essential

Para verificar que Rust está instalado, podemos hacer:

.. code:: shell

    rustc --version

Una vez instalado, podemos actualizar a la última versión estable con:

.. code:: shell

    rustup update

Acceder a la documentación local de Rust
-----------------------------------------------------------------------

Al instalar Rust, se incluye tambiéñ una copia local de la
documentación, para que se pueda consultar incluso sin conexión a
Internet. Para acceder a ella:

.. code:: shell

    rustup doc

El sistema de tipos de Rust
-----------------------------------------------------------------------

El sistema de tipos soporta un mecanismo similar a las clases de tipos,
llamado *traits*, inspirados directamente por el lenguaje **Haskell**.
Esta es una facilidad para el polimorfismo que soporta distintos tipos
de argumentos (polimorfismo *ad-hoc*), lograda mediante la adición de
restricciones para escribir declaraciones de variables. Otras
características de Haskell, como el polimorfismo de diferente tipo
(*higher-kinded*), no están soportadas.

Rust cuenta con **inferencia de tipos**, para las variables declaradas
con la palabra clave ``let``. Tales variables no requieren ser
inicializadas con un valor asignado con el fin de determinar su tipo. En
tiempo de compilación produce un error si cualquier rama de código falla
al asignar un valor a la variable.

Las funciones pueden recibir parámetros genéricos pero deben ser
delimitados expresamente por los *traits*, no hay manera de dejar fuera
de declaraciones de tipo sin dejar de hacer uso de los métodos y
operadores de los parámetros.

Hola, Mundo en Rust
-----------------------------------------------------------------------

.. code:: rust

    fn main() {
        println!("¡Hola, mundo!");
    }

Estas líneas definen una función llamada ``main``. La función ``main``
es especial: Es siempre la primera función que se ejecuta en un programa
Rust. En este caso, definimos una función sin parámetros y que no
devuelve nada. Si hubieran parámetros, se listarían dentro de los
paréntesis.
