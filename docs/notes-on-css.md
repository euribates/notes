---
title: Notes on CSS
---

## CSS Variables (Custom Properties)

This has indeed been possible with SASS and LESS variables for years. However,
there are a few big benefits with CSS Variables.

They don’t require any transpiling to work, as they’re native to the browser.
So you don’t need any setup to get started, as you do with SASS and LESS.  They
live in the DOM, which opens up a ton of benefits, which I’ll go through in this
article and in my upcoming course.

```css
:root {
  --red: #FF6f69;
}

#title {
  color: var(--red);
  }

.quote {
  background-color: var(--red); 
}
```

To declare a variable, you first need to decide which scope the variable should
live in. If you want it to be available globally, simply define it on the
`:root` pseudo-class. It matches the root element in your document tree (usually
the `<html>` tag).

As you can see, you declare a variable just the same way you’d set any CSS
property. However, the variable must start with two dashes. To access a
variable, you need to use the `var()` function, and pass in the name of the
variable as the parameter.

You can also create **local variables**, which are accessible only to the
element it’s declared at and to its children. This makes sense to do if you know
that a variable only will be used in a specific part (or parts) of your app.

For example, you might have an alert box which uses a special kind of colour
which aren’t being used in other places in the app. In that case, it might make
sense to avoid placing it in the global scope:

```css
.alert {  
  --alert-color: #ff6f69;  
}
```

This variable can now be used by its children:

```css
.alert p {  
  color: var(--alert-color);  
  border: 1px solid var(--alert-color);  
}
```

Una ventaja de las variables/propiedades es que tienen **acceso al DOM**, algo
que losp rocesadores como LESS o SASS no pueden hacer. Por ejemplo, podemos
cambiar el valor de una variable basándonos en el ancho de la ventana, por
ejemplo:
 
```css
:root {  
  --main-font-size: 16px;  
}

media all and (max-width: 600px) {  
  :root {  
    --main-font-size: 12px;  
  }  
}
```

EL código CSS anterior actualiza el tamaño principal de las fuentes en caso de
que el área de visualización sea pequeña (600 _pixels_ o menos, para ser
precisos).

Otra gran ventaja es que podemos acceder e incluso modificar estas
variables/propiedades desde Javascript. Para leer una variable CSS desde
Javascript hacen falta estas tres líneas de código:

```js
var root = document.querySelector(':root');  
var rootStyles = getComputedStyle(root);  
var mainColor = rootStyles.getPropertyValue('--main-color');
```

Para actualizar, se usa el método `setProperty` del elemento dentro del cual
está defininida la variable, y se le pasan como parámetros el nombre de la
variable y el nuevo valor:

```js
root.style.setProperty('--main-color', '#88d8b0')
```

