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
izquierda se corresponde con el centr de coordenadas, y el lienzo  o _canvas_
en el que se va a pintar mide $200x200$ unidades. El factor de escala será, por
tanto, $\frac{1}{2}$.

El siguiente ejmplo desplaza el eje de coordenadas al centro de la imagen:

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

A polygon is the easiest way to draw a freeform shape. Polygons
have a `points` property that sets a list of coordinates that are
connected with straight lines.

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


