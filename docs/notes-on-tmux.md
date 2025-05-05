---
title: Notes on Tmux
---

## Sobre TMux

Un buen artículo de introducción a Tmux: 
[Getting started with tmux | ITTavern.com](https://ittavern.com/getting-started-with-tmux/)

Conceptos básicos:

- Sesiones / Ventanas / paneles. Las sesiones pueden estar en primer plano
  (_attached_) o en segundo plano (_detached_). Aun estando en segundo plano,
  los procesos ejecutándose en ellas siguen funcionando. Cada sesión puede tener
  múltiples ventanas, y cada ventana puede tener múltiples paneles, que son
  divisiones de la pantalla.

- El prefijo o tecla de control o **_lead_** por defecto es ++ctrl-b++, y es la
  secuencia que se usa casi siempre para darle ordenes a Tmux. En mucha
  documentación se hará referencia a `Lead` o `Prefix`. Se puede cambiar
  a otra configuración con el comando `set`. Por ejemplo, para cambiarlo a
  ++ctrl+s++, habría que hacer:

    ```
    Prefix + `:set -g prefix C-s`
    ```

  El cambio sera temporal, y  durará lo que la sesión en curso. Para hacerlo
  fijo ver [Cómo configurar Tmux](#como-configurar-tmux).


## Cómo configurar Tmux

En Linux, el fichero de configuración está normalmente en `~/.tmux.conf`.

Después de hacer un cambio en la configuración, si estamos dentro de Tmux, no
hace falta salir y volver a entrar para que los cambios se apliquen, podemos
hacer [Prefix] + `:source-file ~/.tmux.conf`.


## Cómo renombrar las sesions de Tmux

Usar la combinación de teclas: ++ctrl+b++ + `$`.


## Cómo trabajar y modificar los paneles

Estos son los comandos más usados:

- `Ctrl+b` : Dividir en dos paneles horizontales.

- `Ctrl+b %` : Dividor en dos panales verticales.

- `Ctrl+b arrow key` : Cambiar a otro panel.

- Pulsar `Ctrl+b` y, manteniendola pulsada, usar las flechas para cambier el
  tamaño del panel actual.

- `Ctrl+b c` : (C)rear una ventana nueva

- `Ctrl+b n` : Pasar a la ventana siguiente (_Next_).

- `Ctrl+b p` : Pasar a la ventana (P)revia.

Other thing worth knowing is that **scrolling is enabled** by pressing `Ctrl+b
PgUp/PgDown`. In fact, it enables the copy mode, which can also be done by
pressing `Ctrl+b [`. When in copy mode, you can use `PgUp/PgDown` and arrow keys to
scroll through the terminal contents. To (q)uit the copy mode, simply press the
`q` key.

Source: [tmux Tutorial — Split Terminal Windows Easily - Lukasz Wrobel](https://lukaszwrobel.pl/blog/tmux-tutorial-split-terminal-windows-easily/)

## Cómo crear una sesión en Tmux

Para crear una nueva sesión y pasarla a primer plano, simplemente ejecutamos:

```shell
tmux
```

O:

```shell
tmux new
```

Podemos asignarle un nombre a la sesión cuando la creamos, con el flag `-s`. El
siguiente ejemplo crea una sesión llamada `webserver`:

```shell
tmux new -s webserver
```

Aparte de eso, una vez creada siempre se le puede cambiar el nombre con
[Prefix] - `$`.

Una vez dentro de una sesión, veremos que aparece una barra verde en la última
línea de la terminal.


## Cómo recuperar una sesión después de un corte de comunicación

Una vez que la conexión se ha restablecido, volvemos a conectarnos
y volvemos a activar o pasar a primer plano alguna de las sesiones
que siguen activas:

Caso de ejemplo:

```shell
$ tmux
$ make <something big>
......
Connection fails for some reason
Reconect

$ tmux ls
0: 1 windows (created Tue Aug 23 12:39:52 2011) [103x30]

$ tmux attach -t 0
Back in the tmux sesion
```

## Cómo pasar una sesión Tmux a segundo plano. 

Hay que pulsar ++ctrl+b++ and ++d++. Volveremos a una terminal normal, 
y nos mostrará un mensaje como:

```shell
[detached (from session 0)]
```

Pero las sesiones en segundo plano siguen trabajando. Podemos obtener un listado
de las sesiones con `tmux ls`. Para volver a la sesión, `tmux attach`.


## Cómo listar las sesiones Tmux disponibles

Solo hay que llamar al comando `tmux` con la orden `ls`:

```shell
tmux ls
```

## Cómo volver a conectar con una sesión en segundo plano

Usando la orden `attach` volvemos a la ultima sesión activa:

```shell
tmux attach
```

O especificando el nombre de la sesión con `-t` para activar esa sesión en
concreto:

```shell
tmux attach -t webserver
```

La orden `attach` se puede abreviar a `a`:

```shell
tmux a -t sebserver
```

Fuente:

- [Tmux Command Examples To Manage Multiple Terminal Sessions](https://ostechnix.com/tmux-command-examples-to-manage-multiple-terminal-sessions/)
