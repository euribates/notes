---
title: Notas sobre FastAPI
tags:
    - web
    - api
    - python
    - framework
    - dev
---

## Qué es FastAPI

**FastAPI** es un _framework web_ rápido y ligero para construir APIs modernas
utilizando Python 3.6 y  versiones superiores. Algunas de sus ventajas son:

- **Velocidad**: Es muy rápido. Su velocidad es comparable a la de Go y Node.js,
  que generalmente se consideran entre las opciones más rápidas para construir
  APIs.

- **Fácil de aprender y codificar**: FastAPI ya ha resuelto casi todo lo
  necesario para crear una API lista para la producción. No necesitas codificar
  todo desde cero. Con sólo unas pocas líneas de código, puedes tener una API
  RESTful lista para despliegue.

- **Documentación exhaustiva**: FastAPI utiliza los estándares de documentación
  de OpenAPI, por lo que la documentación puede generarse dinámicamente. Esta
  documentación proporciona información detallada sobre los puntos finales, las
  respuestas, los parámetros y los códigos de retorno.

- **Menos errores**: FastAPI admite la validación de datos personalizada, lo que
  permite a los desarrolladores construir APIs con menos errores. Los
  desarrolladores de FastAPI se jactan de que el marco de trabajo da lugar a
  menos errores inducidos por el ser humano, hasta un 40% menos.

- **Type hints**: El módulo de tipos se introdujo en Python 3.5. Esto permite
  declarar el tipo de una variable.

## Los atributos data-*

El núcleo de la funcionalidad de DataStar son los atributos HTML `data-*` (De
ahí el nombre). Usando estos atributois podemos obtener reactividad en el
_frontend_ de forma declarativa.

El atributo `data-on-<event>` se pueden usar para
asignar gestores al evento, y ejecutar expresiones. El valor del
atributo es una espresión Datastar, en la cual se puede usar
JavaScript:


```html
<button data-on-click="alert('I’m sorry, Dave. I’m afraid I can’t do that.')">

    Open the pod bay doors, HAL.

</button>
```

## Parcheos (_Patching_)

With Datastar, the backend drives the frontend by patching (adding, updating and removing) HTML elements in the DOM.

Datastar receives elements from the backend and manipulates the DOM using a morphing strategy (by default). Morphing ensures that only modified parts of the DOM are updated, preserving state and improving performance.

Datastar provides actions for sending requests to the backend. The @get() action sends a GET request to the provided URL using a fetch request.

<button data-on-click="@get('/endpoint')">

    Open the pod bay doors, HAL.

</button>

<div id="hal"></div>

    Actions in Datastar are helper functions that have the syntax @actionName(). Read more about actions in the reference.


If the response has a content-type of text/html, the top-level HTML elements will be morphed into the existing DOM based on the element IDs.

<div id="hal">

    I’m sorry, Dave. I’m afraid I can’t do that.

</div>

We call this a “Patch Elements” event because multiple elements can be patched into the DOM at once.
