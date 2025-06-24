## Notes on FontAsesome

### Stacking icons

For this, you just need to add `fa-stack` class to the parent element, and inside it just regularly put icons, like this

    <span class="fa-stack fa-2x">
    <i class="fas fa-square fa-stack-2x"></i>
    <i class="fab fa-twitter fa-stack-1x fa-inverse"></i>
    </span>

### Animating icons

Also by only adding a simple class, FA provides you some basic animations to add to your icons, such
as spin(`fa-spin`) and pulse(`fa-pulse`):

    <i class="fas fa-spinner fa-spin"></i>
    <i class="fas fa-spinner fa-pulse"></i>

### Rotating icons

You can also rotate your icons without the use of CSS's transform property, only adding one more
class:

    <div class="fa-4x">
        <i class="fas fa-snowboarding"></i>
        <i class="fas fa-snowboarding fa-rotate-90"></i>
        <i class="fas fa-snowboarding fa-rotate-180"></i>
        <i class="fas fa-snowboarding fa-rotate-270"></i>
        <i class="fas fa-snowboarding fa-flip-horizontal"></i>
        <i class="fas fa-snowboarding fa-flip-vertical"></i>
        <i class="fas fa-snowboarding fa-flip-both"></i>
    </div>

### Scaling icons

Scaling affects icon size without changing or moving the container. To scale icons up or down, use
`grow-#` and `shrink-#` with any arbitrary value, including decimals.

So you can change the size of an icon, without affecting the parent element. Here's an example:

    <div class="fa-4x">
    <i class="fas fa-seedling" data-fa-transform="shrink-8" style="background:MistyRose"></i>
    <i class="fas fa-seedling" style="background:MistyRose"></i>
    <i class="fas fa-seedling" data-fa-transform="grow-6" style="background:MistyRose"></i>
    </div>

### Text over icons

You can add a text over an icon.


    <span class="fa-layers fa-fw" style="background:MistyRose">
        <i class="fas fa-calendar"></i>
        <span class="fa-layers-text fa-inverse" data-fa-transform="shrink-8 down-3" style="font-weight:900">27</span>
    </span>

    <span class="fa-layers fa-fw" style="background:MistyRose">
        <i class="fas fa-certificate"></i>
        <span class="fa-layers-text fa-inverse" data-fa-transform="shrink-11.5 rotate--30" style="font-weight:900">NEW</span>
    </span>

You need to wrap the icon into a `span` for example, and add the `fa-layers` class to it.
Inside it add the icon, and another span element, which contains the text, with the `fa-layers-text` class.

### Adding counter to icons

You can also add a counter to an icon. Good example is to display the number of messages received on an envelope icon.
Alt Text

    <span class="fa-layers fa-fw" style="background:MistyRose">
        <i class="fas fa-envelope"></i>
        <span class="fa-layers-counter" style="background:Tomato">1,419</span>
    </span>

It works the same way as putting text over an icon, but instead of `fa-layers-text`, you need to add
the `fa-layers-counter` class.

The counter is positioned at the top-right corner by default, but you can position it elsewhere too:
Can be positioned with `fa-layers-bottom-left`, `fa-layers-bottom-right`, `fa-layers-top-left` and the
default `fa-layers-top-right`. Overflow text is truncated with an ellipsis.

Source: <https://dev.to/weeb/font-awesome-guide-and-useful-tricks-you-might-ve-not-known-about-until-now-o15>
