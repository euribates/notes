---
title: Notes on CSS
---

### CSS Variables (Custom Properties)

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



### Animations and transitions

With CSS3 transitions you have the potential to alter the appearance and
behavior of an element whenever a state change occurs, such as when it is
**hovered over**, **focused on**, **active**, or **targeted**.

Animations within CSS3 allow the appearance and behavior of an element to be
altered in multiple keyframes. **Transitions** provide a change from one state
to another, while **animations** can set multiple points of transition upon
different keyframes.


### Transitions

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
