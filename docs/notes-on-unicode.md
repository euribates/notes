---
title: Notas sobre Unicode
tags:
    - linux
    - unicode
---

## Qué es Unicode

**Unicode** es un estándar de codificación de caracteres diseñado para
facilitar el tratamiento informático, transmisión, y visualización de textos de
numerosos idiomas y disciplinas técnicas, además de textos clásicos de lenguas
muertas. El término Unicode proviene de los tres objetivos perseguidos:
universalidad, uniformidad, y unicidad.

Unicode define cada carácter o símbolo mediante un nombre e identificador
numérico, el **punto de código** (`code point`). Además incluye otras
informaciones para el uso correcto de cada carácter, como sistema de escritura,
categoría, direccionalidad, mayúsculas y otros atributos. Unicode trata los
caracteres alfabéticos, ideográficos y símbolos de forma equivalente, lo que
significa que se pueden mezclar en un mismo texto sin utilizar marcas o
caracteres de control.

Por ejemplo, el símbolo `a` tiene el código de punto $97$. El `code point` para
el carácter `✓` (_Checkmark_) es el $10003$ ($2713$, en hexadecimal).  Estos
códigos son universales y únicos. Obsérvese que es este momento no nos estamos
preocupando de como se van a almacenar estos números, Unicode simplemente
asigna punto de código únicos a determinado símbolos gráficos de alfabetos,
incluyendo escrituras históricas extintas, utilizadas con fines académicos,
como el [cuneiforme](https://es.wikipedia.org/wiki/Escritura_cuneiforme) o el
[rúnico](https://es.wikipedia.org/wiki/Alfabeto_r%C3%BAnico), sistemas
ideográficos y otras colecciones de símbolos, como los utilizados en
matemáticas, tecnología, música, iconografía, etc.

Fuentes:

- [Todo sobre Unicode (en realidad lo mínimo indispensable) · El Blog de pmoracho](https://pmoracho.github.io/blog/2019/06/04/Unicode/)

- [Unicode: Lo que necesitas saber como programador de Python ::  Python Brasil 2022](https://www.youtube.com/watch?v=sYWZ23N2Jqg)

## Caracteres Unicode para el dibujo de cajas (_Box Drawing_)

Official Unicode Consortium code chart (PDF)

```
    0   1   2   3   4   5   6   7   8   9   A   B   C   D   E   F
U+250x  ─   ━   │   ┃   ┄   ┅   ┆   ┇   ┈   ┉   ┊   ┋   ┌   ┍   ┎   ┏
U+251x  ┐   ┑   ┒   ┓   └   ┕   ┖   ┗   ┘   ┙   ┚   ┛   ├   ┝   ┞   ┟
U+252x  ┠   ┡   ┢   ┣   ┤   ┥   ┦   ┧   ┨   ┩   ┪   ┫   ┬   ┭   ┮   ┯
U+253x  ┰   ┱   ┲   ┳   ┴   ┵   ┶   ┷   ┸   ┹   ┺   ┻   ┼   ┽   ┾   ┿
U+254x  ╀   ╁   ╂   ╃   ╄   ╅   ╆   ╇   ╈   ╉   ╊   ╋   ╌   ╍   ╎   ╏
U+255x  ═   ║   ╒   ╓   ╔   ╕   ╖   ╗   ╘   ╙   ╚   ╛   ╜   ╝   ╞   ╟
U+256x  ╠   ╡   ╢   ╣   ╤   ╥   ╦   ╧   ╨   ╩   ╪   ╫   ╬   ╭   ╮   ╯
U+257x  ╰   ╱   ╲   ╳   ╴   ╵   ╶   ╷   ╸   ╹   ╺   ╻   ╼   ╽   ╾   ╿
```

## Símbolos tipográficos útiles en Unicode


tabla:

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

Otra tabla:

| Símbolos | code point (Hex) | Desc             |
|----------|------------------|------------------|
| ✓        | 2713             | check mark       |
| ✗        | 2717             | cross mark       |
| §	       | 00A7             | section          |
| ¶	       | 00B6             | paragraph        |
| ·	       | 00B7             | middle dot       |
| †	       | 2020             | dagger           |
| ‡	       | 2021             | double dagger    |
| •	       | 2022             | bullet           |
| …	       | 2026             | ellipsis         |
| ←	       | 2190             | left arrow       |
| ↑	       | 2191             | up arrow         |
| →	       | 2192             | right arrow      |
| ↓	       | 2193             | down arrow       |
| ☐	       | 2610             | ballot box       |
| ☑	       | 2611             | ballot box check |
| ☒	       | 2612             | ballot box X     |
| ★	       | 2605             | black star       |
| ☆	       | 2606             | white star       |
| □	       | 25A1             | square           |

Fuente: [Unicode/List of useful symbols - Wikibooks, open books for an open world](https://en.wikibooks.org/wiki/Unicode/List_of_useful_symbols)

## UTF-16

**UTF-16**, es una forma de codificación de caracteres Unicode
utilizando símbolos de longitud variable, pero usando palabras de
16 bits, en vez de bytes. Para codificado un `code point` su usan
1 o 2 palabras de 16 bits por carácter Unicode (2 o 4 bytes).

Por ejemplo, el texto "Hello", un UTF-16, se codifica,
(usando hexadecimal), como:

```
0048 0065 006C 006C 006F
---- ---- ---- ---- ----
 H    e    l    l    o 
```

## UTF-8

UTF-8 es un sistema (De entre otros varios posibles, como el UTF-16) para
almacenar los _code points_ de Unicode, usando bytes de 8 bits, en vez de
palabras de 18 bits. En UTF-8, cada punto de código de 0-127 se almacena en un
solo byte. Sólo los puntos de código 128 y superiores se almacenan utilizando
2, 3, y de hecho, hasta 6 bytes.

Esto tiene el efecto secundario --y deseado-- de que el texto en inglés se ve
**exactamente igual en UTF-8 que en ASCII**, 

Específicamente, `Hello`, que era `00480065006C006C006F` en UTF-16, se
almacenará como `48656C6C6F` en UTF-8, que es lo mismo que se almacenaba en ASCII.


y ANSI, y en todos los juegos de caracteres OEM del planeta. Ahora, si eras tan
atrevido como para usar letras acentuadas, griegas o klingon, tendrás que usar
varios bytes para almacenar un único “code point”, pero los estadounidenses
nunca se darán cuenta. (UTF-8 también tiene la agradable propiedad de que el
ignorante código de procesamiento de cadenas que quiera usar un solo byte 0
como terminador nulo no truncará las cadenas).

## Cosas que hay que tener en cuenta al trabajar con UTF-8

- **NO se puede** determinar la longitud de una cadena de texto simplemente
  contando los bytes.

- **NO se puede** saltar directamente a una posición aleatoria dentro de una
  cadena de texto y asumir que a partir de ahí se puede leer texto; podriamos
  estar en medio de un caracter que usara más de un byte, y eso prococa que el
  resto se interprete incorrectamente.

- **No se puede idividir u obtener una subcadena de texto cortando en una
  posicion aleatoria, por las mismas razones que el punto antrerior.


