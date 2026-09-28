Javascript
========================================================================

.. tags:: javascript,html,web,development

.. contents:: Relación de contenidos
    :depth: 3


Obtener la posición del cursor en un control de tipo ``TextArea``
------------------------------------------------------------------------

Podemos usar la propiedad ``selectionStart`` del control. Este propiedad
nos informa de la primera posición del texto seleccionado, pero si no
hay texto seleccionado, informa de la posición actual del cursor.

Programación asíncrona con Javascript
------------------------------------------------------------------------

La programación asíncrona es una técnica que permite a su programa iniciar
una tarea potencialmente de larga duración y aún así poder responder a
otros eventos mientras esa tarea se ejecuta, en lugar de tener que esperar
hasta que esa tarea haya terminado. Una vez que esa tarea ha terminado, su
programa se presenta con el resultado.

Muchas funciones proporcionadas por los navegadores, algunas muy
interesantes, pueden llevar mucho tiempo y, por lo tanto, es conveniente
ejecutarlas de forma asíncrona:

- Realizar solicitudes HTTP usando ``fetch()``

- Acceso a la cámara o micrófono de un usuario con ``getUserMedia()``

- Pedir a un usuario que seleccione los archivos usando
  ``showOpenFilePicker()``

En principio, un programa JavaScript es *single-thread*, es decir, que
solo tiene un hilo de ejecución, por lo que si se realiza una operación
que lleva mucho tiempo, el programa no puede seguir ejecutándose hasta
que esta termina.

Una forma de resolver esto es mediante **funciones asíncronas**:

- Se Llama a una función que realiza una tarea potencialmente larga.

- La función empieza la tarea, pero retorna inmediatamente. Esto permite
  que la ejecución continúe (Aunque la tarea potencialmente larga no ha
  terminado, quizá ni siquiera ha empezado).

- La función ahora realiza la tarea sin bloquear el hilo principal, por
  ejemplo empezando un nuevo *thread*.

- Cuando la tarea ha terminado, se notifica el resultado.

La descripción que acabamos de ver de funciones asíncronas puede
recordar a los manejadores de eventos. De hecho, los manejadores de
eventos son realmente una forma de programación asíncrona: proporcionas
una función (el manejador de eventos) que se llamará, no de inmediato,
sino siempre que ocurra el evento. Si el evento fuera «la operación
asíncrona se ha completad», entonces se podría usar dicho evento para
notificar a la persona que llama sobre el resultado de una llamada de
función asíncrona.

Algunas API asíncronas tempranas utilizaron eventos de esta manera. La
API ``XMLHttpRequest`` permite realizar solicitudes HTTP a un servidor
remoto con JavaScript. Dado que esto puede llevar mucho tiempo, es una
API asíncrona, y se le notifica sobre el progreso y la eventual
finalización de una llamada *callback*.

*Callbacks*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un manejador de eventos es un tipo particular de función de
**callback**. Un *callback* es una función que se pasa como parámetro a
otra función, con la expectativa de que se llame en el momento adecuado.
Como acabamos de ver, las funciones *callback* solían ser
la principal forma de implementar funciones asíncronas en JavaScript.

Sin embargo, este código puede resultar difícil de entender cuando la
propia función de devolución de llamada debe llamar a funciones que
aceptan una función de devolución de llamada. Esta es una situación
común si se necesita realizar alguna operación que se descompone en una
serie de funciones asíncronas. Por ejemplo, considere lo siguiente:

Supongamos que tenemos que realizar un proceso que implica tres pasos,
donde cada uno de ellas depende de la anterior. Como código síncrono,
esto no representa ningún problema, pero con funciones asíncronas es más
complicado.

.. code:: js

   function doStep1(init, callback) {
     const result = init + 1;
     callback(result);
   }
   
   function doStep2(init, callback) {
     const result = init + 2;
     callback(result);
   }
   
   function doStep3(init, callback) {
     const result = init + 3;
     callback(result);
   }
   
   function doOperation() {
     doStep1(0, (result1) => {
       doStep2(result1, (result2) => {
         doStep3(result2, (result3) => {
           console.log(`result: ${result3}`);
         });
       });
     });
   }
   
   doOperation();

Debido a este patrón de *callbacks* dentro de *callbacks*, la función
``doOperation()`` tiene un alto nivel de anidado, lo que la hace difícil
de entender y de depurar. Este se denomina a veces «Infierno de
callbacks» (*callback hell*) o «Pirámide de la perdición» (*Pyramid of
Doom*), por la apariencia del código indentado.