Fuente: [Learn CSS Variables in 5 minutes - A tutorial for beginners](https://www.freecodecamp.org/news/learn-css-variables-in-5-minutes-80cf63b4025d)



## Animaciones y transiciones

CSS nos permite crear animaciones complejas y controlarlas de varias formas.
Una animación se describe usando dos partes: un conjunto de **@keyframes** y
los correspondientes parámetros animados. Este es un ejemplo:

```
@keyframes stretching {
  0% {
    width: 100px;
  }
  100% {
    width: 200px;
  }
}
```

La animación de este ejemplo se llama `stretching` (Podriamos llamarla como
queramos) y describe los cambios en los estilos desde un momento inicial hasta
un momento final. Esta animación puede ser aplicada a cualquier elemento. Para
ello, necesitamos definir el nombre de la animacion (Con `animation-name` y la
duración (con `animation-duration`), como en el siguiente ejemplo:

```css
.button {
  animation-name: stretching;
  animation-duration: 1s;
}
```

Para cada animación, necesitas asignarle un nombre y describir como mínimo un
valor, aunque normalmente definiremos más. Podemos especificar (o no) los
valores iniciales y finales de la animación. Esto se puede hacer usando los
valores `0%` y `100%`, como ya vimos, o con las palabras reservadas `from` y
`to`. Podemos definir valores intermedios usando cualquier valor comprendido
entre el `0%` y el `100%`.

Si omitimos el keyframe inicial, la animación se ejecuta desde el estilo
inicial que tenga el elemento, siguiendo los pasos definidos.

Si omitimos el valor final, la animación se ejecuta hasta el último paso, y
luego retrocede hasta volver a su estado inicial.

la duración de la animación puede espedificarse usando diferentes unidades,
segundos, como en `2s`, o milisegundos: `250ms`.

El siguiente ejemplo no define un estado inicial (No hay ningun paso definido
en el valor `0%` o `from`), pero aplica una trasformacion que rota -90º
a la mitad de la animación (`50%`) y finaliza con una rotación completa de 360º
grados:

```css
@keyframes rotate {
  50% {
    transform: rotate(-90deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
```

El estado inicial será el del objeto al que aplicamos la trasformación; si no
ha sido modificado, será de 0º.

El siguiente ejemplo define una animación del color de fondo (`background-color`) en 4 fases. Usamos
`to` y `from`, pero podríamos haberla heccho exactamente igual con `0%` y
`100%`:

```css
@keyframes coloring {
  from { background-color: red; }
  33%  { background-color: yellow; }
  66%  { background-color: green; }
  to   { background-color: blue; }
}
```

Si borraramos el estado final, `to`, el color pasararia de rojo a amarillo,
verde y azul y luego, retrocede volviendo a verde, amarillo y finalmente de
nuevo al color rojo.

La propiedad `transform` es muy interesante y potente, ya que permite realiza
muchas transformaciones distintas. Hemos visto `rotate`, para girar sobre el
eje Z, también podemos desplazar el objeto, con `translateY` o `translateX`:

```
@keyframes lift-up {
  from {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-250px);
    }
  to {
    transform: translateY(-300px);
    }
}
```

Los `keyframes` pueden ser agrupados simplemente usando comas. El siguiente
ejemplo define una animación que mantendrá el ancho fijo a 100 pixels durante
la primera mitad, y en la segunda se irá incrementado hasta el valor final de
200 pixels:

```css
@keyframes stretching {
  0%, 50% {
    width: 100px;
  }
  100% {
    width: 200px;
  }
}
```

### Animaciones complejas

Se puede aplicar varias animaciónes diferentes al mismo elemento. Los cambios
se realizarán simultaneamente.

Para ello, se asignan varias animaciones, separadas com coma, en la propiedad
`animation-name`. Si queremos que todas las animaciones duren lo mismo, podemos
dejar un único valor en `animation-duration`, pero también podemos asignar
diferentes duraciones para cada animación, de nuevo usando comas para separa
cada posible valor.

### Repetir animaciones

Hasta ahora, las animaciones solo se han ejecutado una vez. Podemos usar la
propiedad `animation-iteration-count` para especificar el número de
repeticiones que queremos. Acepta números positivos (o incluso el cero, en ese
caso no se ejecutará) o la palabra clave `infinite` para que se repita de forma
cíclica sin fin.

### Sentido de la animación

Con el atributo `animation-direction` definimos el sentido de la animación; por
defecto vale `normal`, que es ejecutar la animación desde el valor `from` hasta
el valor `to`, pero si la cambiamos a `reverse`, la animación se ejecuta al
contrario, desde `to` hasta `from`.

Además de `normal` y `reverse`, hay otros dos posibles valores, que solo tiene
sentido usar cuando el número de repeticiones de la animación
(`animation-iteration-count`) es mayor que 1: Si usamos `alternate`, las
animaciones impares se ejecutan en el orden normal, y las pares en orden
inverso. Con el valor `alternate-reverse` es justo al contrario, las
animaciones impares se ejecutan en orden inverso y las pares en orden normal.

```css
@keyframes clockwise {
  to {
    transform: rotate(180deg);
  }
}

@keyframes counterclockwise {
  to {
    transform: rotate(-180deg);
  }
}

.gear-big {
  animation-name: clockwise;
  animation-duration: 2s;
  animation-iteration-count: infinite;
  animation-direction: alternate-reverse;
}

.gear-small {
  animation-name: counterclockwise;
  animation-duration: 2s;
  animation-iteration-count: infinite;
  animation-direction: alternate-reverse;
}
```

### Asigna un retraso o _delay_ a una animación

Podemos asignara un retraso o _delay_ con la propiedad `animation-delay`. Eso
nos permite encadenar animaciónes sin que se ejecuten simultaneamente, o
solapándose. Admite las mismas unidades que `animation-duration`, esto es,
segundos con `s` o milisegundos con `ms`.

### definiendo el estado final de la animación

Hasta ahora las animaciones volvian al estado original después de ejecutada la
animación, pero definiendo la propieddad `animation-fill-mode` a `forwards`
podemos hacer que el elemento se quede con los valores finales después de la
animación.

Otro valor posible es `backwards`. Este valor define el estado del elemento antes de la ejecución de la animacion; si un elemento tiene asignada una animación con un _delay_ y el parámetro 
`animation-fill-mode` a `backwards`, los estilos descritos en el primer paso de
la animación, ya sea usando `from` o `0%` serán aplicados al principio, entes
de que la aplicación se ejecute.

El tercer valor posible es `both`: Combina los dos anteriores, es decir, antes
de la animación, el elemento adquiere los valores definidos en el primer paso,
`from` o `0%`, y después de la animación, se queda con los valores definod en
el último paso, `to` o `100%`.

### Parar (pause) y continuar una animación

Hay una propiedad `animation-play-state`, con dos posibles valores, `running` y
`paused`, que nos permite pausar y continuar la animación


### Definiendo la forma de la animación

La propiedad más importante de la animación es `animation-timing-function`, y
define la forma en que la animación es ejecutada; las aceleraciones y
velocidades con las que se animan las propiedades. El valor por defecto es
`ease`, que proporciona una animación suave, con una aceleración al principio y
una desaceleración al final.  Otros posibles valore son: `linear` para realizar
un movimiento lineal, sin ninguna aceleración ni al principio ni al final; el
típico movimiento "robótico". Los valores `ease-in` y `ease-out` realizan una
aceleración suave al principio o una desaceleracion suave al final,
respectivamente. El valor `ease-in-out` es similar a `ease`, pero con cambios
de velocidad algo más rápidos.

Tambien podemos asignarle a esta propiedad una curva con la función
`cubic-bezier`; de hecho todos los nombres `ease`, `ease-in`, etc. son solo
alias para llamar a esa función con ciertos parámetros predefinidos.

```css
animation-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1);
```


Usando las transiciones de CSS3, podemos aplicar estas animaciones a objetos
cuando eston cambien de estado; por ejemplo cuando el ratón se situa encima,
(`hovered over`), cuando adquiere el foco (`focused on`), cuando se activa
(`active`) o se fija como objetivo (`targeted`)
With CSS3 transitions you have the potential to alter the appearance and
behavior of an element whenever a state change occurs, such as when it is
**hovered over**, **focused on**, **active**, or **targeted**.

Animations within CSS3 allow the appearance and behavior of an element to be
altered in multiple keyframes. **Transitions** provide a change from one state
to another, while **animations** can set multiple points of transition upon
different keyframes.


### Transiciones

As mentioned, for a transition to take place, an element must have a change in
state, and different styles must be identified for each state. The easiest way
for determining styles for different states is by using the `:hover`, `:focus`,
`:active`, and `:target` pseudo-classes.

There are **four transition related properties in total**, including
`transition-property`, `transition-duration`, `transition-timing-function`, and
`transition-delay`. Not all of these are required to build a transition, with
the first three are the most popular.

In the example below the box will change its background color over the course of
1 second in a linear fashion.

```
.box {
  background: #2db34a;
  transition-property: background;
  transition-duration: 1s;
  transition-timing-function: linear;
}

.box:hover {
  background: #ff7b29;
}
```

**Vendor Prefixes**

The code above, as with the rest of the code samples in this lesson, are not
vendor prefixed. This is intentionally un-prefixed in the interest of keeping
the code snippet small and comprehensible. For the best support across all
browsers, use vendor prefixes.

For reference, the prefixed version of the code above would look like the
following:

```
.box {
    background: #2db34a;
    -webkit-transition-property: background;
       -moz-transition-property: background;
         -o-transition-property: background;
            transition-property: background;
    -webkit-transition-duration: 1s;
       -moz-transition-duration: 1s;
         -o-transition-duration: 1s;
            transition-duration: 1s;
    -webkit-transition-timing-function: linear;
       -moz-transition-timing-function: linear;
         -o-transition-timing-function: linear;
            transition-timing-function: linear;
}

.box:hover {
  background: #ff7b29;
}
```

**Transitional Property**

The `transition-property` property determines exactly what properties will be
altered in conjunction with the other transitional properties. By default, all
of the properties within an element’s different states will be altered upon
change. However, only the properties identified within the transition-property
value will be affected by any transitions.

In the example above, the `background` property is identified in the
`transition-property` value. Here the background property is the only property
that will change over the duration of 1 second in a linear fashion. Any other
properties included when changing an element’s state, but not included within
the transition-property value, will not receive the transition behaviors as set
by the transition-duration or transition-timing-function properties.

If multiple properties need to be transitioned they may be comma separated
within the transition-property value. Additionally, the keyword value `all` may
be used to transition all properties of an element.


**Transitional Properties**

It is important to note, not all properties may be transitioned, only properties
that have an identifiable halfway point. Colors, font sizes, and the alike may
be transitioned from one value to another as they have recognizable values
in-between one another. The display property, for example, may not be
transitioned as it does not have any midpoint. A handful of the more popular
transitional properties include the following:

- `background-color`
- `background-position`
- `border-color`
- `border-width`
- `border-spacing`
- `bottom`
- `clip`
- `color`
- `crop`
- `font-size`
- `font-weight`
- `height`
- `left`
- `letter-spacing`
- `line-height`
- `margin`
- `max-height`
- `max-width`
- `min-height`
- `min-width`
- `opacity`
- `outline-color`
- `outline-offset`
- `outline-width`
- `padding`
- `right`
- `text-indent`
- `text-shadow`
- `top`
- `vertical-align`
- `visibility`
- `width`
- `word-spacing`
- `z-index`


**Transition Duration**

The duration in which a transition takes place is set using the
`transition-duration` property. The value of this property can be set using
general timing values, including seconds (s) and milliseconds (ms). These timing
values may also come in fractional measurements, `.2s` for example.

When transitioning multiple properties you can set multiple durations, one for
each property. As with the transition-property property value, multiple
durations can be declared using comma separated values. The order of these
values when identifying individual properties and durations does matter. For
example, the first property identified within the transition-property property
will match up with the first time identified within the transition-duration
property, and so forth.

If multiple properties are being transitioned with only one duration value
declared, that one value will be the duration of all the transitioned
properties.


**Transition Timing**

The `transition-timing-function` property is used to set the speed in which a
transition will move. Knowing the duration from the transition-duration
property a transition can have multiple speeds within a single duration. A few
of the more popular keyword values for the `transition-timing-function`
property include `linear`, `ease-in`, `ease-out`, and `ease-in-out`.

The `linear` keyword value identifies a transition moving in a constant speed
from one state to another. The `ease-in` value identifies a transition that
starts slowly and speeds up throughout the transition, while the `ease-out` value
identifies a transition that starts quickly and slows down throughout the
transition. The `ease-in-out` value identifies a transition that starts slowly,
speeds up in the middle, then slows down again before ending.

Each timing function has a cubic-bezier curve behind it, which can be
specifically set using the cubic-bezier(x1, y1, x2, y2) value. Additional
values include step-start, step-stop, and a uniquely identified
`steps(number_of_steps, direction)` value.

When transitioning multiple properties, you can identify multiple timing
functions. These timing function values, as with other transition property
values, may be declared as comma separated values.


**Transition Delay**

On top of declaring the transition property, duration, and timing function, you
can also set a delay with the transition-delay property. The delay sets a time
value, seconds or milliseconds, that determines how long a transition should be
stalled before executing. As with all other transition properties, to delay
numerous transitions, each delay can be declared as comma separated values.


**Shorthand Transitions**

Declaring every transition property individually can become quite intensive,
especially with vendor prefixes. Fortunately there is a shorthand property,
`transition`, capable of supporting all of these different properties and values.
Using the transition value alone, you can set every transition value in the
order of: `transition-property`, `transition-duration`, `transition-timing-function`,
and lastly `transition-delay`. Do not use commas with these values unless you are
identifying numerous transitions.

To set numerous transitions at once, set each individual group of transition
values, then use a comma to separate each additional group of transition
values.

```
.box {
  background: #2db34a;
  border-radius: 6px;
  transition: background .2s linear, border-radius 1s ease-in 1s;
}

.box:hover {
  color: #ff7b29;
  border-radius: 50%;
}
```


**Customizing Animations**

Animations also provide the ability to further customize an element’s behavior,
including the ability to declare the number of times an animation runs, as well
as the direction in which an animation completes.


**Animation Iteration**

By default, animations run their cycle once from beginning to end and then
stop. To have an animation repeat itself numerous times the
`animation-iteration-count` property may be used. Values for this property
include either an integer or the `infinite` keyword. Using an integer will
repeat the animation as many times as specified, while the `infinite` keyword
will repeat the animation indefinitely in a never ending fashion.


**Animation Direction**

You may also declare the direction an animation completes using the
`animation-direction property`. Values for this property include `normal`,
`reverse`, `alternate`, and `alternate-reverse`.

The `normal` value plays an animation as intended from beginning to end. The
`reverse` value will play the animation exactly opposite as identified within
the `@keyframes` rule, thus starting at 100% and working backwards to 0%.

The `alternate` value will play an animation forwards then backwards. Within
the keyframes that includes running forward from 0% to 100% and then backwards
from 100% to 0%. Using the `animation-iteration-count` property may limit the
number of times an animation runs both forwards and backwards. The count starts
at 1 running an animation forwards from 0% to 100%, then adds 1 running an
animation backwards from 100% to 0%. Combining for a total of 2 iterations. The
alternate value also inverses any timing functions when playing in reverse. If
an animation uses the `ease-in` value going from 0% to 100%, it then uses the
`ease-out` value going from 100% to 0%.

Lastly, the `alternate-reverse` value combines both the alternate and reverse
values, running an animation backwards then forwards. The `alternate-reverse`
value starts at 100% running to 0% and then back to 100% again.


**Animation Fill Mode**

The `animation-fill-mode` property identifies **how an element should be styled
either before, after, or before and after an animation is run**. The property
accepts four keyword values, including `none`, `forwards`, `backwards`, and
`both`.

The `none` value will not apply any styles to an element before or after an
animation has been run.

The `forwards` value will keep the styles declared within the last specified
keyframe. These styles may, however, be affected by the animation-direction and
animation-iteration-count property values, changing exactly where an animation
ends.

The `backwards` value will apply the styles within the first specified keyframe
as soon as being identified, before the animation has been run. This does
include applying those styles during any time that may be set within an
animation delay. The `backwards` value may also be affected by the
animation-direction property value.

Lastly, the `both` value will apply the behaviors from both the forwards and
backwards values.


**Shorthand Animations**

Fortunately animations, just like transitions, can be written out in a
shorthand format. This is accomplished with one `animation` property, rather
than multiple declarations. The order of values within the animation property
should be `animation-name`, `animation-duration`, `animation-timing-function`,
`animation-delay`, `animation-iteration-count`, `animation-direction`,
`animation-fill-mode`, and lastly `animation-play-state`.


Links:

- [Transitions &amp; Animations - Learn to Code Advanced HTML &amp; CSS](https://learn.shayhowe.com/advanced-html-css/transitions-animations/)

- [Zooming Background Images | CSS-Tricks - CSS-Tricks](https://css-tricks.com/zooming-background-images/)

- [SMOOTH Image Zoom on Hover Effects with CSS](https://w3bits.com/css-image-hover-zoom/)

- [Understanding CSS3 Transitions &#8211; A List Apart](http://www.alistapart.com/articles/understanding-css3-transitions/)

- [The Guide To CSS Animation: Principles and Examples — Smashing Magazine](http://coding.smashingmagazine.com/2011/09/14/the-guide-to-css-animation-principles-and-examples/)

- [CSS cubic-bezier Builder](http://www.roblaplaca.com/examples/bezierBuilder/)

- [Using CSS animations - CSS: Cascading Style Sheets | MDN](https://developer.mozilla.org/en-US/docs/CSS/Using_CSS_animations)


## Cómo hacer un árbol expandible/colapsable con CSS

Se puede hacer usando solo CSS, usando listas anidadas.

Primero, a la lista más externa le ponemos la clase `tree`. Cada elemento de la
lista estará compuesto por doe elementos,`details` y `summary`, y usaremos el
atributo `open` de details para controlar cuando el contenido se expande o se
colapsa.


Fuente: [Tree views in CSS](https://iamkate.com/code/tree-views/)

## Como posicionar texto sobre una imagen

Ponemos en un contendor comun las imagen y el texto:

```html
 <div class="container">
  <img src="img_snow_wide.jpg" alt="Snow" style="width:100%;">
  <div class="bottom-left">Bottom Left</div>
  <div class="top-left">Top Left</div>
  <div class="top-right">Top Right</div>
  <div class="bottom-right">Bottom Right</div>
  <div class="centered">Centered</div>
</div>
```

Hacemos que el contendor tenga `position` a `relative`:

```css
.container {
  position: relative;
  text-align: center;
  color: white;
}
```

Y para posicionar el texto en las esquinas o en el centro:

```
.bottom-left {
  position: absolute;
  bottom: 8px;
  left: 16px;
}

/* Top left text */
.top-left {
  position: absolute;
  top: 8px;
  left: 16px;
}

/* Top right text */
.top-right {
  position: absolute;
  top: 8px;
  right: 16px;
}

/* Bottom right text */
.bottom-right {
  position: absolute;
  bottom: 8px;
  right: 16px;
}

/* Centered text */
.centered {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```


Fuente: [How To Position Text Over an Image](https://www.w3schools.com/howto/howto_css_image_text.asp)

## El modelo Flax en CSS

El modelo **flexbox** es un modelo de composición unidimensional (Es decir, que
funciona o en modo columna o en modo fila, pero no en ambos a la vez. Para eso
usaríamos el _Grid Layout_.

Para trabajar con flex, lo primero es definir el **eje principal**, eso se hace
con la propiedad `flex-direction`. Los valores posibles son: `row`,
`row-reverse`, `column` y `column-reverse'. Los valores `row` o `row-reverse`
definen como eje principal el horizontal, `column` y `column-reverse` definen el
eje vertical como eje principal. El valor por defecto es `row`.

El **eje perpendicular** también es importante, pero no hace falta definirlo, ya
que es, como su nombre indica, perpendicular al eje principal.

Flex permite alinear y justificar tanto el en eje principal como en el eje
perpendicular, así que tenemos que tener claros cuales son.

Otro concepto relacionado con los ejes son los de de **inicio** y **fin**. Como
se quiere que el modelo sea agnóstico con respecto a los hábitos de escritura
de diferentes culturas, no se habla nunca de izquierda/derecha ni arriba/abajo,
sino de inicio y fin. Si `flex-direction` es `row`, entonces el margen inicial
del eje principal quedará a la izquierda, y el margen final a la derecha.


```
flex-direction: row

╭────────────────────────────╮
│                            │
│ [A] [B] [C]                │   
│                            │
╰────────────────────────────╯
```

Si fuera a trabajar en árabe, usaría `row-reverse` y entonces el margen inicial
del eje principal queda a la derecha y el margen final a la izquierda.

```
flex-direction: row-reverse

╭────────────────────────────╮
│                            │
│                [C] [B] [A] │   
│                            │
╰────────────────────────────╯
```


Un área del documento que contiene un _flexbox_ es llamada **contenedor flex**.
Para crear un contenedor flex, establecemos la propiedad del área del contenedor
display como `flex` o `inline-flex`. Tan pronto como hacemos esto, los hijos
directos de este contenedor se vuelven **ítems flex**. Como con todas las
propiedades de CSS, se definen algunos valores iniciales, así que cuando creemos
un contenedor flex todos los ítems flex contenidos se comportarán de la
siguiente manera.

- Los ítems se despliegan sobre una fila (la propiedad flex-direction por defecto es row)

- Los ítems empiezan desde el margen inicial sobre el eje principal

- Los ítems no se ajustan en la dimensión principal, pero se pueden contraer

- Los ítems se ajustarán para llenar el tamaño del eje cruzado

- La propiedad `flex-basis` es definida como `auto`

- La propiedad `flex-wrap` es definida como `nowrap`.

El resultado es que todos los ítems se alinearán en una solo fila, usando el
tamaño del contenedor como su tamaño en el eje principal. Si hay más ítems de
los que caben en el contenedor, estos no pasarán más abajo si no que
sobrepasarán el margen. Si los ítems tienen diferentes alturas, todos serán
ajustados en el eje cruzado para alcanzar al mayor.

```css
box {
    display: flex;
}
```

```html
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div>Three
      <br>has
      <br>extra
      <br>text
  </div>
</div>
```

El resultado será:

```
╭─────────────────────────────────────────╮
│ ╭─────╮ ╭─────╮ ╭───────╮               │   
│ │ One │ │ Two │ │ Three │               │   
│ │     │ │     │ │ has   │               │   
│ │     │ │     │ │ extra │               │   
│ │     │ │     │ │ text  │               │   
│ ╰─────╯ ╰─────╯ ╰───────╯               │
╰─────────────────────────────────────────╯
```

Como se comento antes, si los elementos exeden el tamaño del contenedor en el
eje principal, por defecto sequiran en la misma línea (o columna), pero podemos
hacer que se repartan en varias líneas/columnas usando la propiedad `flex-wrap`
con el valor `wrap` (El valor por defecto es `nowrap`).

### La abreviatura flex-flow

Se pueden combinar las propiedades `flex-direction` y `flex-wrap` en la
abreviatura `flex-flow` . El primer valor especificado es `flex-direction` y el
segundo, `flex-wrap`.


### Propiedades aplicadas a los ítems flex

Para obtener más control sobre los ítems flex disponemos de tres propiedades:

- `flex-grow`

- `flex-shrink`

- `flex-basis`

Antes de darle sentido a estas propiedades debemos considerar el concepto de
**espacio disponible**. Lo que hacemos cuando cambiamos el valor de alguna de
estas propiedades es cambiar la forma que se distribuye el espacio disponible
entre nuestros ítems. Este concepto de espacio disponible es también importante
cuando veamos la alineación de ítems.

Si tenemos tres ítems con un ancho de 100 pixeles en un contenedor de 500
pixeles de ancho, entonces el espacio que se necesita para colocar nuestros
ítems es de 300 pixeles. Esto deja 200 pixeles de espacio disponible. Si no
cambiamos los valores iniciales, flexbox colocará ese espacio después
del último ítem.

```
╭──────────────────────────────────────────╮
│ ╭──────╮ ╭──────╮ ╭──────╮               │   
│ │ A    │ │ B    │ │ C    │               │   
│ ╰──────╯ ╰──────╯ ╰──────╯               │
╰──────────────────────────────────────────╯
```

La propiedad **flex-basis** define el tamaño de un ítem en términos del espacio
que deja como espacio disponible. El valor inicial de esta propiedad es `auto`; en
este caso el navegador revisa si los ítems definen un tamaño. En el ejemplo anterior,
todos los ítems tienen un ancho de 100 pixeles así que este es usado como `flex-basis`.
Si los ítems no tiene un tamaño entonces el **tamaño de su contenido** es usado como
`flex-basis`. 


Con la propiedad `flex-grow` definida como un entero positivo, los ítems flex pueden
crecer en el eje principal a partir de `flex-basis`. Esto hará que el ítem se ajuste
y tome todo el espacio disponible del eje, o una proporción del espacio disponible
si otro ítem también puede crecer.

Si le damos a todos los ítems del ejemplo anterior un valor `flex-grow` de $1$ entonces
el espacio disponible en el contenedor flex será compartido equitativamente entre estos
ítems y se ajustarán para llenar el contenedor sobre el eje principal.

También podemos usar `flex-grow` para distribuir el espacio proporcionalmente. Si
otorgamos al primer ítem un valor `flex-grow` de $2$ y a los otros un valor de $1$,
entonces el primer elemento ocupara el mismo espacio que los otros dos.

Así como la propiedad `flex-grow` se encarga de añadir espacio sobre el eje
principal, la propiedad `flex-shrink` controla como se contrae. Si no contamos
con suficiente espacio en el contenedor para colocar los ítems y `flex-shrink`
posee un valor entero positivo, el ítem puede contraerse a partir de flex-basis.
Así como podemos asignar diferentes valores de `flex-grow` con el fin que un ítem
se expanda más que otros, un ítem con un valor más alto de `flex-shrink` se contraerá
más que sus hermanos que poseen valores menores.

Hay que considerar el tamaño mínimo del ítem para poder determine un valor de
contracción, por lo que `flex-shrink` puede comportarse de forma menos
consistentemente que `flex-grow`.

Es raro ver la propiedades `flex-grow`, `flex-shrink` y `flex-basis`
usadas individualmente ya que han sido combinadas en la abreviación `flex`,
que permite establecer los valores en este orden: `flex-grow`, `flex-shrink` y
`flex-basis`.



Una característica clave de flexbox es la capacidad de **alinear y justificar
ítems sobre los ejes principal y cruzado**, y distribuir el espacio entre los
ítems flex. La propiedad `align-items` alineará los ítems sobre el eje cruzado,
mientras que `justify-content` los alinea sobre el eje principal.

El valor inicial para `align-items` es `stretch`, razón por la cual los ítems
se ajustan por defecto a la altura del más alto. En efecto se ajustan para
llenar el contenedor flex — el ítem más alto define la altura de este.

En cambio usaremos `flex-start` para que los ítems se
alineen al comienzo del contenedor flex, `flex-end` para alinearlos al
final, o `center` para alinearlos al centro. 

Los valores posibles de `align-items` son:

- `stretch`

- `flex-start`

- `flex-end`

- `center`

La propiedad `justify-content` sirve para alinear los ítems en el eje
principa. El valor inicial es `flex-start` que alineará los ítems al
inicio del margen del contenedor, pero también se podría definir
como `flex-end` para alinearlos al final, o `center` para alinearlos al
centro.

Los valores de `justify-content` son:

- `space-evenly`

- `flex-start`

- `flex-end`

- `center`

- `space-around`

- `space-between`


También podemos usar `space-between` para tomar todo el espacio sobrante
después de que los ítems hayan sido colocados, y distribuir de forma
pareja los ítems para que haya un espacio equitativo entre cada ítem. O
bien, usamos el valor `space-around` para crear un espacio equitativo
a la derecha e izquierda de cada ítem.
