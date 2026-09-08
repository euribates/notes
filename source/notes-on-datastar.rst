Datastar
========================================================================

.. tags:: development, javascript, django

Qué es :index:`Datastar`
------------------------------------------------------------------------

**Datastar** es un *framework* javascript ligero. Permite construir desde
aplicaciones web sencillas a aplicaciones colaborativas en la web en
tiempo real. No impone ninguna restricción en la parte de *backend*.
Pesa unos 11 kB.

Fuente: `Data-star homepage`_


Como funciona Datastar
----------------------

Con Datastar, el *backend* es el que determina los cambios en el
*frontend* parcheando (Añadiendo, modificando o borrando) los elementos
HTML en el DOM. Las modificaciones se realizan usando una estrategia de
*morphing* por defecto, que se asegura de solo modificar las partes del
DOM que necesitan cambios, manteniendo el estado y favoreciendo el
rendimiento.

El núcleo de Datastar son los atributos ``data-*``, de ahí el nombre. De
esta forma podemos añadir comportamiento reactivo e interacciones con el
*backend* de forma declarativa.

Datastar proporciona acciones (``actions``) para enviar peticiones al
*backend*. Por ejempo, la llamada a ``@get()`` realiza una solicitud de
tipo GET a la URL indicada:

.. code:: html

    <button data-on-click="@get('/endpoint')">
        Open the pod bay doors, HAL.
    </button>

    <div id="hal"></div>


En el ejemplo anterior, si la respuesta de ``/endpoint`` devuelve un
contenido de tipo ``text/html``, los elementos de mayor nivel es
transformados en el árbol DOM ya existente para que que conviertan en
los elementos retornados, basándose en los identificadores de los
elementos.

Lo importante aquí es darse cuenta de que **es el backend el que
determina** los elementos que deben ser actualizados. En otros
*frameworks*, lo más normal es que esta decisión se tome en el cliente.

.. code:: html

    <div id="hal"> I’m sorry, Dave. I’m afraid I can’t do that.  </div>

Esto elementos se suelen llamar *Patch Elements*. Va en plural porque se
puede transformar múltiples elementos en el DOM con una sola llamada,
(aunque obviamente nada impide cambiar solo uno).

En el ejemplo anterior, el DOM debe contener un elemento con un ID igual
a ``hal`` para que el parcheo funcione. Hay otras estrategias de
parcheo, pero esta es la más simple y la más usada en la mayoría de
escenarios.

Si la respuesta tiene con ``contet-type`` de tipo ``text/event-stream``,
podemos hacer que el contenido conste de eventos. El siguiente ejemplo
replica el anterior, pero usando eventos:

.. code:: html

    event: datastar-patch-elements
    data: elements <div id="hal">
    data: elements I’m sorry, Dave. I’m afraid I can’t do that.
    data: elements </div>

Como podemos enviar tanto eventos como queramos, y además se mantiene
una conexión viva, podemos extender el ejemplo anterior para que se
muestre la respuesta de `HAL 9000`_ y luego, después de unos cuantos
segundos, se restablezca el texto inicial:

