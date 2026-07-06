Shaders (Godot)
========================================================================

.. tags:: blender, game development

.. contents:: Relación de contenidos
    :depth: 3

Vectores
------------------------------------------------------------------------

En el lenguaje de *shaders* de Godot tenemos vectores de 2, 3 y 4 
dimensiones. Cada uno de los valores del vector es un *float*.

.. code:: c

    vec2 v2 = vec2(3.0, 4.0);
    vec3 v3 = vec3(3.0, 4.0, 5.0);
    vec4 v4 = vec4(3.0, 4.0, 5.0, 100.0);

Podemos combinar vectores de diferentes dimensiones. El siguiente código
es perfectamente legal

.. code:: c

    vec2 v2 = vec2(3.0, 4.0)
    vec3 v3 = vec3(vec2, 5.0)

Para acceder a los valores individuales, podemos usar los siguientes
atributos:

======== ======= ======= ========== ===============================
attr     attr    attr    Valor      Disponible en                
======== ======= ======= ========== ===============================
``x``    ``r``   ``s``   Primero    ``vec2``, ``vec3``, ``vec4``
``y``    ``g``   ``t``   Segundo    ``vec2``, ``vec3``, ``vec4``
``z``    ``b``   ``p``   Tercero    ``vec3``, ``vec4``          
``w``    ``a``   ``q``   Cuarto     ``vec4``                    
======== ======= ======= ========== ===============================

Los atributos ``r`` (*red*), ``g`` (*green*), ``b`` (*blue*)
y ``a`` (*alfa*) facilitan usar un ``vec4`` para colores.


Ademas de los vectores normales, tenemos vectores de enteros:
(``ivec2``, ``ivec3`` e ``ivec4``) y vectores de booleanos : ``bvec2``,
``bvec3`` y ``bvec4``.

Funciones
------------------------------------------------------------------------

Esta seria la estructura general:

.. code:: c

    <return type> <func_name> ( <args> ) {
        ... 
        <return> <value>;
        }

Por ejemplo:

.. code::

    int add_integer(int a, int b) {
        int result = a + b;
        return result;
        }

Documentación y referencias
------------------------------------------------------------------------

- El tutorial oficial sobre `Shaders en Godot`_.
- La `Referencia sobre shaders`_
- El `Lenguaje de Shading`_



Variables y funciones integradas
------------------------------------------------------------------------

Hay un gran número de funciones integradas, conforme a GLSL ES 3.0. 
Consulte la página de `funciones integradas`_ para obtener más información.

Sobre las variables integradas, como ``UV``, ``COLOR`` y ``VERTEX``, hay
que tener en cuenta que su disponibilidad depende tanto del tipo de
*shader* (``spatial``, ``canvas_item``, ``particle``, etc.) como de la
función utilizada (``vertex``, ``fragment``, ``light``, etc.).


Variables globales
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Los variables globales, como su nombre indica, están disponibles en
cualquier partes.

Descripción

=========== ====================================================
Nombre      Descripción
=========== ====================================================
``TIME``    Tiempo global desde que el motor ha arrancado, en
            segundos. Se repite después de cada 3.600 segundos.
            Este límite se puede cambiar en los ajustes, buscar
            ``rollover``.
``PI``      La constante PI (3.141592), relación de la longitud
            de una circunferencia respecto a su diámetro .
``TAU``     La constante TAU (6.283185) equivalente a PI * 2.
            También es el número de radianes un una vuelta
            completa.
``E``       La constante E (2.718281). El número de Euler, base
            del logaritmo natural.
=========== ====================================================

Variables disponibles en la función ``vertex``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

En la función ``vertex``, podemos acceder a las siguientes
variables:

======================= ================================================
Nombre                  Descripción
======================= ================================================
``VERTEX``              Es la más importante en este tipo de *shader*.
                        Representa la coordenada actual con la que está
                        trabajando el *shader*.
``SCREEN_MATRIX``       Coordenadas del espacio de recorte.
``UV``                  Mapa para normalizar las coordenadas de la
                        textura. El rango de salida es
                        :math:`[0.0 .. 1.0]`.
``TEXTURE_PIXEL_SIZE``  Tamaño de píxel normalizado de la textura
                        2D predeterminada. Para un ``Sprite2D`` con una
                        textura de tamaño   :math:`64 \times 32 px`,
                        ``TEXTURE_PIXEL_SIZE`` sería 
                        ``vec2(1.0/64.0, 1.0/32.0)``.
``COLOR``               Color de la primitiva del vértice multiplicado
                        por el valor de ``modulate`` del ``CanvasItem``
                        y multiplicado por el valor de
                        ``self_modulate`` de ``CanvasItem``.
``POINT_SIZE``          Tamaño de punto para el dibujo de puntos.
======================= ================================================

Variables disponibles en la función ``fragment``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La variable incorporada ``COLOR`` se utiliza para diferentes cosas:

- En la función ``vertex()``, ``COLOR`` contiene el color de la
  primitiva del vértice multiplicado por el ``modulate`` de
  ``CanvasItem`` multiplicado por el ``self_modulate`` del
  ``CanvasItem``.

- En la función ``fragment()``, es el mismo valor multiplicado por el
  color de la textura predeterminada (si está presente).

- En la función ``fragment()``, ``COLOR`` es también la salida final.

Para leer solo el contenido de la textura predeterminada, ignorando el vértice COLOR:

.. code:: c

    void fragment() {
      COLOR = texture(TEXTURE, UV);
    }

======================= ================================================
Nombre                  Descripción
======================= ================================================
``UV``                  Equivalente a la función ``UV`` de ``vertex``
``TEXTURE``             La textura usada por el ``CanvasItem``.
``NORMAL``              El mapa de normales, si se ha utilizado
======================= ================================================

Recursos sobre Shaders para Godot
------------------------------------------------------------------------

- `Godot Shaders`_

  
.. _Godot Shaders: https://godotshaders.com/

.. _funcions integradas: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shader_functions.html#doc-shader-functions
.. _Shaders en Godot: http://docs.godotengine.org/en/stable/tutorials/shaders/
.. _Referencia sobre shaders: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/index.html
.. _Lenguaje de Shading: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html
