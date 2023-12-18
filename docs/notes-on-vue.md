---
title: Notas sobre Vue.js
tags:
  - javascript
  - framework
  - frontend
---

## Notas sobre Vue.js

### React for Vue developers

- <https://sebastiandedeyne.com/react-for-vue-developers/>

## Cómo cambiar los delimitares

Por ejemplo, para evitar interferir con las _tags_ de las plantillas de Django o
Jinja2:

```javascript
let app = new Vue.createApp({
    delimiters: ['{%', '%}'],
    ...
}
```

## Cómo ejecutar una función nada más cargado Vue

Hay que definir la propiedad `mounted` con la función que queramos

```javascript
let app = new Vue.createApp({
  ...
  mounted: function() {
    // props are exposed on `this`
    console.log(this.foo)
  }
}
```


## El hola, mundo en Vue

Este es el código para un contador en Vue3. Em primer lugar necesitamos definir
el área en la página Html en la que correrá nuestra aplicación (El resto de la
página será invisible para Vue). Esto normalmente se hace con un `div`, pero
podría ser cualquier elemento del DOM, incluido `body`. Para este
ejemplo, usaremos un `div` con el identificador `counter`:

```html
<div id="counter">
  Counter: [[ counter ]]
</div>
```

Luego necesitamos la parte de javascript:

```js
let app = Vue.createApp({
    delimiters: ['[[', ']]'],            /* custom delimeters */
    data: function() {                   /* state definition */
        return {
            counter: 0,
        }
    },
    mounted: function() {                /* mounted function */
        console.log('Vue 3 mounted');
        },
    methods: {                           /* methods */
        increment_counter: function() {
            this.counter++;              /* Use this to access state */
            },
        },
    });

app.mount('#app');
```

Notas sobre este ejemplo:

- Definimos unos marcadores propios, `[[` y `]]` para que no entren en conflicto
  el sistema de plantillas de Vue con el sistema de plantillas de Django:

- La entrada `data` debe ser una función que devuelva un diccionario con los
  datos que definen el estado de la aplicación. En este caso, solo el valor del
  contador.

- La entrada `mounted` nos permite definir código que se ejecutará una vez que
  Vue se haya cargado y se haya montado en el árbol DOM indicado. Es útil para
  inicializaciones que dependan de que todo el árbol DOM está montado, llamadas
  a APIs externas, etc. En nuestro caso solo se usa para imprimir un mensaje de
  log.

- En `methods` definimos métodos que podremos usar más tarde en la aplicación. En
  estos métodos, `this` es una referencia a la propia aplicación Vue, así que
  podemos acceder a las propiedades como en este ejemplo, con `this.counter`.

- Es necesario montar la aplicación sobre un árbol de componentes DOM, esto se
  hace en la última línea del código.
