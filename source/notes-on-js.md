---
title: Notes on javascript
tags:
    - js
    - javascript
    - html
    - web
    - development
---


## Obtener la posición del cursor en un control de tipo TextArea

Podemos usar la propiedad `selectionStart` del control. Este propiedad
nos informa de la primera posición del texto seleccionado, pero
si no hay texto seleccionado, informa de la posición actual del cursor.


## Cómo copiar texto al/desde porta papeles con Javascript

Para copiar, hay que seleccionar primero el texto que queremos, ya sea que lo
haga el usuario o el programa. Una vez hecho esto, solo hay que llamar a
`document.execCommand("copy");`.

Por ejemplo, el siguiente código selecciona previamente todo el contenido de un
elemento de tipo `TextArea`, identificado como `txt_input`, y lo copia al
porta papeles.

```js
let txt_input = jQuery('#txt_input');
txt_input.select()
document.execCommand("copy");
```

Fuente: [jquery - Click button copy to clipboard - Stack Overflow](https://stackoverflow.com/questions/22581345/click-button-copy-to-clipboard)


## Cómo convertir de string a entero en Javascript

Usa la función `parseInt`.


## Funciones flecha (Arrow functions expressions)

Una función flecha a **arrow function expression** es una forma alternativa y
más compacta de definir una nueva función en Javascript. Pero tiene **algunas
limitaciones** y no puede ser usada en todos los casos.

Las diferencias y limitaciones con respecto a las definiciones normales son:

- No realiza ninguna vinculación a `this` o `super`, y no deben ser usadas para
  definir métodos.

- No tiene la _keyword_ `new.target`.

- No pueden/deben ser usadas con `call`, `apply` ni `bind`, que dependen por lo
  general de la definici'on de un _scope_ perdefinido.

- No pueden ser usadas como constructores

- No pueden ejecutar `yield`

Veamos la conversión de una definición de función normal en una función
_flecha_:


```js
function (a) { return a + 100; }
```

Eliminamos la palabra clave `function` y ponemos una flecha (`->`) entre la
lista de parámetros y el corchete de apertura:

```js
(a) => { return a + 100; }
```

Eliminamos los corchetes que delimitan el cuerpo, así como la palabra clave
`return`, el valor retornado es implícitamente el calculado:

```js
(a) => a + 100;
```

Si la lista de parámetros solo tiene un elemento, se pueden omitir los paréntesis:

```js
a => a + 100;
```

Tanto los corchetes, `{` y `}`, como los paréntesis y el uso de `return` pueden
ser obligatorios en determinados casos: En caso de tener **múltiples
parámetros** o **ningún parámetro** tendremos que volver a usar los paréntesis.
En el caso de que el cuerpo contengan **más de una línea de código**, tenemos
que volver a usar los corchetes y usar `return`. **No** se devuelve en estos
casos el último valor evaluado, eso sería demasiado fácil.

Fuente: [MDN Web Docs: Arrow function expressions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions)


## Cómo usar la consola para depurar código con Javascript

La forma más usada es `console.log()`, pero hay más posibilidades:

- `console.log()` Para mostrar información general

- `console.info()` Para mensajes informativos

- `console.debug()` Para mensajes de depuración

- `console.warn()` Para mensajes de aviso

- `console.error()` Para mensajes de error


### Adding styles

Además la salida de `console.log` puede usar estilos, especificados como segundo parámetro
de la llamada.

```js
console.log('%c This is a fancy message', 'color: white;font-size:2em;background:teal')
```

Es importante incluir la marca `%c` al principio del mensaje.


### String substitutions

When passing a string to one of the console object’s methods that accept a
string (such as log()), you may use these substitution strings:

- `%s` – string
- `%i` or `%d` – integer
- `%o` or `%O` – object
- `%f` – float

```js
for (var i=0; i<=3; i++) {
   console.log("Hello %s. You've called me %d times", 'Marko', i+1);
}
```

### `console.assert()`

Log a message and stack trace to the console if the first argument is `false`.

```js
const errorMsg = 'The number is not even';
for (let number=0; number<=4; number++) {
   console.log('The number is ' + number);
   console.assert(number % 2 === 0, {number, errorMsg});
   }
```

### `console.clear()`

Clear the console

### `console.count()`

Log the number of times this line has been called with the given label.

### `console.dir()`

Displays an interactive list of the properties of the specified JavaScript object.

### `console.group()` and `console.groupEnd()`:

Creates a new inline group, indenting all following output by another 
level. To move back out a level, call `groupEnd()`.

The `console.groupCollapsed()` method creates a new inline group in the Web
Console, like `console.group()`, but the new group is created collapsed.
The user will need to use the disclosure button next to it to expand it,
revealing the entries created in the group.

In both `group` or `groupCollapsed` methods, you can pass an optional
parameter to label the group.

### console.trace()

Outputs a stack trace.

## Cómo copiar texto de una página web que lo haya deshabilitado con Javascript

Abrir la consola del navegador con ++ctrl+shift+i++ y ejecutar:

```js
restrictCopyPasteByKeyboard = function () { return true; };
```

Si no funciona:

```js
javascript:(function(){
  allowCopyAndPaste = function(e){
  e.stopImmediatePropagation();
  return true;
  };
  document.addEventListener('copy', allowCopyAndPaste, true);
  document.addEventListener('paste', allowCopyAndPaste, true);
  document.addEventListener('onpaste', allowCopyAndPaste, true);
})();
```

Fuente: [Enable copy and paste in a webpage from the browser console · GitHub](https://gist.github.com/Gustavo-Kuze/32959786ce55b2c3751629e40c75c935)

Fuente: [javascript - Enable copy and paste for a site that doesn&#39;t allow it - Stack Overflow](https://stackoverflow.com/questions/55315209/enable-copy-and-paste-for-a-site-that-doesnt-allow-it)

## Cómo reactivar el menu derecho del ratón

Usa el siguiente cófigp JavaScript
en la consola del navegador

```js
document.addEventListener('contextmenu', event => event. stopPropagation(), true);
```

Fuente: 
[javascript - How to re-enable right click so that I can inspect HTML elements in Chrome? - Stack Overflow](https://stackoverflow.com/questions/21335136/how-to-re-enable-right-click-so-that-i-can-inspect-html-elements-in-chrome)
