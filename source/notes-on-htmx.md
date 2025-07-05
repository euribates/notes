---
title: Notas sobre htmx
labels:
    - web
    - development
---

## Qué es htmx

**Htmx** es una libraría que te permite acceder a caracterísiticas avanazadas
del navegador directamente desde el HTML, sin tener que realiza llamadas a
javascript. Tomado de la documentación:

> htmx gives you access to AJAX, CSS Transitions, WebSockets and
> Server Sent Events directly in HTML, using attributes, so you
> can build modern user interfaces with the simplicity and power
> of hypertext

Está libre de dependencias, y es orientada al navegador. Esto significa
que usarla es tan sencillo como añadir una etiqueta `script` en la
sección `head`. No son necesarios procesos previos antes de usarlo. En otras
palabras, no hace falta javascript en el servidor: Ni
[node](https://nodejs.org/es), ni [npm](https://www.npmjs.com/) o similares. 

- [Documentación oficial de htmx](https://htmx.org/docs/)

## Cómo funciona htmx

El núcleo de htmx es un conjunto de atributos que permiten realizar peticiones
AJAX directamente desde el HTML:

| Atributo    | Descripción                                   |
|-------------|-----------------------------------------------|
| `hx-get`    | Realiza una petición `GET` a una URL dada     |
| `hx-post`   | Realiza una petición `POST` a una URL dada    |
| `hx-put`    | Realiza una petición `PUT` a una URL dada     | 
| `hx-patch`  | Realiza una petición `PATCH` a una URL dada   | 
| `hx-delete` | Realiza una petición `DELETE` a una URL dada  |

Cada uno de estos atributos apunta a una URL determinada. El elemento
realizara la petición a la URL correspondiente cuando se dispare
el activador.

```html
<button hx-put="/messages">
    Put To Messages
</button>
```

Esto le indica al navegador:

> Cuando el usuario pulse este botón, realiza una petición de tipo `PUT`
> a la dirección `/messages` y carga la respuesta dentro del botón.

## Cuales son los activadores de htmx

Por defecto, las peticiones AJAX se disparan por los eventos "naturales" de un
elemento:

- Los elementos `input`, `textarea` y `select` se activan en un evento de tipo
  `change`.

- El elemento `form` se activa con un evento de tipo `submit`.

- Todo lo demás se activa con un evento `click`.

Si queremos un comportamiento diferente, podemos usar el atributo `hx-trigger`
para especificar que evento activará el disparador.


El siguiente ejemplo se activa cuando el ratón entra dentro del área
de un elemento `div`:

```html
<div hx-post="/mouse_entered" hx-trigger="mouseenter">
    [Here Mouse, Mouse!]
</div>
```

## Modificadores de los disparadores

Un disparador acepta también algunos modificadores que cambian su
comportamiento. Por ejemplo, si queremos que una solicitud **solo ocurra una
vez**, podemos incluir el modificador `once` en el disparador:

```html
<div hx-post="/mouse_entered" hx-trigger="mouseenter once">
    [Here Mouse, Mouse!]
</div>
```

Otros modificadores que pueden ser usados con los disparadores son:

- `changed`: Solo se ejecuta la petición so el valor del elemento ha cambiado

- `delay:<time interval>`: Espera durante el tiempo indicado (por ejemplo `1s` para
un segundo) antes de realizar la petición. Si el evento se dispara otra vez, el
contador se reinicia.

- `throttle:<time interval>`: Espera durante el tiempo indicado antes de realizar
la solicitud. Al contrario que con `delay`, si se produce un nuevo evento
antes del tiempo límite, el evento se descarta, de forma que la petición se
realizará al final del contador.

- `from:<CSS Selector>`: Espeta por un evento de un elemento diferente. Se puede usar
para implementar atajos de teclado, por ejemplo. Hay que hacer notar que el
selector CSS no es re-evaluado si la página cambia.

Se pueden usar estos atributos para implementar carios patrones comunes de UX,
como por ejemplo una búsqueda activa:

```
<input type="text" name="q"
    hx-get="/trigger_delay"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#search-results"
    placeholder="Search...">
<div id="search-results"></div>
```

Este elemento `input` realizará una solicitud `GET` 500 milisegundos después de
que se produzca un evento de tipo pulsación de una tecla, si el contenido del
campo se ha visto modificado. El resultado es insertado en el elemento `div` con
el identificador `search-results`.

Se pueden especificar múltiples atributos de tipo `hx-trigger`, separándolos con
comas.

## Filtros de activación (_Trigger Filters_)

Se pueden aplicar filtros, usando javascript, pare discriminar si los eventos
deben activar o no los disparadores. Se especifican usando corchetes cuadrados
después del nombre del evento. Dentro de los corchetes irá una expresión en
JavaScript que será evaluada. Si devuelve `true`, el disparador se activará, en caso
contrario no lo hará.

El siguiente ejemplo solo activará el disparador si al pulsar el evento
se mantuvo pulsada la tecla Control:

```html
<div hx-get="/clicked" hx-trigger="click[ctrlKey]">
    Control Click Me
</div>
```

Las propiedades como `ctrlLKey` se resuelve primero contra el evento
desencadenante, luego en el ámbito global. El valor de `this` estará vinculado
al elemento actual.

