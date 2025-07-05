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
Config.write()
```

Ojo, la última línea hará el cambio permanente, configurando así el tamaño por
defecto de todas las ventanas kivy.

- Dinámicamente, despues de que se cree la ventana

```python
from kivy.core.window import Window
Window.size = (300, 100)
```

Fuente: [python - Kivy: How to change window size? - Stack Overflow](https://stackoverflow.com/questions/14014955/kivy-how-to-change-window-size)
