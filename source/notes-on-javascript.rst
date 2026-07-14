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

Adding styles
~~~~~~~~~~~~~

Además la salida de ``console.log`` puede usar estilos, especificados
como segundo parámetro de la llamada.

.. code:: js

    console.log('%c This is a fancy message', 'color: white;font-size:2em;background:teal')

Es importante incluir la marca ``%c`` al principio del mensaje.

String substitutions
~~~~~~~~~~~~~~~~~~~~

When passing a string to one of the console object’s methods that accept
a string (such as log()), you may use these substitution strings:

-  ``%s`` – string
-  ``%i`` or ``%d`` – integer
-  ``%o`` or ``%O`` – object
-  ``%f`` – float

.. code:: js

    for (var i=0; i<=3; i++) {
        console.log("Hello %s. You've called me %d times", 'Marko', i+1);
    }

``console.assert()``
~~~~~~~~~~~~~~~~~~~~

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


Cómo usar la API de almacenamiento web
------------------------------------------------------------------------

La API de almacenamiento web permite almacenar información de tipo
clave/valor, que se almacena en el espacio local del usuario, gestionado
por el navegador. Es similar a ``SessionStorage``, pero este último guarda
la información mientras el navegador esté abierto, incluyendo recargas de
página y restablecimientos, mientras que ``LocalStorage`` persiste
incluso cuando el navegador se cierra.

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

