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

## El patrón Monada (_Monad_)

El patrón **Mónada** o **_Monad_** es un patrón de diseño
habitual en los lenguajes de programación funcionales
que nos permite combinar varios cálculos u funciones un una única expresión,
manteniendo a la vez una adecuada gestión de errores y [efectos
secundarios](https://es.wikipedia.org/wiki/Efecto_secundario_(inform%C3%A1tica)).

Para poder encadenarse, cada función debe, en teoría, devolver una nueva mónada
que puede ser usada como una entrada para la siguiente función.

### Typos de mónadas

Se han definido diferentes tipos de mónadas, que son de uso común para
representar diferentes tipos de cálculos o procesos. Algunos ejemplos son:

- **`Maybe Monad`**: Representa una computación que puede, o no, devolver un
valor. Se usa para gestionar condiciones de error o valores opcionales.

- **`State Monad`**: Representa una computación que mantiene en estado interno, que se
pasa de función a función. Se usa para modelar simulaciones y otros procesos
que requieren tener en cuenta los cambios durante el tiempo.

- **`Reader Monad`**: Representa una computación que tiene acceso a un entorno
  o configuración compartida. Puede ser útil para parametrizar procesos
  y hacerlos más reutilizables.

- **`Writer Monad`**: Representa una computación, cálculo o proceso que genera una
salida o que tiene un efecto secundario. Se utiliza para hacer _logging_,
_debug_ y otros tipos de procesos de diagnóstico.

- **`IO Monad`**:  Representa una computación, cálculo o proceso que realiza
operaciones de entrada/salida, o otros tipo de efectos secundarios. Esto es
útil para interacturar con sistemas externos, como bases de datos o servicios
web.

Cada mónada define su propio conjunto de operaciones que defines como las
operaciones a efectuar pueden encadenarse juntas y como se pueden
transformar o combinar los valores. En cualquier caso, todas las mónadas
comparten la propiedad de ser **componibles** y **modulares**, lo que las
convierte en herramientas muy potentes para construir cálculos y procesos
complejos en un estilo de programación funcional.

Fuentes: 

- [Mastering Monad Design Patterns: Simplify Your Python Code and Boost Efficiency - DEV Community](https://dev.to/hamzzak/mastering-monad-design-patterns-simplify-your-python-code-and-boost-efficiency-kal)

- [ArjanCodes | Python Functors and Monads: A Practical Guide](https://arjancodes.com/blog/python-functors-and-monads/)

- [What the Heck Are Monads?! - YouTube](https://www.youtube.com/watch?v=Q0aVbqim5pE)
## Cómo funciona la mónada `Maybe`

Podemos implementar la mónada `Mayde` en Python usando clases y la sobrecarga de operadores.
El siguiente código es un ejemplo de una implementación de `Maybe`, que recordemos que
representa una computación que puede, o no, retornar un valor:

```python
class Maybe:

    def __init__(self, value):
        self._value = value

    def bind(self, func):
        if self._value is None:
            return Maybe(None)
        else:
            return Maybe(func(self._value))

    def orElse(self, default):
        if self._value is None:
            return Maybe(default)
        else:
            return self

    def unwrap(self):
        return self._value

    def __or__(self, other):
        return Maybe(self._value or other._value)

    def __str__(self):
        if self._value is None:
            return 'Nothing'
        else:
            return f'Just {self._value!r}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Maybe):
            return self._value == other._value    
        return False

    def __ne__(self, other):
        return not (self == other)

    def __bool__(self):
        return self._value is not None
```

Vaamos un ejemplo de uso:

```python

def add_one(x):
    return x + 1

def double(x):
    return x * 2

result = Maybe(3).bind(add_one).bind(double)
print(result)  # Just 8

result = Maybe(None).bind(add_one).bind(double)
print(result)  # Nothing

result = Maybe(None).bind(add_one).bind(double).orElse(10)
print(result)  # Just 10

result = Maybe(None) | Maybe(1)
print(result) # Just 1
```

Obsérvese que las funciones que realizan la computación, `add_one`, `double`,
funcionan **igual de bien con números que con mónadas**. Pero cuando usamos
mónadas, obtenemos computaciones compuestas que pueden manejar condiciones
de error y efectos secundarios.

El método `bind` acepta una función como entrada y devuelve una nueva
instancia de `Meybe`, que representa el resultado de aplicar la función 
al valor original, si existe. El operador `|`se puede usar para combinar
dos instancias de `Maybe`, devolviendo la primera si esta contiene un valor, y la
segunda en caso contrario.

Nótese que este patrón no es de uso frecuente en Python, ya que está normalmente más
asociado a los funcionales funcionales puros, pero puede ser útil en el caso de
tener que encadenar operaciones de una forma modular y reutilizable.

## La mónada `State`

La monada **`State`** nos permite encapsular un proceso con estados de una forma
puramente funcional. Las funcionas aceptan una variable de estado inicial y devuelven
una nueva variable de estado y un resultado. El estado se representa
generalmente con una estructura de datos, y la función realiza operaciones que
actualizan el estado segón lo necesite. Veamos una implementación en Python:

La siguiente implementacíon utiliza las mónadas de estaod para realizr una
operación que cuenta el número de veces que una función es invocada.

```python
class State:

    def __init__(self, state):
        self.state = state

    def __call__(self, value):
        return (self.state[1], State((self.state[0] + 1, value)))

# create a stateful computation that counts the number of times it is called
counter = State((0, 0))

# call the computation multiple times and print the current count
for i in range(5):
    result, counter = counter(i)
    print(f"Computation result: {result}, count: {counter.state[0]}") 

#Computation result: 0, count: 1
#Computation result: 0, count: 2
#Computation result: 1, count: 3
#Computation result: 2, count: 4
#Computation result: 3, count: 5
```

Las ventajas de usar esta mónada en Python es incluir la capacidad de escribir
funciones puras que encapsulan cálculos que implican estados, lo que clarifica y
hace más mantenible el código. Como hemos separado el cálculo y modificaciones
del estado del resto del código, podemos tener funciones más modulares y
_testeables_, que también son, por ello, más fáciles de comprender.


