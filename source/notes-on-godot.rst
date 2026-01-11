Godot
========================================================================

Sobre :index:`Godot`
------------------------------------------------------------------------

**Godot** es un motor de vídeo juegos 2D y 3D multiplataforma, libre y
de código abierto, publicado bajo la Licencia MIT y desarrollado por la
comunidad de Godot. El motor funciona en sistemas Windows, OS/X, Linux y
BSD. Permite exportar los vídeo juegos creados a PC (Windows, OS X y
Linux), teléfonos móviles (Android, iOS), y HTML5.

En Godot se puede programar en varios lenguajes, pero el recomendado
para empezar es **GDScript**, que es un lenguaje con una gran influencia
de **Python**, y con una fuerte integración con el motor.

Godot es si está escrito en **C++**, y es posible escribir extensiones
en este lenguaje para conseguir aun más rendimiento y control del motor,
pero en general esto no es necesario, especialmente al principio.

Nodos
------------------------------------------------------------------------

Los **nodos** son el componente básico de Godot. Hay muchos tipos
diferentes de nodos, cada uno de ellos especializado en realizar un
determinada función dentro de un juego. Un tipo de nodo, por ejemplo, se
especializa en mostrar una imagen en pantalla, otro puede encargarse de
realizar una animación, otra puede representar un modelo 3D de un
objeto.

Los nodos tienen **propiedades**, que permiten definir y personalizar su
comportamiento. El sistema es modular, de forma que añades al juego solo
los nodos que necesites. Esto es bueno porque podemos empezar a hacer
juegos sin tener que conocer todos los tipos de nodos existentes.

En un proyecto, los nodos se organizan en un `árbol jerárquico`_.
Todos los nodos son hijos de otros nodos, excepto el nodo raíz. Los
nodos pueden tener múltiples hijos, o no tener ninguno, pero solo pueden
tener un padre.

Escenas
------------------------------------------------------------------------

El conjunto de nodos agrupados en forma de árbol jerárquico forma lo que
denominamos la **escena**. El árbol de nodos se conoce normalmente como
el **árbol de la escena**.

Que el nombre no nos confunda, las escenas no son *solo* las escenas que
podríamos pensar como fases de un juego, que lo son, pero también pueden
ser **cualquier agrupación de nodos en forma de árbol** que nos interese
agrupar como una escena. Por ejemplo, podemos tener una escena solo para
el personaje que controle el jugador. Otra escena podría ser un
laberinto. Una fase del juego sería otra escena, que incluiría en su
árbol la escena del jugador y la escena del laberinto.

Un aspecto muy importante de los nodos es que, además de las
propiedades, podemos **asignarles un script o programa** que controle su
comportamiento.

Como eliminar un nodo de una escena
------------------------------------------------------------------------

**tl/dr**: ``self.queue_free()``

La forma correcta es llamando al método ``queue_free()`` del propio
nodo. Si el nodo no está en una escena (lo cual es raro, pero podría
pasar) se puede eliminar simplemente con el método ``free()``.

Como convertir una rama del árbol de nodos en una escena
------------------------------------------------------------------------

Simplemente hay que arrastrar el nodo de la rama que queremos que sea la
raíz de la nueva escena a la sección de Recursos (``FileSystem``), en la
esquina inferior izquierda.

La función ``get_tree()``
------------------------------------------------------------------------

La función **``get_tree()``** nos da acceso al árbol completo de la
escena actual, en forma de un objeto de tipo `SceneTree`_


Esto nos permite controlar la escena en sí, el *viewport*, y el *game
loop*.

Se usa normalmente para cambiar, reiniciar o salir de niveles, para
añadir dinámicamente nodos, o para pausar el juego.

Métodos de uso frecuente:

-  ``reload_current_scene()`` : Carga de nuevo la escena actual

-  ``change_scene_to_file(filename)`` : Carga una nueva escena, desde un
fichero.

-  ``quit()`` : Sale del programa

Cómo cargar una escena en Godot
------------------------------------------------------------------------

Usando ``get_tree()`` podemos obtener el nodo raíz de la escena actual,
y luego, sobre ese nodo llamar al método
``change_scene_to_file(file_path)`` para cargar la nueva escena.

Ejemplo:

.. code:: gdscript

    get_tree().change_scene_to_file("res://Physics/Main.tscn")

Cómo cambiar el gris oscuro de fondo por defecto de las escenas
------------------------------------------------------------------------

En ``Project`` –> ``Settings``, ir a ``Environemnt`` y cambiar el color
etiquetado como ``Default Clear Color``.


