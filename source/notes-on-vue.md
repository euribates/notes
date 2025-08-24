---
title: Notas sobre Vue.js
tags:
  - javascript
  - framework
  - frontend
  - vue.js
---

## Notas sobre Vue.js

### React for Vue developers

- <https://sebastiandedeyne.com/react-for-vue-developers/>

## Cómo cambiar los delimitares

Por ejemplo, para evitar interferir con las _tags_ de las plantillas de Django o
Jinja2:

```javascript
let app = Vue.createApp({
    delimiters: ['[[', ']]'],
    ...
}
```

Ahora los delimitadores para la 
salida de valores son `[[` y `]]`.

## Cómo ejecutar una función nada más cargado Vue

Hay que definir la propiedad `mounted` con la función que queramos

```javascript
let app = Vue.createApp({
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
        incrementCounter: function() {
            this.counter++;              /* Use this to access state */
            },
        },
    });

app.mount('#app');
```

Ahora, para que esto funcione, necesitamos definir el siguiente código
Html:

```html
    <div id="app">
      <button @click="incrementCounter">Counter is: [[ counter ]]</button>
    </div>
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

- La vinculación entre el area de la páfina web y el codigo Vue que gestiona
  ese area se realiza usando el identificador Html, en este caso `app` (Pero
  podria sere cualquier otro valor, siempre que mantegamos la referencia
  consistente entre Html y Javascript.

- Para mostrar un valor de los definidos en la función `data`, usamos las
  marcas `[[` y `]]`, ya que así lo definimos al inicializar Vue. Esto lo
  hacemos para que no entren en conflicto, ya que el marcado por defecto
  de Vue, unsaod `{{` y `}}`, es identico al de Django.

- POdemos ejecutar los **metodos** definidos en la clave `methods`, con la
  sintaxis `@event="<nombre del evento>"`. En el ejemplo mostrado:
  `@click="incrementCounter"`.


## Como vincular un campo de un formulario con un valor de vue

Se hace mediante la directiva `v-model`, asignándole el valor de la entrada
que tenemos en Vue.

```html
<input v-model="counter">
```

También podríamos hacer el doble _binding_ a mano, usando `:value` e `@input`,
como en el siguiente ejemplo:

```html
<input
  :value="text"
  @input="event => text = event.target.value">
```

Pero es más corto y legible la opción anterior:

La directiva `v-model` puede ser usada con diferentes tipos ed entrada, como
`input`, `textarea` y `select`.

## Cómo iterar correctamente en Vue.js

Podemos usar la directiva **`f-for`** para representar una lista
de elementos a partir de un _array_. Esta directiva usa una sintaxis
especial de la forma `item in items`, donde `items` es el `array` o
fuente de datos y `item` es un alias al elemento del _array_ siendo iterado en
ese momento.

Por ejemplo, si tenemos esta fuente de datos:

```javascript
data() {
  return {
    turtles: [
        { name: 'Leonardo', 'skill': 'Katana' },
        { name: 'Raphael', 'skill': 'Sai' },
        { name: 'Michelangelo', 'skill': 'Nunchaku' },
        { name: 'Donatello', 'skill': 'Bastón Bō' },
  }
}
```

Podemos representarlo en HTML como:

````html
<li v-for="turtle in turtles">
  [[ turtle.name ]] prefers [[ item.skill ]]
</li>
```

Vue.js es capaz de detectar cuando se producen cambios en un array mediante
determinados métodos, y realizar las llamadas correspondientes para actualizar
el DOM. Los métodos que reconoce son:

- `push()`
- `pop()`
- `shift()`
- `unshift()`
- `splice()`
- `sort()`
- `reverse()`

Además, el bucle `v-for` también soporta una sintaxis adicional
que añade la opción de acceder al índice del elemento actual:

```html
<li v-for="(item, index) in items">
  [[ inted ]] : [[ turtle.name ]] prefers [[ item.skill ]]
</li>
```
