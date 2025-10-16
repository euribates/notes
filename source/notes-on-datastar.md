---
title: Notas sobre Datastar
tags:
    web
    development
    library
    reactive
    backend
---

## Qué es Data-star

**Datastar** es un _framework_ js ligero. Permite construir desde aplicaciones
web sencillas a aplicaciones colaborativas en la web en tiempo real. No impone
ninguna restricción en la parte de _backend_. Pesa ≈ unos 11 kB.

- [Data-star homepage](https://data-star.dev/)


## Como funciona Datastar

Con Datastar, el _backend_ es el que determina los cambios en el _frontend_
parcheando (Añadiendo, modificando o borrando) los elementos HTML en el DOM.
Las modificaciones se realizan usando una estrategia de _morphing_ por defecto,
que se asegura de solo modificar las partes del DOM que necesitan cambios,
manteniendo el estado y favoreciendo el rendimiento.

El núcleo de Datastar son los atributos `data-*`, de  ahí el nombre. De esta
forma podemos añadir comportamiento reactivo e intreacciones con el _backend_
de forma declarativa.

Datastar proporciona acciones (`actions`) para enviar peticiones al _backend_.
Por ejempo, la llamada a `@get()` realiza una solicitud de tipo GET a la URL
indicada.

```html
<button data-on-click="@get('/endpoint')">

    Open the pod bay doors, HAL.

</button>

<div id="hal"></div>
```

En el ejemplo anterior, si la respuesta de `/endpoint` devuelve un
contenido de tipo `text/html`, los elementos de mayor nivel es
transformados en el árbol DOM ya existente para que que conviertan en
los elementos retornados, basándose en los identificadores de los
elementos.

Lo importante aquí es darse cuenta de que **es el _backend_ el que determina**
los elementos que deben ser actualizados.

```
<div id="hal">
    I’m sorry, Dave. I’m afraid I can’t do that.
</div>
```

Esto elementos se suelen llamar _Patch Elements_. Va en plural porque se
puede transformar múltiples elementos en el DOM con una sola llamada,
(aunque obviamente nada impide cambiar solo uno).


