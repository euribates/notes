---
title: Notas sobre Datastar
tags:
    web
    development
    library
    reactive
    backend
---

## Como funciona Datastar

Con Datastar, el _backend_ es el que determina los cambios en el _frontend_
parcheando (Añadiendo, modificando o borrando) los elementos HTML en el DOM.
Las modificaciones se realizan usando una estrategia de _morphing_ por defecto,
que se asegura de solo modificar las partes del DOM que necesitan cambios,
manteniendo el estado y favoreciendo el rendimiento.

Datastar proporciona aciones para enviar peticiones al _backend_. Por ejempo, la
llamada a `@get()` realiza una solicitud de tipo GET a la URL indicada.

```html
<button data-on-click="@get('/endpoint')">

    Open the pod bay doors, HAL.

</button>

<div id="hal"></div>
```
En el ejemplo anterior, si la respuesta de `/endpoint` devuelve un
contenido de tipo `text/html`, los elementos de mayor nivel es
transformados en el árbol DOM ya existente para que que conviertan en
los elementos retornados, basandose en los identificadores de los
elementos.

```
<div id="hal">
    I’m sorry, Dave. I’m afraid I can’t do that.
</div>
```

Esto elementos se suelen llamar _Patch Elements_, porque se puede
transformar múltiples elementos en el DOM con una sola llamada.