Cómo trabajar con números aleatorios
------------------------------------------------------------------------

En el espacio global tenemos el método ``randomize()``. Este método solo
debe ser ejecutado al principio, para inicializar el generador de numero
pseudo-aleatorios con una semilla diferente, basado en el momento en que
ejecuta. También podemos fijar la semilla con ``seed(int)``.

- La función ``randi() -> int`` devuelve un número entero al azar entre
  :math:`0` y :math:`2^{32-1}`.

- La función ``randf() -> float`` devuelve un número flotante al azar
  entre :math:`0` y :math:`1`.

- La función ``randfn(float mean, float deviation) -> float`` devuelve
  un número flotante basado en una distribución normal, con media
  ``mean`` (Por defecto :math:`0`) y desviación estándar ``deviation``
  (Por defecto :math:`1.0`).

- La función ``randf_range(float from, float to) -> float`` devuelve un
  valor en coma flotante comprendido entre los valores ``from`` y
  ``to``, ambos inclusive.

- La función ``randi_range(int from, int to) -> int`` devuelve un entero
  comprendido entre los valores ``from`` y ``to``, ambos inclusive.


El nodo ``Node2D``
------------------------------------------------------------------------

Un nodo **``Node2d``** representa un objeto pensado para ser usado en un
juego 2D. Tiene una posición, una rotación (aplicada en el eje Z), una
escala para cada eje y una deformación de torsión o *skew*.

La herencia es:

.. code:: mermaid

    graph LR
    
    Node --> CanvasItem;
    CanvasItem --> Node2D;

Todos los demás objetos de tipo 2D, como objetos físicos, *sprites*,
etc. heredan de este tipo. Un uso habitual de ``Node2D`` es como nodo
padre de otros nodos 2D, ya que así todos los hijos heredan la posición,
rotación, escala, etc. También nos permite controlar de forma sencilla
el orden de *renderizado*. Los nodos de tipo ``Control`` también heredan
de la misma base que ``Node2D``, ``CanvasItem``, por lo que heredan
otras propiedades interesantes como ``z_index`` y ``visible``.

Métodos de ``Node2D``
~~~~~~~~~~~~~~~~~~~~~

Methods

- ``apply_scale(ratio: Vector2)`` : Cambia la escala

- ``get_angle_to(point: Vector2) -> float`` : Obtiene el angulo entre el
  nodo y el punto indicado ``point``.

- ``get_relative_transform_to_parent(parent: Node) -> Transform2D`` :
  Obtiene la transformación aplicada (En forma de matriz :math:`2\times
  3`) entre el nodo antecesor, indicado con ``parent`` y el nodo actual.

- ``global_translate(offset: Vector2)`` : Añade una diferencia u
  *offset* a la posición global del nodo.

- ``look_at(point: Vector2)`` : Rota el nodo de forma que el eje local
  :math:`x` del nodo se oriente hacia el punto indicado, que debe estar
  expresado en el espacio global de coordenadas.


El nodo ``CanvasItem``
------------------------------------------------------------------------

La herencia es:

.. code:: mermaid

    graph LR

    Node --> CanvasItem;

**``CanvasItem``** es una clase abstracta de la que deriva cualquier
componente en el espacio 2D, como por ejemplo ``Control`` para nodos
relacionados con la interfaz de usuario o ``Node2D`` para elementos en
juegos de dos dimensiones.

Cualquier objeto que herede de ``CanvasItem`` puede dibujar en pantalla.
El motor realiza una llamada a ``queue_redraw()``, que forzará a todos
los nodos a volver a dibujarse. A causa de esto, el control **no tiene**
que volver a pintarse obligatoriamente en cada *frame*, lo que mejora el
rendimiento de forma significativa. Hay muchos métodos de dibujo
disponibles, cuyos nombres empiezan por ``draw_*``, como por ejemplo
``draw_circle``, pero estos métodos **solo pueden ser usados dentro del
método especial ``_draw()``, ``_notificacion()`` (con el valor
``NOTIFICATION_DRAW``) o métodos que estén conectados con la señal de
``draw``**.

- `CanvasItem <https://docs.godotengine.org/en/stable/classes/class_canvasitem.html>`_

- `draw_circle() <https://docs.godotengine.org/en/stable/classes/class_canvasitem.html#class-canvasitem-method-draw-circle>`_


El nodo ``Area2D``
------------------------------------------------------------------------

La herencia es:

.. code:: mermaid

    graph LR
    
    Node --> CanvasItem;
    CanvasItem --> Node2D;
    Node2D --> CollisionObject2D;
    CollisionObject2D --> Area2D;

El objetivo de un objeto **``Area3D``** es principalmente reaccionar a
colisiones. Para ellos requiere de un ``CollisionShape`` que define la
superficie o área de colisión. Mientras que ``CollisionShape``
simplemente define un área de colisión estática, ``Area2D`` está
buscando activamente colisiones que se produzcan en esa área.

El nodo ``RigidBody2D``
------------------------------------------------------------------------

.. code:: mermaid

    graph LR
    
    Node --> CanvasItem;
    CanvasItem --> Node2D;
    Node2D --> CollisionObject2D;
    CollisionObject2D --> PhysicsBody2D;
    PhysicsBody2D --> RigidBody2D;

El node **``RigidNode2D``** es un nodo que puede ser afectado por
fuerzas y que puede ser afectado por otros, reacciona a colisiones,
tiene una masa, tiene inercia, etc. Es básicamente lo que se podría
esperar de un modelo de un objeto "real".

Cosas que hay que saber de ``RigidBody3D``:

- Utiliza el motor de físicas de Godot
- Necesita un `CollisionShape`
- Normalmente tendrá un `Sprite2D` o algo para que sea visible.

Por ejemplo, se le supone sujeto a la fuerza de la gravedad, así que su
comportamiento por defecto será "caer" en el sentido en que esté
configurada la gravedad del motor de físicas.

Necesita un nodo de tipo ``CollisionShape2D`` para definir su área de
interacción. Con la propiedad ``lineal -> Damp`` podemos definir el
rozamiento que le afecta en su movimiento. Por defecto está a cero, así
que cualquier fuerza aplicada provoca un movimiento continuo.

Podemos usar el método ``apply_force`` para aplicar una fuerza sobre el
cuerpo.

El nodo ``CollisionShape2D``
------------------------------------------------------------------------

La herencia es:

.. code:: mermaid

    graph LR
    
    Node --> CanvasItem;
    CanvasItem --> Node2D;
    Node2D --> CollisionShape2D;

A la hora de usar ``Area2D``, o alguno de los otros nodos que se usan
para detectar colisiones, es necesario definir la forma del área usada
para las colisiones. Esta es la función principal de este nodo, definir
dicho área. La forma en si está definida como un objeto de tipo
``Shape3D``, que incluye formas geométricas como rectángulos, círculos y
polígonos, entre otras.

El nodo ``AnimationPlayer``
------------------------------------------------------------------------

Un nodo **``AnimationPlayer``** sirve para crear animaciones de tipo
general, permitiendo animar (casi) cualquier característica del **nodo
que lo contenga**. Contiene un diccionario de recursos de tipo
``AnimationLibrary``, al que se puede acceder por el nombre de la
animación. Para animaciones más sencillas puede ser más sencillo usar
``tweens``.

En Godot podemos animar cualquier cosa que esté accesible desde el
Inspector, como las transformaciones de un nodo, *sprites*, elementos de
interfaz de usuario, partículas, visibilidad, color de los materiales,
etc. También se pueden modificar valores de variables e incluso llamar a
funciones.

Para poder trabajar con las animaciones lo primero es crear un nodo de
tipo ``AnimationPlayer``. Este nodo sirve como contenedor de una o más
animaciones. Un nodo de tipo ``AnimationPlayer`` puede contener
múltiples animaciones, que pueden además transicionar de una a otra.

Después de crear el nodo, hay que pulsar el botón ``Animation`` en la
parte inferior del *viewport*. Aparecerá el panel de animaciones, que
consta de cuatro partes:

- Los controles de animación, que permiten añadir, cargar, salvar o
  borrar animaciones

- Las lista de animaciones, o **tracks**

  - La **línea temporal** o **timeline**, con *frames* claves o
    *keyframes*

  - Los controles del *timeline* y de los *tracks*

La animación por ordenador se basa en el concepto de *keyframes*. Un
*keyframe* define el valor de una propiedad en un momento determinado.
Se representan en forma de diamante en cada pista. Si hay una línea
entre dos diamantes, significa que los dos *keyframes* tienen el mismo
valor, es decir, que no se produce ningún cambio entre ellos. En el
resto de los casos, es decir, cuando los valores son diferentes, se
calculan de forma automática los valores intermedios.

Un *keyframe* define el valor de una propiedad en un instante
determinado.