.. code:: html

    event: datastar-patch-elements
    data: elements <div id="hal">
    data: elements I’m sorry, Dave. I’m afraid I can’t do that.
    data: elements </div>

    event: datastar-patch-elements
    data: elements <div id="hal">
    data: elements Waiting for an order...
    data: elements </div> ```

En el servidor, haríamos:

.. code:: python

    from datastar_py import ServerSentEventGenerator as SSE
    from datastar_py.sanic import datastar_response
 
    @app.get('/open-the-bay-doors')
    @datastar_response
    async def open_doors(request): 
        yield SSE.patch_elements(
            '<div id="hal">'
            'I’m sorry, Dave. I’m afraid I can’t do that.'
            '</div>'
            )
        await asyncio.sleep(1)
        yield SSE.patch_elements('<div id="hal">Waiting for an order...</div>')


Señales
------------------------------------------------------------------------

Datastar usa señales para gestionar el estado en el *frontend*. Se puede
pensar en las señales como **variables reactivas** cuyos valores se
propagan de forma automática a y desde las expresiones que las usan. Las
señales se identifican con el prefijo ``$``.

Por defecto, todas las señales, excepto las locales (aquellas cuyos
nombres comienzan con un guion bajo) se envían con cada solicitud al
*backend*. Al realizar, un ``GET`` las señales se envían como parámetros
de consulta de Datastar; en el resto de los casos, se envían dentro del
cuerpo en JSON.

Enviar todas las señales en cada solicitud sirve para que el *backend*
tenga acceso completo al estado del *frontend*. Esto es intencionado. No
se recomienda enviar señales parciales, pero si es necesario, se puede
usar la opción ``filterSignals`` para filtrar las señales enviadas
al *backend*.

Es normal crear señales de forma implícita cuando se usa ``data-bind`` o
``data-computed``, porque cuando se usa una señal sin haberla definido
se crea automáticamente, con un valor inicial de cadena de texto vacía.
Pero podemos crear las señales de forma explícita usando el atributo
``data-signals``, lo que nos permite también definir un valor inicial:

.. code:: html

   <div data-signals:foo-bar="1"></div>

Las señales pueden anidarse usando como separador el punto:

.. code:: html

   <div data-signals:form.baz="2"></div>

Como en el caso de ``data-bind``, los nombres de señales que usan
guiones son transformados automáticamente a la convención de nombres
:term:`Camel case`, es decir, se borra el guión y se pasa a mayúsculas
la letra que sigue al guión. Por ejemplo, ``foo-bar`` pasa a ser
``fooBar```.

.. code:: html

   <div data-signals:foo-bar="1"
        data-text="$fooBar"></div>

Se pueden definir varias señales a la vez, usando un diccionario de parejas
clave/valor, donde la clave es el nombre de la señal y el valor es el
valor inicial de la misma. Los valores anidados se pueden indicar con
usando diccionarios como valores del diccionario de nivel superior:

.. code:: html

    <div data-signals="{fooBar: 1, form: {baz: 2}}"></div>


Atributos de Datastar
------------------------------------------------------------------------

Los atributos ``data-*`` en DataStar tiene las siguientes
caracterísiticas:

- Son evaluados en el orden en que aparecen en el DOM.
- Tiene ciertas reglas especiales en lo que respecta a mayúsculas y
  minúsculas.
- Pueden ser renombrados (*aliases*) para evitar conflictos con otras
  librerías.
- Pueden contener expresiones Datastar.
- Tiene gestión de errores en tiempo de ejecución.

``data-attr``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Asigna a cualquier atributo de una etiqueta HTML el valor de una
expresión, y los mantiene en sincronía.

.. code:: html

   <div data-attr:title="$foo"></div>

También se puede usar para múltiples atributos, usando un conjunto de
duplas clave-valor,, donde las claves representan los nombres de los
atributos y los valores representan expresiones:

.. code:: html

   <div data-attr="{title: $foo, disabled: $bar}"><

``data-text``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vincula el contenido textual de un elemento con una expresión.

.. code:: html

   <div data-text="$foo"></div>

``data-on``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vincula un evento que puede suceder a un elemento con una expresión
de código, que se ejecutará cada vez que se produzca el evento.

.. code:: html

   <button data-on:click="$foo = ''">Reset</button>

Dentro de la expresión podemos usar la variable predefinida ``evt``, que
hace referencia al evento javascript en cuestión, con todos sus valores.

.. code:: html

   <div data-on:my-event="$foo = evt.detail"></div>

Podemos usar tanto los eventos estándar de Javascript como eventos
personalizados. El código vinculado a ``data-on:submit`` en principio
cancela el comportamiento por defecto de enviar los datos del
formulario.

Existen varios modificadores que nos permiten cambiar el comportamiento
ante los eventos. Algunos de estos modificadores tienen parámetros:

- ``__once``: Solo se dispara la expresión la primera vez que sucede el
  evento.

- ``__pasive``: No llama a ``preventDefault``, que es el comportamiento
  por defecto

