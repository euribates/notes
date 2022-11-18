---
title: Notas sobre Restructured Text
---

## Sobre ReStructeredText

## Matemáticas en reStructuredText con LaTeX

Since version 0.8 it is supported natively: You shouldn't use any
workaround anymore. The syntax is also very simple. It is the same as
latex math, but without the enclosing `$`. So you can
simply write the following for a math block:

```latex
.. math::
    \frac{ \sum_{t=0}^{N}f(t,k) }{N}
```

Or if you want to write inline you can use this:

```latex
    :math:`\frac{ \sum_{t=0}^{N}f(t,k) }{N}`
```

notice the delimiting backticks there.

UPDATE: in newer versions it seems to be necessary to use a
double-backslash for the math elements, so it's `\\frac`
not `\frac`.

Fuente: <https://stackoverflow.com/questions/3610551/math-in-restructuredtext-with-latex>
