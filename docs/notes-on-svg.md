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


