---
title: Notas sobre SVG
tags:
    - web
    - python
    - art
---

## Sobre SVG

SVG son las siglas de Scalable Vector Graphics, (Gráficos basados en vectores
escalables). Es un formato gráfico basado en XML para crear archivos
vectoriales en 2D.

El soporte de los diferentes navegadores a las diferentes partes del estándar
SVG actualizado lo puedes ver en [Caniuse](https://caniuse.com/?cats=SVG&statuses=all).

## morphing paths

One of the attributes that can be animated in SMIL (but not in CSS) is the d
attribute (short for data) of an SVG . The d attribute contains the data which
defines the outline of the shape that you’re drawing. The path data consists of
a set of commands and coordinates that tell the browser where and how to draw
points, arcs, and lines that make up the final path.

Animating this attribute allows us to morph SVG paths and create shape tweening
effects. But, in order to be able to morph shapes, the start, end, and any
intermediate path shapes need to have the exact same number of vertices/points,
and they need to appear in the same order. If the number of vertices doesn’t
match, the animation wouldn’t work. The reason for this is that the shape
changing actually happens by moving the vertices, and interpolating their
positions, so if one vertex is missing or does not match, the paths won’t be
interpolated anymore.

To animate an SVG path, you specify the attributeName to be d, and then set the
from and to values that specify the start and end shapes, and you can use the
values attribute to specify any intermediate values you want the shape to go
through in between.

For the sake of brevity, I won’t get into the details of how to do this here.
Instead, you can read this excellent article by Noah Blon, in which he explains
how he created a shape-tweening kind-of-loading animation using . The live demo
for Noah’s article is this:

## Cómo entender las propiedades `width`, `height` y `viewBox`

Las propiedades `width` y `height` determinan **Cuanto espacio va a ocupar
la imagen en la página**, expresadas en pixels. La propiedad `viewBox`, por
otro lado, lo que hace es definir el sistema de coordenadas y las unidades de
ancho y largo que, de forma arbitraria, vamos a usar dentro de la imagen. La
combinacion de los dos valores nos daria los factores de escala.

El valor de `viewBox` conssiste en cuatro valores. Los dos primeros definen a
que punto se corresponde la esquina superior izquierda de la imagen, y los dos
siguientes definen el tamaño total (ancho y alto), desde la perspectiva de la
imagen.

En el siguiente ejemplo:

```svg
<svg 
  width="100" 
  height="100" 
  viewBox="0 0 200 200"
>
  <circle cx="100" cy="100" r="50" />
</svg>
```

La imagen ocupara en la pantalla o página del browser $100x100$ pixels.
Internamente, desde el punto de vista de la imagen, la esquina superior
izquierda se corresponde con el centro de coordenadas, y el lienzo  o _canvas_
en el que se va a pintar mide $200x200$ unidades. El factor de escala será, por
tanto, $\frac{1}{2}$.

El siguiente ejemplo desplaza el eje de coordenadas al centro de la imagen:

```svg
<svg 
  width="200"
  height="200"
  viewBox="-100 -100 200 200"
>
  <circle cx="0" cy="0" r="50" />
</svg>
```

Fuente: [SVG Tutorial](https://svg-tutorial.com/)

## Cómo usar el ellento `polygon`

Un polígono es la forma más sencilla de dibujar una forma irregular. Tienen
un atributo `points` que definen una lista de coordenadas que serán conectados
por segmentos rectos.

```svg
<svg 
  width="200"
  height="400"
  viewBox="-100 -200 200 400"
>
  <polygon 
    points="0,0 80,120 -80,120" 
    fill="#234236" 
  />
</svg>
```
Fuente: [Day 2: How to Build a Christmas Tree with SVG - SVG Tutorial](https://svg-tutorial.com/svg/polygon)

## Cómo usar el elemento `Path`

El elemento `path` es el elemento mas potente y versatil de las formas
básicas. Se puede usar para crear líneas, curvas, arcos, etc. Un _path_
permite combinar múltiples líneas rectas o curvas.

La forma de un elemento `path` se define mediante un único parámetro,
`d`, sobre cuyo contenido se hablara extensamente más adelante. El valor
del parámetro es básicamente una serie de comandos de dibujo, con sus
parámetros correspondientes.

Cada comando de dibujo se representa con una única letra. Por ejemplo,
podemos usar `M` (de _move_) para movernos a unas coordenadas `x` e `y`.

Todos los comandos vienen en dos versiones, una con la letra en
mayúscula y otra en minúscula, la versión en mayúsculas trabaja con
coordanadas absolutas, mientras que la versión en minúsculas lo hace con
coordenadas relativas. Las unidades son implícitas, relativas al sistema
de coordenadas del usuario.

Las ordenes son mover a (M/m), dibujar una línea (L/l), dibujar una
línea horizontal (H/h), dibujar una línea vertical (V/v), cerrar la
ruta (Z/z). Para hacer líneas curvas hay 3 comandos, curvas de
Bezier, en versiones cuadrática, `Q/q` o cúbica `C/c` y arcos `A/a`.




|  Comando  |  Significado                           |
|-----------|----------------------------------------|
| `M x y`   | Mueve a la posición absoluta x, y      |
| `m dx dy` | Mueve a la posición relativa dx, dy    |
| `L x y`   | Dibuja una línea desde la posición actual a la posición absoluta x, y |
| `l dx dy` | Dibuja una línea desde la posición actual a la relativa dx, dy    |
| `H x`     | Dibuja una línea horizontal hasta posición absoluta x |
| `h dx`    | Dibuja una línea horizontal hasta posición relativa dx |
| `V x`     | Dibuja una línea vertical hasta posición absoluta y |
| `v dx`    | Dibuja una línea vertical hasta posición relativa dy |
| `Z` o `z` | Cierra la ruta, uniendo el último punto con el primero |
| `C dx1 dy1 dx2 dy2 x y` | Curva de Bezier cúbica, con coordenadas absolutas |
| `c dx1 dy1 dx2 dy2 x y` | Curva de Bezier cúbica, con coordenadas relativas |
| `S dx1 dy1 x y` | Curva de Bezier cúbica, encadenada |
| `s dx1 dy1 x y` | Curva de Bezier cúbica, encadenada |
| `Q x1 y1 x y` | Curva de Bezier cuadrática, con coordenadas absolutas |
| `q x1 y1 x2 y2 x y` | Curva de Bezier cuadrática, con coordenadas relativas |


The last set of coordinates here (x, y) specify where the line should
end. The other two are control points. (x1, y1) is the control point for
the start of the curve, and (x2, y2) is the control point for the end.
The control points essentially describe the slope of the line starting
at each point. The Bézier function then creates a smooth curve that
transfers from the slope established at the beginning of the line, to
the slope at the other end.


The other type of Bézier curve, the quadratic curve called with Q, is
actually a simpler curve than the cubic one. It requires one control
point which determines the slope of the curve at both the start point
and the end point. It takes two parameters: the control point and the
end point of the curve.  As with the cubic Bézier curve, there is a
shortcut for stringing together multiple quadratic Béziers, called with
T.

`T` This shortcut looks at the previous control point used and infers a
new one from it. This means that after the first control point, fairly
complex shapes can be made by specifying only end points. This only
works if the previous command was a `Q` or a T command. If not, then the
control point is assumed to be the same as the previous point, and only
lines will be drawn.


Arcs

El otro tipo de línea curva que puede ser creada con SVG es el arco,
creado con los comandos `A` o `a`. Los arcos son **secciones de un
círculo o una elipse**. Dados dos puntos cualquiera localizados en
la elipse o círculo, hay dos arcos posibles que los unen, uno dibujado
en el sentido de las agujas del reloj y el otro en el sentido contrario.


For a given x-radius and y-radius, there are two ellipses that can connect any two points (as long as they're within the radius of the circle). Along either of those circles, there are two possible paths that can be taken to connect the points—so in any situation, there are four possible arcs available.

Because of that, arcs require quite a few parameters:
