---
title: Notas sobre patrones
---

## Qué son los patrones de Diseño (_Design Patterns_)

Una definición sencilla podría ser:

> Un patrón de diseño es un **modelo de solución** para un **determinado
> problema** de diseño recurrente o habitual. El patrón describe el problema,
> le da un nombre, y sugiere una aproximación general a como resolverlo.

El concepto no está limitado al desarrollo de software; se puede aplicar a
cualquier campo donde se puedan encontrar problemas recurrentes. De hecho los
primeros patrones de diseño surgen en la arquitectura, producto del arquitecto
Christopher Alexander, en el libro _The Timeless Way of Building_ y
desarrollados posteriormente, junto con otros autores, en _A Pattern Language_.

En sus palabras, cada patrón "__describe un problema que ocurre infinidad de
veces en nuestro entorno, así como la solución al mismo, de tal modo que
podemos utilizar esta solución un millón de veces más adelante sin tener que
volver a pensarla otra vez.__"

## El patrón Command

El patrón **Command** es un patrón de diseño que **encapsula una petición** en
un **objeto inmutable**.

La idea principal es usar un objeto para encapsular toda la información
necesaria, y que permita ejecutar una acción en un momento posterior. La
información que almacena suele incluir, entre otras cosas:

- Un nombre

- Objeto o instancia al que pertenece el método

- Parámetros a incluir en la invocación del método

Por ejemplo, consideremos el caso de un software de instalación de tipo
_wizard_, en el que, a través de una serie de fases o pantallas se van
capturando todas las preferencias del usuario. El usuario puede avanzar o
retroceder a gusto por las distintas fases, cambiando sus decisiones en
cualquier momento. Solo cuando se llega al final y el usuario da su aprobación,
se ejecutan todos los pasos que conducen a la instalación del programa.

Esto se puede resolver muy bien usando este patrón. Una posible solución podría
ser crear al principio de la ejecución del instalador un objeto *Command* que
almacene toda la información relativa a las preferencias del usuario. Las
preferencias se van guardando y actualizando en este objeto. Cuando el usuario
finalmente pulse "Instalar" el programa simplemente se invoca el método
`execute` del objeto, que realiza la instalación acorde a las preferencias que
tiene almacenadas.  Hemos encapsulado toda la información necesaria para
realiza una acción dentro de un objeto **Command**, que puede ser ejecutado
posteriormente.

Otro ejemplo podría ser un _spooler_ de impresión. El _spooler_ puede
implementarse con un objeto `Command` que almacena la información pertinente,
como el tamaño de la página (A4, por ejemplo) si debe imprimirse apaisada u
horizontal, tipo de papel, etc. Una vez que el usuario manda a imprimir un
documento, cuando el _spooler_ quiera imprimirlo solo tiene que llamar al
método `execute()` del objeto *Command* y el documento se imprime con las
preferencias predefinidas.

### Ventajas y desventajas del patrón Command

Entre las ventajas de este patrón se pueden destacar las siguientes:

- Una de sus grandes ventajas es que permite determinar cuando se ejecuta,
  puede ser ahora mismo o en un momento posterior, esto es, permite **diferir
  en el tiempo** la ejecución.

- Otra gran virtud es que **desacopla** a la entidad que emite el evento de la
  entidad que lo ejecuta. Esto permite sistemas más flexibles y extensibles.

- Es fácil componer una secuencia de objetos **Comands** y tratarlos como a
  cualquier otra estructura de datos, por ejemplo, ponerlos en una cola.

- Es muy fácil añadir una nueva orden o **Command** al sistema sin afectar al
  código preexistente.

- Se puede implementar fácilmente un sistema de **rollback** o de deshacer
  (**undo**). Solo hay que almacenar en alguna parte los comandos ejecutados y
  obligar a las clases **Command** a implementar, además del método ``execute``,
  un método ``undo``, para deshacer lo que se haya hecho en el comando ``execute``
  (No siempre se podrá hacer esto, especialmente si trabajamos con sistemas
  externos)

Las desventajas son:

- Puede incrementar significativamente el número de clases y objetos que deben
  trabajar juntos para realizar una acción.

- Cada comando individual es una clase, que incremente la complejidad y
  dificulta la implementación y el mantenimiento.
