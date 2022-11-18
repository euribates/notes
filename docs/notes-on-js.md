---
title: Notes on javascript
---

## Cómo convertir de string a entero

Usa la función `parseInt`.


## Arrow functions expressions

An **arrow function expression** is a compact alternative to a traditional
function expression, but **is limited** and can't be used in all situations.

Differences & Limitations:

- Does not have its own bindings to `this` or `super`, and should not be used as methods.
- Does not have `new.target` keyword.
- Not suitable for `call`, `apply` and `bind` methods, which generally rely on establishing a scope.
- Can not be used as constructors.
- Can not use `yield`, within its body.

Let's decompose a traditional function down to the simplest arrow function
step-by-step. Notice each step along the way is a valid "arrow function".

```js
// Traditional Function
function (a) { return a + 100; }

// 1. Remove the word "function" and place arrow between the argument and opening body bracket

(a) => { return a + 100; }

// 2. Remove the body braces and word "return" -- the return is implied.

(a) => a + 100;

// 3. Remove the argument parentheses (Only works if decalres one single parameter)

a => a + 100;
```

As shown above, the `{` braces `}` and `(` parentheses `)` and `return` are required in some cases.

For example, if you have **multiple arguments or no arguments**, you'll need to
**re-introduce parentheses** around the arguments

Likewise, **if the body requires additional lines of processing**, you'll need
to **re-introduce braces PLUS the `return`** [because arrow functions do not magically
guess what or when you want to "return" (and asuming it was the last line was
too simple, it seems)].

Source: [MDN Web Docs: Arrow function expressions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions)


## Using console for JavaScript debugging

Using `console.log()` for JavaScript debugging is the most common practice. But, there is more...

The most common Console methods are:

- `console.log()` – For general output of logging information.
- `console.info()` – Informative logging.
- `console.debug()` – A message to the console with the log level debug.
- `console.warn()` – A warning message.
- `console.error()` – An error message.

### Adding styles

The `console.log` output can be styled in DevTools using the CSS format specifier.

```js
    console.log('%c This is a fancy message', 'color: white;font-size:2em;background:teal')
```

Notice the `%c` at the beginning ot the message.

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