Con este tipo de código, se hace muy difícil el depurado de los errores;
a menudo hay que gestionar errores en cada nivel de la *pirámide*, en
vez de tener una única gestión de errores en al nivel superior. Además,
hay un fuerte acoplamiento entre las funciones, cada una de ellas sabe de la
existencia y parámetros de entrada de la siguiente. 

Pare resolver estos y otros problemas, el paradigma de programación
asíncrona más moderno es el uso de las promesas (*promises*).

Promesas o *promises*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una **Promesa** (*Promise*) es un representante (*proxy*) de un valor
que no se conoce necesariamente en el momento de crear la promesa.
Permite asociar controladores (*handlers*) al valor resultante de un
éxito o a la razón de un fallo de una acción asíncrona. Esto permite que
los métodos asíncronos devuelvan valores de forma similar a los métodos
síncronos: en lugar de devolver inmediatamente el valor final, el método
asíncrono devuelve una promesa de proporcionar dicho valor en algún
momento futuro.

Una Promesa se encuentra en uno de estos estados:

- **pendiente** (*pending*): estado inicial; no se ha cumplido ni rechazado. 

- **cumplida** (*fulfilled*): significa que la operación se completó con éxito. 

- **rechazada** (*rejected*): significa que la operación falló.

Se dice que una promesa está **resuelta definitivamente** (*settled*) si
ha sido cumplida o rechazada, pero no está pendiente.  En cualquiera de
estas situaciones, se invocan los controladores asociados que fueron
puestos en cola mediante el método ``then`` de la promesa (O las funciones
hermanas ``finally`` y ``catch``).

.. note:: 

   Si la promesa ya hubiera sido cumplida o rechazada cuando se asigna
   el controlador correspondiente, dicho controlador se ejecutará
   igualmente; por tanto, no existe condición de carrera entre la
   finalización de la operación asíncrona y la asignación de sus
   controladores.


Una promesa pendiente puede pasar a estar cumplida o rechazada. Si se
cumple, se ejecuta el controlador de cumplimiento (*on fulfillment*)
--el primer parámetro del método ``then()`` o el parámetro de
``finally``--, el cual lleva a cabo acciones asíncronas adicionales. Si
se rechaza, se ejecuta el controlador de errores, ya sea el pasado como
segundo parámetro del método ``then()`` o como único parámetro del método
``catch()``.

El ejemplo anterior usando promesas:

..code:: js

   async function doStep1(init) { return init + 1; }
     
   async function doStep2(value) { return value + 2; }
     
   async function doStep3(value) { return value + 3; }
     
   async function doOperation() {
       var result = doStep1(1)
           .then((value) => doStep2(value))
           .then((value) => doStep3(value))
           .then((value) => console.log("value is:", value))
           .catch((err) => console.error(err));
       return result;
       };

   var r = doOperation(); 
   assert(r == 7)


Fuente: https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Async_JS


Cómo copiar texto al/desde porta papeles con Javascript
------------------------------------------------------------------------

Para copiar, hay que seleccionar primero el texto que queremos, ya sea
que lo haga el usuario o el programa. Una vez hecho esto, solo hay que
llamar a ``document.execCommand("copy");``.

Por ejemplo, el siguiente código selecciona previamente todo el
contenido de un elemento de tipo ``TextArea``, identificado como
``txt_input``, y lo copia al porta papeles.

.. code:: js

    let txt_input = jQuery('#txt_input');
    txt_input.select()
    document.execCommand("copy");

Fuente: `jquery - Click button copy to clipboard - Stack
Overflow <https://stackoverflow.com/questions/22581345/click-button-copy-to-clipboard>`__

Cómo convertir de string a entero en Javascript
-----------------------------------------------

Usa la función ``parseInt``.

Funciones flecha (Arrow functions expressions)
----------------------------------------------

Una función flecha a **arrow function expression** es una forma
alternativa y más compacta de definir una nueva función en Javascript.
Pero tiene **algunas limitaciones** y no puede ser usada en todos los
casos.

Las diferencias y limitaciones con respecto a las definiciones normales
son:

- No realiza ninguna vinculación a ``this`` o ``super``, y no deben ser
usadas para definir métodos.

- No tiene la *keyword* ``new.target``.

- No pueden/deben ser usadas con ``call``, ``apply`` ni ``bind``, que
dependen por lo general de la definici’on de un *scope* perdefinido.

- No pueden ser usadas como constructores

- No pueden ejecutar ``yield``

