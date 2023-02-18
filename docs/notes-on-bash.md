---
title: Notas sobre bash
---

## Introducción a bash

**Bash** (_Bourne-again shell_) es una interfaz de usuario de línea de comandos, específicamente un _shell_ de Unix; así como un lenguaje de scripting. Fue escrito originalmente por Brian Fox para el sistema operativo GNU, y pretendía ser el reemplazo de software libre del shell Bourne.

## Recomendaciones para scripts en bash

- Usar `bash`. Otros _shells_ como `zsh` o `fish` dificultan que el script se
  pueda ejecutar en otras máquinas, mientras que `bash` está instalado en
  practicamente cualquier sistema.

- La primera línea debe ser:
    
    ```
    #!/usr/bin/env bash
    ```

- Usar la extensión `.sh` (o `.bash`)

- Usa `set -o errexit` al principio del _script_. De esta manera `bash` termina
  si se produce un error en vez de intentar continuar con el resto del
  _script_.

- Usa `set -o nounset`. Esto hará que el _script_ falle si se intenta acceder a
  una variable que no esté definida. Si se quiere acceder a una variable que
  puede estar definida o no, usar `${VARNAME-}` en vez de `$VARNAME`, y listo.

- Usa `set -o xtrace`, con una comprobación previa de la variable `$TRACE`

```
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi
```

  Esto ayuda mucho a la hora de depurar un _script_, y se puede ejecutar
  el mismo en modo `TRACE ON` ejecutandolo como `TRACE=1 ./script.sh`.

- Usar siempre `[[` y `]]` para la comprobación de condiciones, en vez de `[` y
  `]` o `test`. Las marcas `[[` y `]]` son _keywords_ de `bash`, y es más
  potente que los otras dos alternativas.

- Acepta diferentes maneras de pedir ayuda para ejecutar el _script_, por
  ejemplo `-h`, `--help`

- Escribir los mensajes de error a la salida estándar de errores.

```
echo 'Something unexpected happened' >&2
```

- Si fuera apropiado (Casi siempre es así), cambiar al directorio del _script_
  al principio. En la mayoría de los casos debería bastar con:

```
cd "$(dirname "$0")"
```
    
La siguiente plantilla puede servir como primer paso:

```
#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
set -o allexport; source .env; set +o allexport
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
    echo 'Usage: ./script.sh arg-one arg-two

This is an awesome bash script to make your life better.

'
    exit
fi

cd "$(dirname "$0")"

main() {
    echo do awesome stuff
}

main "$@"
```

Fuente: [Shell Script Best Practices — The Sharat's](https://sharats.me/posts/shell-script-best-practices/)

## Cómo borrar una variable de entorno 

Con la orden `unset`:

```shell
$ unset AUTH_TOKEN
```

## How do I clear Bash's cache of paths to executables?

The ``bash`` shell does cache the full path to a command. You can verify that
the command you are trying to execute is hashed with the type command:

```shell
type npx
npx is hashed (/usr/local/bin/npx)
```

To clear the entire cache:

```shell
hash -r
```

Or just one entry:

```
hash -d npx
```

For additional information, consult `help hash` and `man bash`.

Source: [How do I clear Bash's cache of paths to executables? -
Stackoverflow](https://unix.stackexchange.com/questions/5609/how-do-i-clear-bashs-cache-of-paths-to-executables)

## Cómo exportar las funciones definidas en el fichero `.bashrc`

Podemos exportar las funciones para que puedan ser usadas por cualquiera,
usando la formula `export -f <functionname>`:

```shell
function hello() {
   echo "Hello, $1!"
}

export -f hello
```


## Cómo cambiar el directorio actual al mismo del script

En general, hay dos tipos de script escritos en bash:

- Herramientas o utilidades de sistema que deben trabajar sore el directorio
  actual

- Herramientas porpias de proyectos que modifican ficheros relativos
  a la propia ubicación del proyecto.

Para este segundo tipo, es útil cambiar al directorio donde está el script.
Esto se puede conseguir con el siguiente comando:

```bash
cd "$(dirname "$(readlink -f "$0")")"
```

Esta orden está compuesta por tres:

1) `readlink -f "$0"` determina el _path_ del _script_ ejecutado (`$0`)

2) `dirname` convierte el _path_ anterior (que apunta al script) a otro que
apunta al directorio que contiene el _script_.

3) `cd` cambia el directorio actual al directorio evaluado en el paso anterior.

Fuente: [Getting started with bash: Change to the Directory of the Script](https://riptutorial.com/bash/example/30284/change-to-the-directory-of-the-script)


## Definir variables de entorno en un fichero bash a partir de un fichero `.env`

This is the way:

```bash
set -o allexport; source .env; set +o allexport
```

Ahora se puede leer un valor definido en ese fichero `.env`, e incluso utilizar
un valor por defecto si no estuviera definido:

```bash
# Activar el entorno virtual
VIRTUAL_ENV="${VIRTUAL_ENV:-acl}"
echo "Working on $VIRTUAL_ENV"
```

Fuente: [Load environment variables from dotenv/.env file in
Bash](https://gist.github.com/mihow/9c7f559807069a03e302605691f85572)


## Assign default values in bash scripting

You can use something called **bash parameter expansion** to accomplish this.

To get the assigned value, or `default` if it's missing:

```shell
FOO="${VARIABLE:-default}"  # If variable not set or null, use default.
```

Or to assign default to `VARIABLE` at the same time:

```shell
FOO="${VARIABLE:=default}"  # If variable not set or null, set it to default.
```

- Source: [Stack Overflow - Assigning default values to shell variables with a single command in bash](https://stackoverflow.com/questions/2013547/assigning-default-values-to-shell-variables-with-a-single-command-in-bash)


## Cómo personalizar bash

In order to customize your shell with aliases, colors, and set a custom prompt,
start by adding a `.bashrc` and a `.bash_profile` file.

The `.bash_profile` is executed for **login shells** and the `.bashrc` is
executed for **interactive non-login shells**. When you login using a username
and password to a server/virtual machine (vm) via ssh or directly on a machine,
the `.bash_profile` is executed to configure the shell before the initial
command prompt appears. If you have already logged into the server/vm and open
a new terminal window, then the `.bashrc` is executed before the command prompt
appears. The `.bashrc` is also run when you switch back from another shell (i.e
ksh or zsh) into bash.

Check out the following links for more information:

-   [Bash Scripting Tutorial](https://ryanstutorials.net/bash-scripting-tutorial/)
-   [Bash scripting tutorial for beginners](https://linuxconfig.org/bash-scripting-tutorial-for-beginners)
-   [The Shell Scripting Tutorial](https://www.shellscript.sh/)
