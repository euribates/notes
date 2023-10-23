---
title: Notes on Godot Engine
---

## Sobre Godot

Godot es un motor de videojuegos 2D y 3D multiplataforma, libre y de código
abierto, publicado bajo la Licencia MIT y desarrollado por la comunidad de
Godot. El motor es funcional en sistemas Windows, OS X, Linux y BSD. Permite
exportar los videojuegos creados a PC (Windows, OS X y Linux), teléfonos
móviles (Android, iOS), y HTML5. 

## Nodos y escenas (_nodes and scenes_)

Los **nodos** son el componente básico de Godot. Hay muchos tipos diferentes de
nodos, cada uno de ellos especializado en realizar un determinada función
dentro de un juego. Un tipo de nodo, por ejemplo, se especializa en mostrar una
imagen en pantalla, otro puede encargarse de realizar una animación, otra puede
representar un modelo 3D de un objeto.

Los nodos tienen **propiedades**, que permiten definir y personalizar su
comportamiento. El sistema es modular, de forma que añades al juego solo los
nodos que necesites. Esto es bueno porque podemos empezar a hacer juegos sin
tener que conocer todos los tipos de nodos existentes.

En un proyecto, los nodos se organizan en un [**árbol
jerárquico**](https://es.wikipedia.org/wiki/%C3%81rbol_(inform%C3%A1tica)).
Todos los nodos son hijos de otros nodos, excepto el nodo raíz. Los nodos
pueden tener múltiples hijos, o no tener ninguno, pero solo pueden tener un
padre.

El conjunto de nodos agrupados en forma de árbol jerárquico forma lo que
denominamos una **escena**. El árbol de nodos se conoce normalmente como
**àrbol de la escena**.

Que el nombre no nos lleve a engaño, las escenas no son _solo_ las escenas que
podríamos pensar como fases de un juego, que lo son, pero también pueden ser
cualquier agrupación de nodos en forma de árbol que nos interese agrupar como
una escena. Por ejemplo, podemos tener una escena solo para el personaje que
controle el jugador. Otra escena podría ser un laberinto. Una fase del juego
sería otra escena, que incluiría en su árbol la escena del jugador y la escena
del laberinto.

Un aspecto muy importante de los nodos es que, además de las propiedades,
podemos asigna a un nodo un **script** o programa que controle su
comportamiento.

En Godot se puede programar en varios lenguajes, pero el recomendado para
empezar es **GDScript**, que es un lenguaje con una fuerte influencia de
**Python**, y con una integración muy fuerte con el motor.

Godot es si está escrito en **C++**, y es posible escribir extensiones en este
lenguaje para conseguir aun más rendimiento y control del motor, pero en
general esto no es necesario, especialmente al principio.

## Collision Shape

When using `Area2D`, or one of the other collision objects in Godot, it needs
to have a shape defined, or it can't detect collisions. A collision shape
defines the region that the object occupies and is used to detect overlaps
and/or collisions. Shapes are defined by Shape2D, and include rectangles,
circles, polygons, and other types of shapes.

## Gestionando la entrada con `InputEvent`

Las entradas en los juegos son complicadas, como ya vimos en su día. Los eventos,
representados en Godot Engine con objetos de la clase `InputEvent` nos permiten detectar
cosas como pulsaciones del teclado, movimiento del _joystick_, ratón, etc. Los eventos
pueden ser recibidos en múltiples lugares, dependiendo de su proposito.

Por ejemplo, podemos añadir una función para cerrar el juego si se pulsa la tecla `escape`
con el siguiente código:

```gdscript
func _unhandled_input(event):
    if event is InputEventKey:
        if event.pressed and event.scancode == KEY_ESCAPE:
            get_tree().quit()
```

Sin embargo, hay un sistema más flexible, que usa un mecanismo llamado `InputMap`. Con este
sistema, definimos las acciones de entrada que queremos usar y las asignamos a múltiples
eventos del sistema. Por ejemplo, podemos crear el evento `ir_a_la_izquierda` y asignarlo a
la tecla `A`, a la tecla con la flecha hacia la izquierda y a determinada tecla del
_gamepad_. De esta forma se puede cambiar estas correspondencias en los ajustes del proyecto
sin tener que modificar el código, e incluso permitir, dentro del juego, cambiar estas
asignaciones a gusto del jugador.

Para cambiar los ajustes, hay que ir al menú 
    
    Project > Project Settings > Input Map

Y luego usar las acciones que hay predefinidas, o creadas por uno 
mismo, por ejemplo así:

```gdscript
func _process(delta):
    if Input.is_action_pressed("ui_right"):
        # Move right
```

## Qué ficheros de Godot debemos mantener bajo control de versiones, y cuales no

El **directorio** `.import` está lleno de ficheros binarios, creados automáticamente y
regenerados cada vez que un usuario importa un proyecto. Son ficheros grandes y no tiene
sentido almacenarlos en el sistema de gestión de versiones.

Los **ficheros** con extensión `.import` almacenan las especificaciones sobre la forma en
que se deben importar determinados ficheros /Sonidos, imágenes, etc...). Estos ficheros se
generan automáticamente, si no existen, pero se pueden personalizar para controlar
determinados aspectos de la importación, por ejemplo, se puede hacer que al importar una
determinada textura, se desactive el filtrado.

En resumen: incluir los ficheros `.import` pero no incluir el directorio `.import`

## Qué es y para que sirve el nodo CharacterBody2D

La herencia de este nodo es:


``` mermaid
graph LR
  CharacterBody2D --> PhysicsBody2D;
  PhysicsBody2D --> CollisionObject2D;
  CollisionObject2D --> Node2D;
  Node2D --> CanvasItem;
  CanvasItem --> Node;
```

Es un objeto especializado en representar personajes 2D controlados por un
_script_. Su movimiento no se ve afectados por la física, pero ellos si que pueden afectar
físicamente a otros cuerpos físicos que se encuentren por el camino.

Proporciona una API de alto nivel para mover objetos que queremos que detecten
muros y reaccionen a pendientes (Vease el método
[`move_and_slide`](https://docs.godotengine.org/en/stable/classes/class_characterbody2d.html#class-characterbody2d-method-move-and-slide)). Es usado a
menudo para los personajes controlados por el jugador.

Para elementos del juego que no requieran movimientos complicados ni detección
de colisiones, como por ejemplo, plataformas móviles en un juego de
plataformas, es más sencillo de usar y configurar el nodo
[`AnimatableBody2D`](https://docs.godotengine.org/en/stable/classes/class_animatablebody2d.html#class-animatablebody2d)