Veamos la conversión de una definición de función normal en una función
*flecha*:

.. code:: js

    function (a) { return a + 100; }

Eliminamos la palabra clave ``function`` y ponemos una flecha (``->``)
entre la lista de parámetros y el corchete de apertura:

.. code:: js

    (a) => { return a + 100; }

Eliminamos los corchetes que delimitan el cuerpo, así como la palabra
clave ``return``, el valor retornado es implícitamente el calculado:

.. code:: js

    (a) => a + 100;

Si la lista de parámetros solo tiene un elemento, se pueden omitir los
paréntesis:

.. code:: js

    a => a + 100;

Tanto los corchetes, ``{`` y ``}``, como los paréntesis y el uso de
``return`` pueden ser obligatorios en determinados casos: En caso de
tener **múltiples parámetros** o **ningún parámetro** tendremos que
volver a usar los paréntesis. En el caso de que el cuerpo contengan
**más de una línea de código**, tenemos que volver a usar los corchetes
y usar ``return``. **No** se devuelve en estos casos el último valor
evaluado, eso sería demasiado fácil.

Fuente: `MDN Web Docs: Arrow function
expressions <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions>`__

Cómo usar la consola para depurar código con Javascript
------------------------------------------------------------------------

La forma más usada es ``console.log()``, pero hay más posibilidades:

- ``console.log()`` Para mostrar información general

- ``console.info()`` Para mensajes informativos

- ``console.debug()`` Para mensajes de depuración

- ``console.warn()`` Para mensajes de aviso

- ``console.error()`` Para mensajes de error

Añadiendo estilos al debug
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Además la salida de ``console.log`` puede usar estilos, especificados
como segundo parámetro de la llamada.

.. code:: js

    console.log('%c This is a fancy message', 'color: white;font-size:2em;background:teal')

Es importante incluir la marca ``%c`` al principio del mensaje.

String substitutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When passing a string to one of the console object’s methods that accept
a string (such as log()), you may use these substitution strings:

-  ``%s`` : texto
-  ``%i`` o ``%d`` : Números enteros
-  ``%o`` o ``%O`` : Objectos
-  ``%f`` : Números decimales

.. code:: js

    for (var i=0; i<=3; i++) {
        console.log("Hello %s. You've called me %d times", 'Marko', i+1);
    }


``console.assert()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Log a message and stack trace to the console if the first argument is
``false``.

.. code:: js

    const errorMsg = 'The number is not even';
    for (let number=0; number<=4; number++) {
        console.log('The number is ' + number);
        console.assert(number % 2 === 0, {number, errorMsg});
        }


``console.clear()``
~~~~~~~~~~~~~~~~~~~

Clear the console


``console.count()``
~~~~~~~~~~~~~~~~~~~

Log the number of times this line has been called with the given label.


``console.dir()``
~~~~~~~~~~~~~~~~~

Displays an interactive list of the properties of the specified
JavaScript object.


``console.group()`` and ``console.groupEnd()``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates a new inline group, indenting all following output by another
level. To move back out a level, call ``groupEnd()``.

The ``console.groupCollapsed()`` method creates a new inline group in
the Web Console, like ``console.group()``, but the new group is created
collapsed. The user will need to use the disclosure button next to it to
expand it, revealing the entries created in the group.

In both ``group`` or ``groupCollapsed`` methods, you can pass an
optional parameter to label the group.

console.trace()
~~~~~~~~~~~~~~~

Outputs a stack trace.


Cómo copiar texto de una página web que lo haya deshabilitado 
------------------------------------------------------------------------

Abrir la consola del navegador con ++ctrl+shift+i++ y ejecutar:

.. code:: js

    restrictCopyPasteByKeyboard = function () { return true; };

Si no funciona:

.. code:: js

    javascript:(function(){
        allowCopyAndPaste = function(e){
        e.stopImmediatePropagation();
        return true;
        };
        document.addEventListener('copy', allowCopyAndPaste, true);
        document.addEventListener('paste', allowCopyAndPaste, true);
        document.addEventListener('onpaste', allowCopyAndPaste, true);
        })();

Fuente: `Enable copy and paste in a webpage from the browser console ·
GitHub <https://gist.github.com/Gustavo-Kuze/32959786ce55b2c3751629e40c75c935>`_

Fuente: `javascript - Enable copy and paste for a site that doesn't
allow it - Stack
Overflow <https://stackoverflow.com/questions/55315209/enable-copy-and-paste-for-a-site-that-doesnt-allow-it>`_