El uso de ``AnimationPlayer`` está orientado a animaciones más complejas
que las que se pueden hacer usando solo ``tweens``. Puede ser también
más cómodo usar la pista de animaciones, que es un entorno interactivo,
que definir la animación en código.

El nodo ``CharacterBody2D``
------------------------------------------------------------------------

La herencia de este nodo es:

.. code:: mermaid

    graph LR
    Node --> CanvasItem;
    CanvasItem --> Node2D;
    Node2D --> CollisionObject2D;
    CollisionObject2D --> PhysicsBody2D;
    PhysicsBody2D --> CharacterBody2D;

El nodo **``CharacterBody2D``** un objeto especializado en representar
personajes 2D controlados por un *script*. Sus movimiento no se ven
afectados por la física, pero ellos si que pueden afectar físicamente a
otros cuerpos físicos que se encuentren por el camino.

Proporciona una API de alto nivel para mover objetos que queremos que
detecten muros y reaccionen a pendientes (Véase el método
`move_and_slide`_

Es usado a menudo para los personajes controlados por el jugador.

Para elementos del juego que no requieran movimientos complicados ni
detección de colisiones, como por ejemplo, plataformas móviles en un
juego de plataformas, es más sencillo de usar y configurar el nodo
`AnimatableBody2D`_.


Cuándo usar ``StaticBody2D``, ``RigidBody2D`` o ``CharacterBody2D``
------------------------------------------------------------------------

Godot ofrece tres tipos diferentes de cuerpos físicos, todos agrupados
bajo la clase base ``PhysicsBody2D``.

- ``StaticBody2D``: Los objetos de esto tipo se usan para representar
  objetos físicos, que interactúan con los demás objetos físicos
  mediante colisiones, pero que **no se mueven** a causa de estas
  interacciones. Se suele usar para representar objetos que forman parte
  del entorno y que no necesitan su propio comportamiento dinámico,
  como pueden ser muros o el suelo.

- ``RigidBody2D``: Representan objetos físicos cuyos movimientos van a
  ser determinados por el motor de físicas. Esto significa que no
  controlamos ni la posición ni la velocidad del objeto, sino que
  influimos sobre él aplicando fuerzas, como gravedad, impulsos,
  `torque`_, etc. y es el motor de físicas el que calcula el movimiento
  resultante, incluyendo en sus cálculos colisiones, rebotes, rotaciones
  y cualquier otro efecto.

- ``CharacterBody2D``: Este tipo de datos proporciona detección de
  colisiones, pero **sin físicas**. Todos los movimientos deben ser
  calculados y aplicados en código, es decir, son nuestra
  responsabilidad. Su uso es principalmente para implementar al jugador
  y otros actores que requieren una física simplificada, tipo *arcade*,
  más que una simulación física más realista.

Decidir que tipo de objeto usar en el juego es una decisión importante:
usando el tipo correcto tendremos que escribir menos código, mientras
que intentar que un tipo se comporte de forma diferente de lo que está
inicialmente programa puede ser complicado y frustrante.

Cómo saber las dimensiones de la pantalla
------------------------------------------------------------------------

Llamando a
```screen_get_size`` <https://docs.godotengine.org/en/stable/classes/class_displayserver.html#class-displayserver-method-screen-get-size>`_
en el módulo ``DisplayServer``.

También podemos preguntar cuantos monitores hay disponibles.

Gestionando la entrada con ``InputEvent``
------------------------------------------------------------------------

Las entradas en los juegos son complicadas. Los eventos, representados
en Godot con objetos de la clase ``InputEvent`` nos permiten detectar
pulsaciones del teclado, movimiento del *joystick*, ratón, etc. Los
eventos pueden ser recibidos en múltiples lugares, dependiendo de su
propósito.

Por ejemplo, podemos añadir una función para cerrar el juego si se pulsa
la tecla ``escape`` con el siguiente código:

.. code:: gdscript

    func _unhandled_input(event):
        if event is InputEventKey:
            if event.pressed and event.scancode == KEY_ESCAPE:
                get_tree().quit()

Sin embargo, hay un sistema más flexible, que usa un mecanismo llamado
``InputMap``. Con este sistema, definimos las acciones de entrada que
queremos usar y las asignamos a múltiples eventos del sistema. Por
ejemplo, podemos crear el evento ``goLeft`` y asignarlo a la tecla
``A``, a la tecla con la flecha hacia la izquierda y a determinada tecla
del *gamepad*. De esta forma se puede cambiar estas correspondencias en
los ajustes del proyecto sin tener que modificar el código, e incluso
permitir, dentro del juego, cambiar estas asignaciones a gusto del
jugador.

Para cambiar los ajustes, hay que ir al menú
``Project > Project Settings > Input Map``
Y luego usar las acciones que hay predefinidas, o creadas por uno mismo,
por ejemplo así:

.. code:: gdscript

    func _process(delta):
        if Input.is_action_pressed("ui_right"):
            # Move right
 

Qué ficheros de Godot debemos mantener bajo control de versiones
------------------------------------------------------------------------

La lista de ficheros a excluir difiere entre las versiones 3 y 4 de
Godot.

El **directorio** ``.import`` está lleno de ficheros binarios, creados
automáticamente y regenerados cada vez que un usuario importa un
proyecto. Son ficheros grandes y generados automáticamente, así que no
tiene sentido almacenarlos en el sistema de control de versiones.

Los **ficheros** con extensión ``.import`` almacenan las
especificaciones sobre la forma en que se deben importar determinados
ficheros /Sonidos, imágenes, etc…). Estos ficheros se generan
automáticamente, si no existen, pero se pueden personalizar para
controlar determinados aspectos de la importación, por ejemplo, se puede
hacer que al importar una determinada textura, se desactive el filtrado.

