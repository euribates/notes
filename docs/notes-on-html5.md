---
title: Notas sobre Html 5
tags:
    - html
    - dev
    - web
---

## Tipos de controles de entrada (input)

Estos son los valores aceptados para el parámetro `type` de la etiqueta `input`:

- `button`: Un botón

- `checkbox`: Un cuadro de opción (opciones múltiples)

- `color`: La entrada es un color

- `date`: La entrada es una fecha. Dependiendo del navegador, este
  mostrará un diálogo modal para introducir la fecha.

- `datetime-local`: La entrada es una fecha, **sin** especificar el
  [huso horario](https://es.wikipedia.org/wiki/Huso_horario) local.

- `email`: Un correo electrónico.

- `file`: Un archivo. Hay que recordar que si usamos un campo de este
  tipo, especialmente para ficheros binarios, debemos especificar el
  atributo `content-encoding` con el valor `multipart/form-data` en el
  elemento `form`.

- `hidden`: Campo oculto

- `image`: Un fichero de tipo imagen. Véase el comentario en el tipo `file`.

- `month`: Para especificar un mes **y año**.

- `number`: Para especificar un número. Acepta los parámetros opcionales
  `min` y `max` para indicar los valores mínimo y máximo admisibles.

- `password`: Un campo para contraseñas, protegido contra miradas de
  terceros.

- `radio`: Un circulo de opción (opciones mutuamente excluyentes).

- `range`: Un valor, definido de forma aproximada mediante un slider,
  dentro de un rango de valores numéricos. Inicialmente el rango va de 0
  a 100, pero se pueden definir ambos límites con los parámetros
  opcionales `min` y `max`.

- `reset`: Limpia todos los campos del formulario.

- `search`: Un parámetro de búsqueda.

- `submit`: Un botón de envío de un formulario.

- `tel`: Un teléfono.

- `text`: Texto normal.

- `time`: 

- `url`: Una URL. El _browser_ no verifica que la dirección sea válida,
  pero si que este bien construida.

- `week`: Permite seleccionar una semana **y un año**. 