- ``__delay``: Retrasa la llamada a la expresión. Ejemplos:

  * ``.500ms``: Retrasa la llamada durante 500 milisegundos. Acepta
    cualquier numero entero.

  * ``.2s``: Retrasa la llamada durante dos segundos. Acepta
    cualquier numero entero.

- ``__case``: transforma el  nombre del evento según la convención
  indicada de mayúsculas/minúsculas:

    * ``camel`` : *Camel case*: ``myEvent``
    * ``kebab`` : *Kebab case*: ``my-event`` (El valor por defecto)
    * ``snake`` : *Snake case*: ``my_event``
    * ``pascal`` : *Pascal case*: ``MyEvent``

``data-class``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Añade o elimina una clase a un elemento según una expresión.

.. code:: html

   <div data-class:font-bold="$foo == 'strong'"></div>

Si la expresión se evalúa como verdadera, se añade la clase `font-bold`
al elemento; de lo contrario, se elimina. El atributo `data-class`
también se puede usar para añadir o eliminar varias clases a/de un 
elemento mediante pares clave-valor, donde las claves representan
nombres de clases y los valores representan expresiones.

.. code:: html

   <div data-class="{success: $foo != '', 'font-bold': $foo == 'strong'}"></div>

``data-computed``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Crea una señal que se calcula en función de una expresión. La señal
calculada es de solo lectura y su valor se actualiza automáticamente
cuando se actualiza alguna de las señales de la expresión.


.. code:: html

   <div data-computed:foo="$bar + $baz"></div>

Las señales calculadas son útiles para memorizar expresiones que
contienen otras señales. Sus valores se pueden usar en otras expresiones.

.. code::

   <div data-computed:foo="$bar + $baz"></div>
   <div data-text="$foo"></div>

.. warning::

   Las expresiones de señales calculadas no deben usarse para realizar
   acciones (cambiar otras señales, acciones, funciones de JavaScript,
   etc.). Si necesita realizar una acción en respuesta a un cambio de
   señal, use el atributo ``data-effect``.

El atributo ``data-computed`` también se puede usar para crear
señales calculadas mediante pares clave-valor, donde las claves
representan nombres de señales y los valores son funciones
invocables (generalmente funciones flecha) que devuelven un valor
reactivo.

.. code:: html

   <div data-computed="{foo: () => $bar + $baz}"></div>

.. _data-effect
``data-effect``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ejecuta una expresión cuando se carga la página y cuando cualquiera de
las señales implicadas en la expresión se vea modificada. Esto sirve
para ejecutar efectos secundarios, como por ejemplo actualizar otra
señal, ejecutar una solicitud o manipular el DOM.

.. code:: html

   <div data-effect="$foo = $bar + $baz"></div>

``data-ignore``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Datastar recorre todo el DOM y afecta a cada elemento que encuentra. Es
posible indicarle a Datastar que ignore un elemento y sus descendientes
añadiéndole el atributo ``data-ignore``. Esto puede ser útil para evitar
conflictos de nombres con bibliotecas de terceros o cuando no se puede
escapar la entrada del usuario.

.. code:: html

   <div data-ignore data-show-thirdpartylib="">
      <div>
      Datastar no procesará este elemento.
      </div>
   </div>

``data-init``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ejecuta una expresión cuando el atributo es inicializado. Esto ocurre
cuando se carga la página, cuando el elemento es pegado en el DOM, y en
cualquier momento en que el atributo se vea modificado (Por una acción
del *backend* o de cualquier otra forma).

.. code::

   <div data-init="$count = 1"></div>

Modificadores: ``__delay`` y ``_viewTransition``.


``data-indicator``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Crea una señal y establece su valor en verdadero mientras se ejecuta una
solicitud de obtención de datos; cuando la solicitud termina, lo 
establece en falso. La señal se puede usar para mostrar un indicador de
carga.

.. code:: html

   <button data-on:click="@get('/endpoint')"
       data-indicator:fetching></button>

