---
title: Notas sobre Datastar
tags:
    - web
    - development
    - library
    - reactive
    - backend
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
forma podemos añadir comportamiento reactivo e intreacciones con el _backend_ de
forma declarativa.

Datastar proporciona acciones (`actions`) para enviar peticiones al _backend_.
Por ejempo, la llamada a `@get()` realiza una solicitud de tipo GET a la URL
indicada.

```html <button data-on-click="@get('/endpoint')">

    Open the pod bay doors, HAL.

</button>

<div id="hal"></div> ```

En el ejemplo anterior, si la respuesta de `/endpoint` devuelve un contenido de
tipo `text/html`, los elementos de mayor nivel es transformados en el árbol DOM
ya existente para que que conviertan en los elementos retornados, basándose en
los identificadores de los elementos.

Lo importante aquí es darse cuenta de que **es el _backend_ el que determina**
los elementos que deben ser actualizados. En otros _frameworks_, lo más normal
es que esta decisión se tome en el cliente.

``` <div id="hal"> I’m sorry, Dave. I’m afraid I can’t do that.  </div> ```

Esto elementos se suelen llamar _Patch Elements_. Va en plural porque se puede
transformar múltiples elementos en el DOM con una sola llamada, (aunque
obviamente nada impide cambiar solo uno).

En el ejemplo anterior, el DOM debe contener un elemeento con un ID digual a
`hal` para que el parcheo funcione. Hay otras estrategias de parcheo, pero esta
es la más simple y la más usada en la mayoría de escenarios.

Si la respuesta tiene con `contet-type` de tipo `text/event-stream`, podemos
hacer que el contenido conste de eventos. El siguienhte ejemplo replica el
anterior, pero usando eventos:

``` event: datastar-patch-elements data: elements <div id="hal"> data: elements
I’m sorry, Dave. I’m afraid I can’t do that.  data: elements </div> ```

Como podemos enviar tanto eventos como queramos, y además se mantiene una
conexión viva, podemos extender el ejemplo anterior para que se muestre la
respuesta de [HAL 9000](https://es.wikipedia.org/wiki/HAL_9000) y luego, después
de unos cuantos segundos, se restablezca el texto inicial:

``` event: datastar-patch-elements data: elements <div id="hal"> data: elements
I’m sorry, Dave. I’m afraid I can’t do that.  data: elements </div>

event: datastar-patch-elements data: elements <div id="hal"> data: elements
Waiting for an order...  data: elements </div> ```

En el servidor, haríamos:

```python from datastar_py import ServerSentEventGenerator as SSE from
datastar_py.sanic import datastar_response

@app.get('/open-the-bay-doors') @datastar_response async def
open_doors(request): yield SSE.patch_elements('<div id="hal">I’m sorry, Dave.
I’m afraid I can’t do that.</div>') await asyncio.sleep(1) yield
SSE.patch_elements('<div id="hal">Waiting for an order...</div>')

```

## Señales

Datastar usa señales para gestionar el estado en el _frontend_. Se puede pensar
en las señales como variables reactivas cuyos valores se propagan de forma
automática a y desde las expresiones que las usan. Las señales se identifican
con el prefijo `$`.



## Atributos de Datastar

Los atributos `data-*` en DataStar tiene las siguientes caracterísiticas:

- Son evaluados en el orden en que aparecen en el DOM
- Tiene ciertas rteglas especiales en lo que respecta a mayúsculas y minúsculas
- Pueden ser renombrados (_aliases_) para evitar conflictos con otras librerías
- Pueden contener expresiones Datastar
- Tiene gestión de errores en tiempo de ejecución.


### `data-attr`

Asigna a cualquier atributo de una etiqueta HTML el valor de una expresión, y
los mantiene en sincronía.

```html
<div data-attr:title="$foo"></div>
```

También se puede usar para múltiples atributos, usando un conjunto de duplas
clave-valor,, donde las claves representan los nombres de los atributos y los
valores representan expresiones:

```
<div data-attr="{title: $foo, disabled: $bar}"><
```

### `data-text`

[TODO]
https://data-star.dev/guide/reactive_signals/#data-text

### `data-bind`

Crea una señal (_signal_), si no existía previamente, y establece un doble
vínculo entre la señal y el valor del elemento. Esto significa que el valor
del elemento se actualiza cada vez que la señal cambie, y que la señal es
modificada cada vez que el valor del elemento cambie.

Se puede poner en cualquire elemento HTML que admita entrada, como elementos
`input`, `textarea` o `select`, por ejemplo. Se añaden manejadores de eventos
para gestionar todos los cambios.

```html
<input data-bind:foo />
```

El nombre de la señal se puede especificar en la clave, como en el ejemplo anterior, o en el valor, como en el
ejemplo siguiente. Esto puede ser muy útil dependiendo del sistema de plantillas
que estés usando.

```html
<input data-bind="foo" />
```

El valor inicial de la señal es el del elemento, a menos que la señal hubiera sido definida previamente.
Por ejemplo, en el siguiente ejemplo, el valor de `$foo` sería `"bar"`:

```html
<input data-bind:foo value="bar" />
```

Pero en el siguiente, `$foo` hereda el valor de `"baz"`, porque hemos predefinido la señalÑ

```html
<div data-signals:foo="baz">

    <input data-bind:foo value="bar" />

</div>
```


## Acciones posibles en Datastar

### peek

Signatura: `@peek(callable: () => any)`

Permite accedr a las se;ales sin suscribirse a ellas.

```html
<div data-text="$foo + @peek(() => $bar)"></div>
```

En el ejemlo previo, la expresión dentro del atributo `data-text` sera
re-evaluado cada vez que `$foo` cambie, pero no será re-evaluada cuando cambie
el valor de `$bar`, porque se ha obtenido el dato mediante la acción `peek`.


### get

Signatura: `@get(uri: string, options={ })`

Envía una petición `GET` al backend. La URI puede ser cualquier _end point_
válido y la respuesta debe ser cero o más eventos SSE. Por defecto, la petición
se realiza incluyendo una cabecera `Datastar-Request: true`, y un json de la
forma `{datastar: *}` que contendrá todas las señales existentes, excepto
aquellas cuyo nombre empiece por un subrayado (`_`). También se puede usar la
opción `filterSignals`, que nos permite incluir o excluir determinadas señales
usando expresiones regulares.

!!! note "Paso de parámetros"

    Cuando se realiza una petición de tipo GET, las señales se envía como
    parámetros en línea, en otros casos, se pasan en el body. Por defecto, en formato JSON.


### post

### put

### patch

### delete
