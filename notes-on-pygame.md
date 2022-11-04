---
title: Notes on PyGame
---

## Introducción a `PyGame`


**[PyGame](http://pygame.org/)** es un conjunto de librerías para python orientadas
a hacer juegos. Internamente usa unas librerías escritas en C/C++ llamadas
[SDL](http://www.libsdl.org/) (*Simple DirectMedia Layer*), que dan acceso a
bajo nivel a los sistemas de audio, teclado, ratón, joystick y gráficos. Tanto
SDL como PyGame funcionan en diferentes plataformas: Windows, Mac OS X y Linux,
entre otras.

## Cómo gestionar el evento de salida en PyGame

Podemos usar el siguiete código para salir del programa si el usuario ha
cerrado la ventana desde el S.O.:
```
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
```

### Cómo mantener un valor constante de FPS en PyGame

En PyGame se usa una variable de tipo reloj, llamada `pygame.time.Clock`. Esta
variable nos permite mantener un FPS fijo independientemente de la máquina.

El mecanismo es el siguiente: para garantizar que el programa no se ejecute
demasiado rápido, se intercalan breves pausas en cada iteración del bucle del
juego. Al final de cada iteración, justo después de la llamada a `flip` o
`update`, se llama al método `tick()` de la variable reloj.

La primera vez que se llame a `tick` no hará nada, pero toma nota del momento
en que se le ha llamado. La segunda vez calcula la diferencia con el momento de
la llamada anterior y comprueba si va demasiado rápido. Si es así, ejecuta una
pausa de tanto tiempo como haga falta para garantizar los FPS que se le pasan
como parámetro.

Por ejemplo, un FPS de 50 significa que hay que generar una imagen nueva
cada 20 milisegundos. Si entre una iteración y la anterior han pasado
solo 5 milisegundos, la llamada a `tick()` hace una pausa de 15
milisegundos para alcanzar los 20 que hacen falta para mantener un rango
constante de 50 FPS. Evidentemente, si la iteración ha llevado más de
20, no se realiza pausa de ningún tipo, y el ratio de FPS bajará.

A efectos prácticos, lo único que hay que recordar es que tenemos que
crear un objeto reloj, del tipo `pygame.time.Clock` antes de entrar en
el bucle, y dentro de este, al final, poner una llamada al método `tick`
pasando el número de FPS que queremos.


