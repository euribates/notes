---
title: Notas sobre kivy
---

## Sobre kivy

## Cómo cambier al tamaño de la ventana

Hay dos maneras:

- Antes de que se cree la ventana

```python
import kivy
kivy.require('1.9.0')

from kivy.config import Config
Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')
```

- Dinámicamente, despues de que se cree la ventana

```python
from kivy.core.window import Window
Window.size = (300, 100)
```

