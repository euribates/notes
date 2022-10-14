## Notes on Vue.js

### React for Vue developers

- <https://sebastiandedeyne.com/react-for-vue-developers/>

### How to change the delimiters

To change delimiters in vue.js, use like this

    new Vue({
        delimiters: ['{%', '%}'],
    }
    
### Vue.js Intro

At the core of Vue.js is a system that enables us to declaratively render data
to the DOM using straightforward template syntax:

```html
<div id="counter">
  Counter: {{ counter }}
</div>
```

```js
const Counter = {
  data() {
    return {
      counter: 0
    }
  }
}

Vue.createApp(Counter).mount('#counter')
```

The data and the DOM are now linked, and everything is now reactive. How do we
know? Take a look at the example below where counter property increments every
second and you will see how rendered DOM changes:

```js
const CounterApp = {
  data() {
    return {
      counter: 0
    }
  },
  mounted() {
    setInterval(() => {
      this.counter++
    }, 1000)
  }
}
```

### Prop / Event Fallthrough

You can set props (and listen to events) on a component which you haven't
registered inside of that component. For example, this button component (which
might exist to set up a button with some default styling) has no special props
that would be registered:

```vue
BaseButton.vue

<template>  
  <button>
    <slot></slot>
  </button>
</template>
 
<script>
export default {}
</script>
```

Yet, you can use it like this:

```html
<base-button type="submit" @click="doSomething">Click me</base-button>
```

Neither the type `prop` nor a custom `click` event are defined or used in the
component. This code works, though, because Vue has built-in support for prop
(and event) "fallthrough".

Props and events added on a custom component tag automatically fall through to
the root component in the template of that component. In the above example,
`type` and `@click` get added to the `<button>` in the BaseButton component.

You can get access to these fallthrough props on a built-in `$attrs` property
(e.g. `this.$attrs`).

This can be handy to build "utility" or pure presentational components where
you don't want to define all props and events individually.

You can learn more about this behavior here: [https://v3.vuejs.org/guide/component-attrs.html](https://v3.vuejs.org/guide/component-attrs.html)


### Binding All Props on a Component

If you have this component (`UserData.vue`):

```html
<template>
  <h2>{‌{ firstname }} {‌{ lastname }}</h2>
</template>
 
<script>
  export default {
    props: ['firstname', 'lastname']
  }
</script>
```

You could use it like this:

```html
<template>
  <user-data :firstname="person.firstname" :lastname="person.lastname"></user-data>
</template>
 
<script>
  export default {
    data() {
      return {
        person: { firstname: 'Max', lastname: 'Schwarz' }
      };
    }
  }
</script>
```

But if you have an object which holds the props you want to set as properties,
you can also shorten the code a bit:

```
<template>
  <user-data v-bind="person"></user-data>
</template>
 
<script>
  export default {
    data() {
      return {
        person: { firstname: 'Max', lastname: 'Schwarz' }
      };
    }
  }
</script>
```

With `v-bind="person"` you pass all key-value pairs inside of `person` as props
to the component. That of course requires `person` to be a JavaScript object.
This is purely optional but it's a little convenience feature that could be
helpful.