Esto puede ser útil para mostrar un indicador de carga, deshabilitar un
botón, etc.

.. code:: html

   <button data-on:click="@get('/endpoint')"
       data-indicator:fetching
       data-attr:disabled="$fetching"
       ></button>
   <div data-show="$fetching">Cargando...</div>

El nombre de la señal se puede especificar en la clave (como se muestra
en el ejemplo anterior) o en el valor (como se muestra en el siguiente).
Esto puede ser útil dependiendo del lenguaje de plantillas que se
utilice.

.. code::

   <button data-indicator="fetching"></button>

Al usar `data-indicator` con una solicitud `fetch` iniciada en un
atributo `data-init`, asegúrese de que la señal del indicador se
crea antes de que se inicialice la solicitud.

.. code:: html

   <div data-indicator:fetching data-init="@get('/endpoint')"></div>


``data-bind``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Crea una señal (*signal*), a no ser que ya existiera previamente, y
establece un doble vínculo entre la señal y el valor del elemento. Esto
significa que el valor del elemento se actualiza cada vez que la señal
cambie, y que la señal es modificada cada vez que el valor del elemento
cambie.

Se puede poner en cualquier elemento HTML que admita entrada, como
elementos ``input``, ``textarea`` o ``select``, por ejemplo. Se añaden
manejadores de eventos para gestionar todos los cambios.

.. code:: html

    <input data-bind:foo />

El nombre de la señal se puede especificar en la clave, como en el
ejemplo anterior, o en el valor, como en el ejemplo siguiente. Esto
puede ser muy útil dependiendo del sistema de plantillas que estés
usando.

.. code:: html

    <input data-bind="foo" />

El valor inicial de la señal es el del elemento, a menos que la señal
hubiera sido definida previamente. Por ejemplo, en el siguiente ejemplo,
el valor de ``$foo`` sería ``"bar"``:

.. code:: html

    <input data-bind:foo value="bar" />

Pero en el siguiente, ``$foo`` hereda el valor de ``"baz"``, porque
hemos predefinido la señal:

.. code:: html

    <div data-signals:foo="baz">
        <input data-bind:foo value="bar" />
    </div>

Acciones posibles en Datastar
------------------------------------------------------------------------

Datastar proporciona **acciones** (funciones auxiliares) que se pueden
usar en expresiones de Datastar.

.. note::

   El prefijo ``@`` indica las acciones que se pueden usar de forma
   segura en expresiones. Esta es una medida de seguridad que impide
   la ejecución de código JavaScript arbitrario en el navegador. 
   Datastar utiliza constructores ``Function()`` para crear y ejecutar
   estas acciones en un entorno aislado, seguro y controlado.


peek
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Signatura: ``@peek(callable: () => any)``

Permite acceder a las señales sin suscribirse a ellas.

.. code:: html

    <div data-text="$foo + @peek(() => $bar)"></div>

En el ejemplo previo, la expresión dentro del atributo ``data-text`` sera
re-evaluado cada vez que ``$foo`` cambie, pero no lo será
cuando cambie el valor de ``$bar``, porque se ha obtenido el dato
dentro de la acción ``peek``.

get
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Signatura: ``@get(uri: string, options={ })``

Envía una petición ``GET`` al backend. La URI puede ser cualquier *end
point* válido y la respuesta debe ser cero o más eventos SSE. Por
defecto, la petición se realiza incluyendo una cabecera
``Datastar-Request: true``, y un json de la forma ``{datastar: *}`` que
contendrá todas las señales existentes, excepto aquellas cuyo nombre
empiece por un subrayado (``_``). También se puede usar la opción
``filterSignals``, que nos permite incluir o excluir determinadas
señales usando expresiones regulares.

.. note:: 

   Cuando se realiza una petición de tipo GET, las señales se envía como
   parámetros en línea, en otros casos, se pasan en el body. Por
   defecto, en formato JSON.

post
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

put
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

patch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

delete
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. _HAL9000: https://es.wikipedia.org/wiki/HAL_9000
.. _Data-star homepage: https://data-star.dev/
