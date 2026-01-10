Kivy
========================================================================

Sobre :index:`kivy`
------------------------------------------------------------------------

**Kivy** es una biblioteca de software de código abierto para el
desarrollo rápido  de aplicaciones equipadas con nuevas interfaces de
usuario, como las aplicaciones multitáctiles.

Cómo hacer un hola, mundo en kivy
------------------------------------------------------------------------

Para hacer una aplicación Kivy, tenemos que crear una clase que derive
de ``kivy.app.App``. Es recomendable, por razones que veremos más
adelante, que el nombre de nuestra clase termine en ``App``.

Podemos **declarar un método** ``build`` que nos debería devolver el árbol de
componentes que formarían la estructura de la ventana principal de la
aplicación. Como es un ejemplo sencillo, aquí solo devolvemos un control de
tipo ``kivy.uix.button.Button``.

Para ejecutar la aplicación, primero **creamos una instancia** de nuestra clase
derivada de ``App``, y luego llamamos a su método ``run()``.

.. code-block:: python
   :emphasize-lines: 4,6,11

    from kivy.app import App
    from kivy.uix.button import Button
    
    class MainApp(App):
    
        def build(self):
            return Button(text="Hello World")
    
    
    if __name__ == '__main__':
        app = MainApp(title="Hola, mundo Kivy") 
        app.run()


Cómo cambiar al tamaño de la ventana
------------------------------------------------------------------------

Hay dos maneras:

-  Antes de que se cree la ventana

.. code:: python

    import kivy
    from kivy.config import Config

    kivy.require('1.9.0')
    Config.set('graphics', 'width', '200')
    Config.set('graphics', 'height', '200')
    Config.write()


Ojo, la última línea hará el cambio **permanente**, configurando así el
tamaño por defecto de todas las ventanas kivy.

-  Dinámicamente, después de que se cree la ventana

.. code:: python

    from kivy.core.window import Window
    Window.size = (300, 100)

Fuente: `Kivy How to change window size`_

.. _Kivy How to change window size: https://stackoverflow.com/questions/14014955/kivy-how-to-change-window-size