En resumen:

Asegúrate de incluir:

- Los ficheros ‘.gs’, ‘.cs’ (Scripts)

- Los ficheros ``.tscn`` (Escenas)

- Todos los *assets*: Ficheros de imágenes (``.bmp``, ’.png\ ``,
  '.jpg``, etc.), audio (``.wav``, ``.mp3``, ``.ogg``, etc.), vídeo
  (``.mov``, ``.avi``, ``.mpg``, etc.)

- incluir **los ficheros ``.import``** pero **no incluir el directorio
  ``.import``**.

Si tenemos dudas en algún tipo de fichero, debemos incluirlo, excepto
para los siguientes casos:

- Excluir la carpeta ``.godot``. Es donde Godot almacena resultados
  intermedios.

- Excluir los ficheros ``*.translation``. Son ficheros binarios de
  traducción generados automáticamente a partir de ficheros
  ``.csv``.


Cómo detectar colisiones
------------------------------------------------------------------------

En general hay colisiones cuando utilizamos el motor de físicas,
movimientos propios, etc. El sistema de colisiones de Godot funciona
añadiendo formas o zonas de colisión (``CollisionShape2D`` para dos
dimensiones, ``CollisionShape3D`` par tres) a áreas. Por ejemplo, en 2D,
se utiliza un nodo padre de tipo ``Area3D``, con uno o más hijos de tipo
``CollisionShape2D``, que define donde se pueden producir y detectar las
colisiones.

Para poder gestionar un sistema que nos permite determinar que cosas
colisionan con que otras, se pueden definir los **capas de colisión**
(*collision mask*) y **máscaras de colisión** (*collision mask*). La
idea para entender esto es que si un objeto pertenece a una determinada
capa, solo colisionará con los objetos que estén situados en la misma
capa.

Cómo funcionan las capas y las máscaras de colisión
------------------------------------------------------------------------

-  Las **Collision Layers** básicamente especifican a que categoría o
categorías pertenece un objeto. Por decirlo de otra manera, los
objetos solo existen en las capas o *layers* que se indican.

-  Las **Collision Masks**, por otro lado, determinan la *interacción*
entre objetos. Los objetos solo interactúan con los objetos que estén
en los niveles definidos en la máscara.

Esto permite un control muy preciso sobre qué objetos pueden
interaccionar con que otros.

Como ejemplo de la utilidad de estas capas, supongamos un juegos de
aviones, en el que queremos que los aviones del jugador ``A`` colisionen
con los del jugador ``B``, y viceversa, pero que los aviones de ``A`` no
colisiones con los propios, ni los de ``B`` con los suyos. Además,
tenemos balas, que pueden colisionar con cualquier avión (Es decir, es
válido el fuego amigo).

Podríamos resolver este caso usando tres capas o *layers*, una (1) para
los aviones de ``A``, otra (2) para los aviones de ``B``. Las balas
irían en un tercer *layer*, (3).

Los aviones de ``A`` irían en la capa 1, pero la mascara se ajustaría
para detectar solo los objetos en la capa 2 (Aviones enemigos, en este
caso de ``B``) y 3 (Balas, de quien sea). La configuración para los
aviones de ``B`` sería la contraría, los aviones estarían en la capa 2
pero su máscara tendría solo la capa 1 (Aviones enemigos, en este caso
de ``A``) y 3 (balas, de quien sea).

.. note:: "Nombre de las capas"

    Se le pueden asignar nombres a las capas en ``Project settings_ ->
    _General_ -> Layer Names``


-  Fuente: `Collision Layers and Masks in Godot 4 -
Tutorial <https://www.gotut.net/collision-layers-and-masks-in-godot-4/>`_

Cómo ver las áreas de colisión de forma fácil
------------------------------------------------------------------------

Solo hay que ir al menú de *Debug* y habilitar el *checkbox* de *Visible
Collision Shapes*.

Cómo usar los *Timers* en Godot
------------------------------------------------------------------------

Un **Timer** en Godot es un nodo que realiza una cuenta atrás a partir
de un valor predeterminado, y que cuando llega a cero emite una señal,
que nosotros podemos capturar para realizar cualquier acción en nuestro
juego.

Usos típicos son:

- Una cuenta atrás antes de empezar una carrera

- Retrasar la activación de un *power-up*

- Activar oleadas de enemigos de una forma estructurada

Después de que un nodo tipo *Timer* entra en el árbol, puede ser
arrancado manualmente llamando al método ``start()``. También puede
arrancar automáticamente si se ha puesto el atributo ``autostart`` a
``true``.

Sin necesidad de escribir código, desde el editor podemos añadir el
nodo, especificar el valor de la cuenta atrás y vincular el evento de
fin de cuenta atrás con una función.

-  `Clase
Timer <https://docs.godotengine.org/en/stable/classes/class_timer.html>`_

Cómo hacer un nodo visible / invisible
------------------------------------------------------------------------

Se puede usar o bien el método ``set_visible(false|true)`` o bien
asignar a la propiedad ``visible``. Por ejemplo ``visible = false``
oculta el objeto. La propiedad y el método están definidos en la clase
``CanvasItem``, que es base de cualquier nodo que se pinte en 3D.

Solo hay que configurar la visibilidad del nodo raíz, todos los nodos
descendientes heredan la visibilidad del padre.

-  `CanvasItem <https://docs.godotengine.org/en/stable/classes/class_canvasitem.html>`_

Cómo hacer animaciones sencillas con *tweens*
------------------------------------------------------------------------

Un **``Tween``** es un objeto ligero usado para crear desde programación
animaciones sencillas. Funciona modificando un valor numérico e
interpolando su valor hasta llegar a un valor final. El nombre proviene
de *in betweening*, una técnica de animación en la que se especifican
valores claves y el ordenador calcula los *frames* intermedios.

Su uso es habitual cuando desconocemos los valores finales con
antelación. Por ejemplo, interpolar el nivel de zoom de una cámara es
sencillo con un *Tween*, y más complicado usando un ``AnimationPlayer``.
Además, consumen menos recursos que ``AnimationPlayer``, por lo que
están orientados a animaciones sencillas. Se usan con un patrón de
**dispara y olvídate** (*Fire and forget*).

.. note:: "Formas corectas de crear un *tween*"

   Un objeto de la clase ``Tween`` puede ser creado de dos maneras,
   llamando a ``SceneTree.create_tween()`` o a ``Node.create_tween()``.
   Los *Tweens* creados manualmente, es decir, usando ``Tween.new()``
   **son inválidos** y no se deben utilizar.

La animación en sí es creada añadiendo *tweeners* al onjeto ``Tween``,
usando alguno de los métodos ``tween_property()``, ``tween_interval()``,
``tween_callback()`` o ``tween_method()``:

.. code:: gdscript

    var tween = get_tree().create_tween()
    tween.tween_property($Sprite, "modulate", Color.RED, 1)
    tween.tween_property($Sprite, "scale", Vector2(), 1)
    tween.tween_callback($Sprite.queue_free)

La secuencia anterior hará que el nodo ``$Sprite`` adquiera un todo rojo
en el primer segundo, luego reduce su tamaño hasta desaparecer (escala
0) en el siguiente segundo, y finalmente llama a ``$Sprite.queue_free``
para borrarse automáticamente. Podría valer para hacer desaparecer un
enemigo en un juego. En principio, los *tweeners* se ejecuta de forma
secuencial, cuando termina una empieza el siguiente, pero esto se puede
modificar y controlar con ``parallel``, que hace que el siguiente
*tweener* se ejecute en paralelo con el previo, y ``set_parallel``, que
si se llama con ``true``, hace que todos los *tweeners* se ejecuten en
paralelo.

Una vez creado un *tweener*, se puede usar ``.set_trans``, que es un
método que esta pensado para ser usado en cascada, y que permite
modificar la transición característica del *tweener*. Por ejemplo,
podemos cambiar de una animación lineal (por defecto) a otro tipo:

.. code:: gdscript

    var tween = get_tree().create_tween()
    tween.tween_property($Sprite, "modulate", Color.RED, 1).set_trans(Tween.TRANS_SINE)
    tween.tween_property($Sprite, "scale", Vector2(), 1).set_trans(Tween.TRANS_BOUNCE)
    tween.tween_callback($Sprite.queue_free)

Figure: Esta imagen está sacada de este proyecto:
`godotTweeningCheatSheet <https://github.com/wandomPewlin/godotTweeningCheatSheet>`_

.. figure:: godot/godot_tween_cheatsheet_v4.png
    :alt: Godot Tweening Cheat Sheet

Godot Tweening Cheat Sheet

De forma similar, tenemos el método ``set_ease``, que acepta contantes
definidas en la clase ``Trans`` como ``EASE_IN``, ``EASE_OUT``,
``EASE_IN_OUT`` y ``EASE_OUT_IN``.

Podemos pasar parámetros a la función a invocar con ``tween_callback``
usando ``bind`` en la función:

.. code:: gdscript

    var tween = get_tree().create_tween()
    tween.tween_property(slot, "modulate", Color(1, 0, 0, 1.0), 0.5)
    ...
    tween.tween_callback(print.bind(self.transform))

Cómo usar las señales (*signals*) en Godot
------------------------------------------------------------------------

Las **señales** (**signals**) son mensajes que pueden emitir los nodos,
para indicar que algo les ha sucedido, como por ejemplo, un botón que ha
sido pulsado. Otros nodos pueden subscribirse a esta señal y ejecutar
una función en respuesta a ese evento.

Las señales son un mecanismo de delegación incorporado en Godot que
permite a un objeto del juego reaccionar a un cambio en otro sin
necesidad de que ninguno de los objetos se relacione directamente entre
si. Usando señales se reduce el acoplamiento y mantiene la flexibilidad
del código.

Por ejemplo, podemos actualizar una barra de estado de vida en pantalla
que represente el daño infligido al jugador. Cuando el jugador sufre un
impacto, o cuando se cure tomando una poción, queremos que la barra
refleje ese cambio. Podemos hacer esto mediante señales.

.. note:: "Cambios en Godot 4.*

    Al igual que los métodos, las señales son un tipo de datos de
    primera clase desde la versión 4.0 de Godot. Esto significa que se
    pueden pasar como argumentos directamente, en vez de usando cadenas
    de texto como se hacia antes.

Los *signals* en Godot son una implementación del `Patrón Observador
(Observer) <https://es.wikipedia.org/wiki/Observer_(patr%C3%B3n_de_dise%C3%B1o)>`_.

Cuando conectamos una señal con el método receptor, Godot crea
automáticamente un nombre para el método, siguiendo la convención
``_on_<nombre del nodo>_<nombre de la señal>``. Por ejemplo, si
conectamos la señal ``pressed`` de un ``Button2D`` llamada ``button``
usando la interfaz, está creará (Si no existía previamente) la función
``_on_button_pressed``.

En resumen, cualquier nodo puede emitir señales específicas cuando le
pase algo (como un botón al ser pulsado , por ejemplo). Otros nodos
pueden conectarse o suscribirse a señales individuales y reaccionar
frente a estos eventos. Un ``Area2D`` que represente monedas emitirá una
señal ``body_entered`` cuando el jugador colisione con ella,
permitiéndonos saber que se ha capturado la moneda.

Cómo conectar una señal con una función mediante código
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se pueden conectar una función con una señal (En términos del patrón
*Observer*, una suscripción). Un caso habitual es cuando se crean o
instancian nuevos nodos desde el programa.

Por ejemplo, supongamos que tenemos un objeto ``Timer``, llamado
igualmente ``Timer``. Estos objetos definen varias señales, supongamos
que nos interesa la señal ``timeout``, u que queremos conectar dicha
señal con nuestra función ``_on_timer_timeout()``:

Se necesita realizar dos operaciones para poder realizar la conexión
mediante código:

-  Obtener una referencia al nodo que define la señal
-  Llamar al método ``connect()`` de la señal

En el caso propuesto de ejemplo:

.. code:: gdscript


    func _on_timer_timeout():
        print('Timer timeout')

    func _ready():
        var timer := get_node("Timer")
        timer.timeout.connect(_on_timer_timeout)


Cómo crear y trabajar con tus propias señales
------------------------------------------------------------------------

Se pueden crear señales personales en un *script*. Supongamos que
queremos mostrar una pantalla de “*Game over*” cuando la salud del
jugador llegue a cero. Podríamos crear una señal propia, por ejemplo
``died`` o ``terminado`` (o el nombre que se nos ocurra), y emitir esa
señal cuando la salud llegue a cero. Lo primero será definir la señal
usando la palabra reservada ``signal``:

.. code:: gdscript

    extends Node2D

    signal terminado

    var health = 20

.. note:: "Sobre los nombres de las señales"

    Dado que las señales representan eventos que acaban de ocurrir, la
    recomendación para darles nombre es incluir un verbo en pasado.

Las señales creadas por nosotros son iguales que las incluidas por
defecto en el lenguaje. Aparecen en la pestaña de ``Node`` y se pueden
conectar igualmente al toque de ratón.

Para **emitir** la señal (es decir, notificar a todos los suscriptores)
desde código, hay que llamar al método ``emit`` de la propia señal:

.. code:: gdscript


    func take_damage(amount):
        health -= amount
        if health <= 0:
            health = 0
        health_depleted.emit()

Una señal puede declarar, de forma opcional, uno o más parámetros,
incluyéndolos como una lista separada por comas, entre paréntesis,
después del nombre de la señal:

.. code:: gdscript

    signal health_changed(old_value, new_value)

.. note:: "Parámetros de las señales"

   Los argumentos declarados aparecen en en editor, en la pestaña
   `Node``, y Godot los usará para generar de forma automática el código
   de la función receptora, si hace falta. Pero al llamar a `emit`, no
   se comprueban estos parámetros, es decir, que debemos asegurarnos de
   que estamos pasándole a la función los parámetros adecuados.

Para emitir la señal con los argumentos, los pasaremos como parámetros
adicionales a la llamada a ``emit``:

.. code:: gdscript

    func take_damage(amount):
        var old_health = health
        health -= amount
        health_changed.emit(old_health, health)


Cómo usar un GridMap
------------------------------------------------------------------------

Un **``GridMap``** es el equivalente en 3D del ``TimeMap``.

La herencia de este nodo es:

.. code:: mermaid

    graph LR
    Node --> Object;
    Node3D --> Node;
    GridMap --> Node3D;

Para usar un ``GridMap``, se debe crear un recurso llamado
``MeshLibrary``, que básicamente es el conjunto de elementos que podemos
usar para posicionar usando el *Grid Map*. Para crear un ``MeshLibrary``,
creamos una escena nueva, conteniendo los *Mesh* válidos. Para convertir
la escena en un ``MeshLibrary`` solo tenemos que usar la opción de
exportar. Los materiales y las formas de colisión que se definan en la
escena también se conservan en la librería.

Al exportar, debemos usar la extensión ``.tres`` (*text resource*).

Que es y para que sirve el nodo ``Path3D``
------------------------------------------------------------------------

Un objeto de tipo **``Path3D``** almacena una curva de Bézier en tres
dimensiones. Tiene muchos usos: definir rutas que seguir, sitios de
generación de elementos, combinarse con un ``CSG Shape`` para construir
una carretera,

Que es y para que sirve el nodo ``PathFollow3D``
------------------------------------------------------------------------

Muy vinculado con el nodo anterior, ``Path3d``, el nodo ``PathFollow3D``
nos permite **mover cosas a lo largo de una curva** descrita por un
``Path3D``. Los nodos ``PathFollow3D`` deben ser obligatoriamente hijos
de un nodo ``Path3D``.

Tienen una propiedad ``progress`` que determina la posición dentro de la
curva, en metros. También podemos usar ``progress_ratio``, que es un
valor que va de :math:`0` a :math:`1`, siendo el cero el principio de la
curva y el uno el final.

Si hacemos que un nodo sea hijo de un ``PathFollow3D``, este nodo se
moverá siguiendo la curva.


.. _AnimatableBody2D: https://docs.godotengine.org/en/stable/classes/class_animatablebody2d.html#class-animatablebody2d
.. _move_and_slide: https://docs.godotengine.org/en/stable/classes/class_characterbody2d.html#class-characterbody2d-method-move-and-slide
.. _SceneTree: https://docs.godotengine.org/en/4.4/classes/class_scenetree.html
.. _torque: https://es.wikipedia.org/wiki/Momento_de_fuerza
.. _árbol jerárquico: <https://es.wikipedia.org/wiki/%C3%81rbol_(inform%C3%A1tica)
