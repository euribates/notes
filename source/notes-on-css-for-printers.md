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


Otra forma de hacerlo es usar una única hoja de estilos, que puede
incluir los estilos para impresión, usando la regla `@media`. Por
ejemplo:

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


## Añadir contenido adicional

Las versiones impresas puede que necesiten información extra que no es
necesario en la pantalla. Su pueden usar las propiedades `content` para
añadir esta información, con los pseudo-elementos `::before` y
`::after`. Por ejemplo, podemos mostrar la URL de un enlace añadiéndolo
después del texto del enlace, entre paréntesis, con el siguiente código:

```css
/* print.css */
a::after {
  content: " (" attr(href) ")";
}
```

O podemos añadir mensajes que solo se verán en la versión impresa:

```css
/* print.css */
main::after {
  content: "Copyright site.com";
  display: block;
  text-align: center;
}
```

En situaciones más complicadas, puede ser conveniente definir una clase
`print` para identificar los elementos que queremos que se vean en la
versión impresa:

```html
<p class="print">Article printed at 1:23pm 5 September 2020. Please see https://site.com/page for the latest version.</p>
```

Con el css:

```css
/* hidden on-screen */
.print {
  display: none;
}

@media print {

  /* visible when printed */
  .print {
    display: block;
  }

}
```

Nota: La mayoría de los navegadores ya incluyen, o pueden incluir, la
URL y la fecha y hora de la impresión, ya sea en la cabecera o en el
pie, así que este ejemplo puede no ser el más afortunado.

## Saltos de página

Las propiedades CSS3 `break-before` y `break-after` permiten definir
como incluir un salto de páŋina las paginas, antes o después de un
elemento. El soporte de estas propiedades es muy bueno, excepto en
navegadores realmente antiguos.

Las propiedades de `break-after` y `break-before` pueden aceptar los
siguientes valores:

- `auto`: El valor por defecto, el salto de página se permite pero no se
  fuerza.

- `avoid`: Impide el salto de página, columna o región.

- `avoid-page`: Impide el salto de página.

- `page`: fuerza un salto de página.

- `always`: un alias alternativa de `page`.

- `left`: Fuerza un salto de página de forma que la próxima página sea
  un página izquierda.

- `right`: Fuerza un salto de página de forma que la próxima página sea
  un página derecha.

El siguiente ejemplo fuerza un salto de página inmediatamente antes
de cualquier elemento `h1`:

```css
/* print.css */
h1 {
  break-before: always;
}
```

La propiedad `break-inside` (Y su versión anterior, `page-break-inside`)
permite especificar si se permite un salto de página dentro de un
elemento. Los valores más usados son:

- `auto`: El valor por defecto, se permite el salto, pero no se fuerza.

- `avoid`: Evita un salto de página/columna/región siempre que sea posible.

- `avoid-page`: Evita un salto de página siempre que sea posible.

Esta modalidad puede ser preferible a la de especificar los saltos de
página, porque normalmente lleva a un menor uso de papel, agrupando en
lo posibles elementos como tablas o imágenes.

```css
/* print.css */
table, img, svg {
  break-inside: avoid;
}
```

La propiedad `windows` permite especificar el número mínimo de líneas
dentro de un bloque que se deben mostrar al inicio de una sección.
Imaginemos un párrafo con cinco líneas de texto. El navegador puede que
intente partir el párrafo después de la cuarta línea, lo que dejaría una
solo línea de texto en la siguiente página. Esto se conoce en tipografía
como una **línea viuda**: la última línea de un párrafo, que queda
maquetada al comienzo de una página nueva y, por tanto, separada del
resto del párrafo. Si ajustamos `windows` al valor `3`, el salto de
línea se hará de forma que se mantengan juntas al menos 3 líneas de
texto.

El valor de la propiedad `orphans` se refiere al número de **líneas
huérfanas** permitidas. Es similar a las líneas viudas, pero en este caso
se refiere al número  mínimo de líneas a incluir al final de la pagina

The box-decoration-break property controls element borders across pages. When an element with a border has an inner page break:

    slice: the default, splits the layout. The top border is shown on the first page and the bottom border is shown on the second page.
    clone: replicates the margin, padding, and border. All four borders are shown on both pages.



## Fuentes


[How to create Printer-Friendly Pages with CSS | Cloudflare](https://www.sitepoint.com/css-printer-friendly-pages/)