Cómo reactivar el menú derecho del ratón
------------------------------------------------------------------------

Usa el siguiente código JavaScript en la consola del navegador:

.. code:: js

    document.addEventListener('contextmenu', event => event. stopPropagation(), true);

Fuente: `javascript - How to re-enable right click so that I can inspect
HTML elements in Chrome? - Stack
Overflow <https://stackoverflow.com/questions/21335136/how-to-re-enable-right-click-so-that-i-can-inspect-html-elements-in-chrome>`_


Cómo usar la API de almacenamiento web (*web storage*)
------------------------------------------------------------------------

La API de almacenamiento web permite almacenar información de tipo
clave/valor, que se almacena en el espacio local del usuario, gestionado
por el navegador. Es similar a ``SessionStorage``, pero este último guarda
la información mientras el navegador esté abierto, incluyendo recargas de
página y restablecimientos, mientras que ``LocalStorage`` persiste
incluso cuando el navegador se cierra.

La API de *web Storage* es muy fácil de usar: almacenas pares simples de
nombre y valor (limitados a cadenas de texto, números, etc.) y recuperas
dichos valores cuando los necesitas.

Estos mecanismos están disponibles mediante las propiedades
``Window.sessionStorage`` y ``Window.localStorage``. Al invocar uno de
éstos, se creará una instancia del objeto ``Storage``, a través del cual
los datos pueden ser creados, recuperados y eliminados. Son objetos de
almacenamiento diferente según su origen; funcionan y son controlados
por separado.

.. note:: 

    Esta API está disponible en las versiones actuales de todos los
    navegadores principales. Una prueba de disponibilidad es necesaria sólo
    para navegadores muy antiguos, como Internet Explorer 6 o
    7.

Dependiendo del navegador, su configuración, etc, comprobar si esta API
está disponible puede resultar conflictivo. Por ejemplo, solo intentar
acceder a la propiedad ``LocalStorage`` puede provocar una excepción. El
siguiente código intenta resolver este problema:

.. code:: js

    function storageAvailable(type) {
        try {
            var storage = window[type],
            x = "__storage_test__";
            storage.setItem(x, x);
            storage.removeItem(x);
            return true;
        } catch (e) {
            return (
            e instanceof DOMException &&
            // everything except Firefox
            (e.code === 22 ||
                // Firefox
                e.code === 1014 ||
                // test name field too, because code might not be present
                // everything except Firefox
                e.name === "QuotaExceededError" ||
                // Firefox
                e.name === "NS_ERROR_DOM_QUOTA_REACHED") &&
            // acknowledge QuotaExceededError only if there's something already stored
            storage.length !== 0
            );
        }
    }

Que se puede usar así:

.. code::

    if (storageAvailable("localStorage")) {
        // Yippee! We can use localStorage awesomeness
    } else {
        // Too bad, no localStorage for us
    }

El método ``Storage.getItem(clave)`` se usa para obtener un dato de la
memoria; el método ``storage.setItem(clave, valor)``. Tanto las claves
como los valores son siempre cadenas de texto. Si se usa un número como
clave, se convierte a texto. Con ``storage.removeItem(clave)`` borramos la
entrada. También se puede usar ``Storage.length`` para probar si el objeto
de almacenamiento está vació o no. El método ``Storage.clear()`` no recibe
argumentos; vacía todo el objeto de almacenamiento de ese dominio.

Cómo se comentó, los valores almacenados son siempre cadenas de texto.
Podemos almacenar valores más complejos usando JSON y las llamadas
a ``JSON.stringify()`` y ``JSON.parse``

Responder a cambios en la memoria con el evento ``StorageEvent``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se dispara un eveno ``StorageEvent`` siempre que se hace un cambio al
objeto ``LocalStorage``. Este evento es una manera para que las otras
páginas del dominio que usan la memoria sincronicen los cambios que se
están haciendo. Las páginas en otros dominios no pueden acceder a los
mismos objetos de almacenamiento.

Cambiar el tipo de entrada de un elemento ``input``
------------------------------------------------------------------------

SUpongamos este código html:

.. code::html

   <input id="hybrid" type="text" name="password" />

Con javascript haríamos:

.. code::javascript

   <script type="text/javascript">
      document.getElementById('hybrid').type = 'password';
   </script>

Como acceder a los atributos de tipo data desde Javascript
------------------------------------------------------------------------

Solo hace falta acceder a la propiedad ``dataset``. Se usacomo un
diccionario, siendo las claves los definidos pero sin el prefijo
``data-``.

