---
title: Notas sobre SASS (_Syntactically awesome style sheets_)
---

## Introduction to SCSS

**Sass** (Syntactically awesome style sheets) is a style sheet language
initially designed by Hampton Catlin and developed by Natalie
Weizenbaum. Sass is a preprocessor scripting language that is
interpreted or compiled into Cascading Style Sheets (CSS). SassScript is
the scripting language itself.

Sass includes **two type extension**: `.scss` and `.sass`. The `.scss`
file extension and is fully compliant with CSS syntax and `.sass` is not
fully compliant with CSS syntax, but it\'s quicker to write.

## Variables

We can define an element in a variable and interpolate it inside our
Sass code. This is useful when you keep your modules in separate files.
The most common uses of variables are color palettes, storing
information like font declarations, sizes, and media queries, that can
be used in separate stylesheets.

For Example:

```sass
$body: #226666;
$primary-color: #403075;
$footer: #AA8439;
$font-stack: Helvetica, sans-serif;
```

Las palabras que empiezan con el símbolo `$` son variables Sass. Pueden ser
usadas desde otras partes del fichero:

```
body {
    background: $body;
    font: $font-stack;
}

.header {
    color: $primary-color;
}

a {
    color: $primary-color;
}
```

## Nesting With SCSS

**Nesting** is one most popular features of SCSS. With nesting, you can add
classes between the braces of a declaration. SCSS will compile and
handle the selectors quite intuitively. You can even use the "&"
character to get a reference to the parent selector.

Example:

```sass
h2 {
    color: navy;

    small {
        color: red;
    }
}
```

Produce:

```
h2 {
    color: navy;
}
h2 small {
    color: red;
}
```


## Mixins and Extends

Mixins and extends are powerful features that help to avoid a lot of
repetition. With mixins, you can make parameterized CSS declarations and
reuse them throughout your stylesheets.

Let's say you have a box and you want to give the box rounded corners:

```
@mixin border-radius($round) {
-webkit-border-radius: $round;
    -moz-border-radius: $round;
    -ms-border-radius: $round;
        border-radius: $round;
}

/*Just use '@include' directive to apply mixin */

.box { @include border-radius(15px); }
```

Notice the `@mixin` directive at the top. It has been given the name
`border-radius` and uses the variable `$round` as its parameter. This
variable is used to set the radius value for each element. After that,
the `@include` directive is called with the parameter value, i.e 15px.

Here is the corresponding CSS:

```css
.box {
    -webkit-border-radius: 15px;
    -moz-border-radius: 15px;
    -ms-border-radius: 15px;
    border-radius: 15px;
}
```

If you want to add different sizes for each corner while including the
directive, that can be also done; you just need to specify it as
follows:

```sass
.box { @include border-radius(15px 10px 5px 0px); }
```


## Extend

The `@extend` directive has been called one of Sass's most powerful
features. This directive allows you to share properties from one
selector to another.

Let's say you declare a common class containing properties:

```css
.box {
    margin: 10px;
    padding: 10px;  
    border: 2px solid blue;
}
```

And now you want two similar boxes with the same properties, but with
different border colors:

```css
.box-red {
    @extend .box;
    border-color: red;
}

.box-yellow {
    @extend .box;
    border-color: yellow;
}
```

Let's see the full SCSS we need to get the desired output:

```sass
.box, .box-red, .box-yellow {
    margin: 1em;
    padding: 1em;
    border: 2px solid red;
}

.box-red {
    border-color: red;
}

.box-yellow {
    border-color: yellow;
}
```


## Import

`@import` will be handled by Sass and all our CSS and SCSS files will be
compiled to a single file that will end up on our live site. You can
create partial Sass files that contain little snippets of CSS that you
can include in other Sass files, i.e. `variable.scss`, `fonts.scss`,
`buttons.scss`, etc., and then we can include all SCSS files in the
`main/style.scss` folder. If you don\'t import the partial files, then
reusable components like mixin and variable will not work.

Let's say you have created multiple files and that you need to import
them into the main.scss file:

```sass
@import “variables”;
@import “fonts”;
@import “base”;
@import “buttons”;
@import “layout”;
``

The only drawback is that a separate HTTP request gets triggered for
each CSS file that you are importing.

Fuente: [Introduction to SCSS](https://dzone.com/articles/introduction-of-scss)
