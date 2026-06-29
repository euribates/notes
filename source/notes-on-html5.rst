HTML 5
========================================================================

.. tags:: html,development,web

.. contents:: Relación de contenidos
    :depth: 3

El elemento ``dialog``
------------------------------------------------------------------------

El elemento ``dialog`` sirve para representar una ventana de diálogo que
puede usarse para alertas, mensajes u subventanas. 

El cuadro de diálogo puede ser **modal** o **no modal**. Los cuadros de
diálogo modales bloquean la interacción con otros elementos de la
interfaz de usuario, dejando el resto de la página inactiva, mientras
que los cuadros de diálogo no modales si permiten la interacción con el
resto de la página.

.. warning:: "No se debe usar ``tabindex`` con diálogos

    El atributo ``tabindex`` no debe ser usado con elementos de tipo
    ``dialog``. El diálogo **no es** un elemento interactivo y, por
    tanto, no recibe el foco. Los elementos contenidos dentro de él,
    como por ejemplo, el botón de cierre del diálogo, si que pueden
    recibir el foco.

Los atributos más importantes de ``dialog`` son ``closedby`` y ``open``,
que veremos con más detalle.

El atributo ``closedby``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El atributo ``closedby`` permite especificar de que forma o formas puede
el usuario cerrar el diálogo. Existen tres formas diferentes:

- El cierre ligero, en el que el diálogo se cierra cuando el usuario
  pulsa o pone el foco fuera del diálogo.

- Cierre mediante una acción específica del usuario, como puede ser
  pulsar la tecla de escape, o un gesto de retroceso o vuelta atrás en
  dispositivos móviles.

- Mediante un mecanismo especifico proporcionado por el desarrollador,
  como un botón con una acción definida en el atributo ``click`` que
  llame `HTMLDialogElement.close()`` o que realice el envío de un
  formulario.

Los posibles valores son:

- ``any``: El diálogo se puede cerrar con cualquiera de los tres métodos
  descritos anteriormente.

- ``closerequest``: El dialogo solo se puede cerrar con alguno de los
  dos últimos, con una acción especifica del usuario o con un mecanismo
  dispuesto por el desarrollador.

- ``none``: Solo vale el último método, es decir, solo se puede cerrar
  el diálogo con un mecanismo específico dispuesto por el desarrollador

¿Cuál es el valor por defecto? Es un poco complicado. Si no se ha
especificado ningún valor para ``closedby``, y se ha abierto con el
método ``showModal`` se comporta como si se hubiera especificado
``closerequest``, pero si no se ha usado este método, se comporta como
si fuera ``none``.

El atributo ``open``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
El otro parámetro importante es ``open``, que indica si el diálogo está
activo y disponible para el usuario. Se recomienda usar las llamadas a
``.show()`` o ``.showModal()`` para mostrar el diálogo, mejor que usar
este atributo. Si un dialogo se abre usando este atributo, se comporta
de forma no modal.



Tipos de controles de entrada (input)
------------------------------------------------------------------------

Estos son los valores aceptados para el parámetro ``type`` de la
etiqueta ``input``:

- ``button``: Un botón

- ``checkbox``: Un cuadro de opción (opciones múltiples)

- ``color``: La entrada es un color

- ``date``: La entrada es una fecha. Dependiendo del navegador, este
  mostrará un diálogo modal para introducir la fecha.

- ``datetime-local``: La entrada es una fecha, **sin** especificar el
  `huso horario <https://es.wikipedia.org/wiki/Huso_horario>`__ local.

- ``email``: Un correo electrónico.

- ``file``: Un archivo. Hay que recordar que si usamos un campo de este
  tipo, especialmente para ficheros binarios, debemos especificar el
  atributo ``content-encoding`` con el valor ``multipart/form-data`` en
  el elemento ``form``.

- ``hidden``: Campo oculto

- ``image``: Un fichero de tipo imagen. Véase el comentario en el tipo
  ``file``.

- ``month``: Para especificar un mes **y año**.

- ``number``: Para especificar un número. Acepta los parámetros
  opcionales ``min`` y ``max`` para indicar los valores mínimo y máximo
  admisibles.

- ``password``: Un campo para contraseñas, protegido contra miradas de
  terceros.

- ``radio``: Un circulo de opción (opciones mutuamente excluyentes).

- ``range``: Un valor, definido de forma aproximada mediante un
  *slider*, dentro de un rango de valores numéricos. Inicialmente el
  rango va de 0 a 100, pero se pueden definir ambos límites con los
  parámetros opcionales ``min`` y ``max``.

- ``reset``: Limpia todos los campos del formulario.

- ``search``: Un parámetro de búsqueda.

- ``submit``: Un botón de envío de un formulario.

- ``tel``: Un teléfono.

- ``text``: Texto normal.

- ``time``:

- ``url``: Una URL. El *browser* no verifica que la dirección sea
  válida, pero si que este bien construida.

- ``week``: Permite seleccionar una semana **y un año**.