Si tenemos este código html:

.. code:: html

   <span data-typeId="123"
         data-type="topic"
         data-points="-1"
         data-important="true"
         id="the-span"></span>

Podemos hacer:

.. code:: js

   document.getElementById("the-span").addEventListener("click", function() {
     var json = JSON.stringify({
       id: parseInt(this.dataset.typeid),
       subject: this.dataset.type,
       points: parseInt(this.dataset.points),
       user: "Luïs"
     });
   });

.. note::

   Además, también
   funciona con los atributos definidos en SVG.


Reescritura de funciones comunes de jQuery
------------------------------------------------------------------------

Selección de elementos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En jQuery, la selección de elementos se realiza normalmente con la
función ``$()`` o ``jQuery()``. En JavaScript puro, puede usar el método
``document.querySelector()`` para obtener el mismo resultado. Devuelve
el primer elemento que coincide con el selector especificado.

El método ``querySelectorAll(selector)`` se puede usar para seleccionar
**todos** los elementos que coinciden con el selector dado.

Por ejemplo, si tienes un código jQuery que selecciona todos los
párrafos de la página usando ``$("p")``, puedes reescribirlo en
JavaScript puro como ``document.querySelectorAll("p")``. Esto devolverá
una *NodeList* que contiene todos los elementos del párrafo.

Si quieres localizar el elemento por su ``id``, es mejor usar
``document.getElementById()``, pasando como parámetro el identificador.

Manipulación de CSS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para manipular las propiedades CSS de un elemento, jQuery proporciona el
método ``.css()``. En JavaScript puro, puede acceder directamente a la
propiedad ``style`` de un elemento y asignar valores a propiedades CSS
específicas. Por ejemplo, ``$(element).css(propiedad, valor)`` se puede
reescribir como ``element.style[propiedad] = valor``.

Gestión de eventos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En jQuery, la gestión de eventos se realiza normalmente mediante el
método ``.on()``. En JavaScript puro, se puede usar el método
``addEventListener()`` para obtener el mismo resultado. Por ejemplo,
``$(element).on(evento, manejador)`` se puede reescribir como
``element.addEventListener(evento, manejador)``.

Realización de solicitudes AJAX
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

jQuery proporciona el método ``.ajax()`` muy útil para realizar
solicitudes AJAX. En JavaScript puro, puedes usar la función ``fetch()``
para lograr el mismo resultado. Por ejemplo, ``$.ajax(options)`` se
puede reescribir como ``fetch(url, options)``.

Animación de elementos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En jQuery, la animación de elementos se suele realizar con el método
``.animate()``. En JavaScript puro, puedes lograr efectos similares usando
transiciones CSS o la API de animaciones web. Por ejemplo,
``$(element).animate(properties, duration, easing, complete)`` se puede
reescribir usando transiciones CSS.

En el siguiente ejemplo se convierte desde el código en jQuery:

.. code:: js

   // jQuery code
   $(element).animate({ opacity: 0.5, left: '+=100px' }, 500, 'easeInOut', function() {
      console.log('Animation complete!');
      });

A JS puro:

.. code::

   // Equivalent JavaScript code using CSS transitions
   element.style.transition = 'opacity 0.5s ease-in-out, left 0.5s ease-in-out';
   element.style.opacity = '0.5';
   element.style.left = parseInt(element.style.left) + 100 + 'px';

   element.addEventListener('transitionend', function() {
      console.log('Animation complete!');
      });

Otra opción es usar la API de Animaciones Web, que ofrece una forma más
potente y flexible de animar elementos. Permite crear animaciones
basadas en fotogramas clave y controlar diversos aspectos de la
animación, como la duración, la velocidad de reproducción y la
iteración.

Pasaríamos de este código jQuery:

.. code:: js
   
   // Código jQuery
   $(element).animate({ opacity: 0.5, left: '+=100px' }, 500, 'easeInOut', function() {
      console.log('¡Animación completada!');
      });

a:

.. code::

   // Código JavaScript equivalente usando la API de animaciones web
   var animation = element.animate(
      [
          { opacity: 1, left: getComputedStyle(element).left },
          { opacity: 0.5, left: parseInt(getComputedStyle(element).left) + 100 + 'px' }
      ],
      {
         duration: 500,
         easing: 'ease-in-out'
      }
      );
   animation.onfinish = function() {
      console.log('¡Animación completada!');
   };

Fuente: https://fmennen.de/post/converting-j-query-code-to-pure-java-script
