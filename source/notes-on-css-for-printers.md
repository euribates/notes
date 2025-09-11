---
title: Notas sobre CSS para impresoras
tags:
    - html
    - css
    - web
    - print
---


## Problemas frecuentes en las versiones impresas de páginas web

- EL texto puede ser demasiado pequeño, demasiado grande o puede estar impreso
  de forma que se hace difícil de leer, como por ejemplo, con poco contraste.

- Las columnas, si las hay, pueden ser demasiado estrechas, demasiado anchas, o
  puede que el contenido se salga de los márgenes.

- Algunas secciones pueden imprimirse cortadas o incluso desaparecer
  completamente.
 
- Se gasta tinta en elementos innecesarios: fondos y/o imágenes.

- Los enlaces embebidos en la página no se ven.

- Se imprimen iconos, menús y elementos de navegación que no sirven para
  nada en la versión impresa.

## Cómo usar CSS para hacer una buena versión impresa

Podemos usar dos estrategias, o bien partir de la hoja de estilos base, y
añadimos una hoja de estilos adicional que sobreescribe ciertos valores. O
podemos usar una hoja de estilos completamente diferente: El contenido de la
página web es el mismo, pero la hoja de estilos es complemanten diferente en la
versión para imprimir.

En cualquier caso, para incluir nuestra hoja de estilos especifica para
imprimir, usaremos:

```html
<link rel="stylesheet" href="main.css">
<link rel="stylesheet" media="print" href="print.css">
```

Aquí se ha usado la primera aproximación, hay una hoja de estilos base
(`main.css`), pero para la impresión se define una hoja de estilos adicional
(`print.css`).


De forma alternativa, una única hoja de estilos puede incluir los estilos
para impresi'on, usando la regla `@media`. Por ejemplo:

```css
body {  /* main.css */
  margin: 2em;
  color: #fff;
  background-color: #000;
}

@media print {  /* override styles when printing */

  body {
    margin: 0;
    color: #000;
    background-color: #fff;
  }

}
```

Se pueden usar cualquier número de reglas `@media`, lo que puede resultar útil
para mantener juntas las definiciones que afectan al mismo elemento.


## Cómo definir el tamaño y la orientación del papel

Definir el tamaño físico del papel es básico. Para ello usamos el atributo
`@page`, que nos permite especificar el tamaño del papel, márgenes, color de
fondo y otras propiedades. Además, se pueden configurar páginas individuales,
como la primera, la última, páginas pares e impares, etc.

Se pueden usar diferentes medidas estandar para especificar el tamaño del palelÑ

- `A5` (148mm x 210mm)
- `A4` (210mm x 297mm, el tamaño por defecto)
- `A3` (297mm x 420mm)
- `B3` (353mm x 500mm)
- `B4` (250mm x 353mm)
- `JIS-B4` (257mm x 364mm)
- `letter` (8.5in x 11in)
- `legal` (8.5in x 14in)
- `ledger` (11in x 17in)

O, si fuera necesario, se puede especificar un tamaño personalizado:

```
@media print {
  @page {
    size: 8.5in 11in;
  }
}
```

Para definir la orientación de la página, se usa el atributo
`orientation`, cuyos valores posibles son:

- `portrait` (Para retrato o vertical. Es el valor por defecto)
- `landscape` (Para apaisado u horizontal)

```
@media print {
  @page {
    size: A4 landscape;
  }
}
```

## Cómo eliminar secciones de la versión impresa

Podemos eliminar de la versión impresa el contenido que no queramos, como por
ejemplo elementos redundantes, de navegación, imagenes de cabecera, cabeceras,
pies de página, etc. Para ello usaremos la opción `display: none;`, como en el
siguiente ejemplo:

```css
/* print.css */
header, footer, aside, nav, form, iframe, .menu, .hero, .adslot {
  display: none;
}
```

Nota: Puede que nos veamos obligados a usar el modificador `!important`, aunque no
esté recomendado, si existe funcionalidad javascript o css que oculte o muestre elementos dependiendo de ciertos estados.

## Simplificar la disposición

Desgraciadamente, los _layouts_ de tipo _grid_ y _flexbox_ no se llevan muy bien
con las versiones impresas. Podemos usar `display:block` y `width: 100%` para
ayudarnos en estos casos.

## Sugerencias para obtener una buena impresión

- Asegurémonos de usar texto en oscuro sobre fondo claro. Lo ideal es,
  obviamente, negro puro sobre blanco puro.

- Plantearse usar fuentes _serif_ para la versión impresa, suele ser más legible
  impresa.

- El tamaño de la tipografía debería ser de 12 puntos o superior.

- Modificar los valores de `padding` y `margin` allí donde sea necesario. Usar
  unidades estándar y absolutas, como `cm`, `mm` (o `in` si te va el rollo
  imperial).

- Usar bordes en lugar de colores de fondo. Muchas veces usamos el fondo como
  elemento para realzar determinados elementos, pero esto no funciona demasiado
  bien en la versión impresa. Se pueden usar bordes y tamaños de texto para que
  sigan siendo llamativas.


- Eliminar imágenes innecesarias. Muchas veces tenemos imágenes solo para un
  efecto estético, pero que no aporta nada más. En estos casos, puede que sea
  conveniente ocultar todas las imágenes, excepto aquellas que tengan una clase
  `print`, por ejemplo:

    ```
    /* print.css */
    * {
      background-image: none !important;
    }

    img, svg {
      display: none !important;
    }

    img.print, svg.print {
      display: block;
      max-width: 100%;
    }
    ```


## Recomendaciones para páginas con mucho texto

En una hoja estándar A4, grandes cantidades de texto resultan por lo normal difíciles de leer. Podemos usar columnas CSS en nuestras versiones impresas, con:

```css
/* print.css */
article {
  column-width: 17em;
  column-gap: 3em;
}
```

En este caso, se crean columnas con al menos `37em` de ancho, con una separación
entre columnas de `3em`. No es necesario preocuparse por el tamaño físico del
papel, si se usa un papel más ancho o se imprime en apaisado, se añadirán
automáticamente las columnas necesarias.

## Invertir imágenes en gráficas

A veces tenemos un gráfico que queremos imprimir, pero en la versión web se
utiliza un color claro para los datos sobre un fondo oscuro. Lo ideal en la
impresión es que fuera al revés, colores oscuros para los datos sobre un fondo
claro. Podemos usar CSS para invertir la imagen:

```css
/* print.css */
img.dark {
  filter: invert(100%) hue-rotate(180deg) brightness(120%) contrast(150%);
}
```

De esta forma, la imagen el web:

![Gráfico con fondo oscuro](css-for-printers/chart.png)

Se imprime como:

![Gráfico con fondo claro](css-for-printers/chart-inverted.png)


## Fuentes


[How to create Printer-Friendly Pages with CSS | Cloudflare](https://www.sitepoint.com/css-printer-friendly-pages/)
