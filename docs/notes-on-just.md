---
title: Notes on just
---

## Qué es just

**Just** es una forma cómoda de poder ejecutar tareas habituales asociadas a un
proyecto. Una un fichero de recetas con un formato similar el de `make`.


### Recetas (Recipes)

Just usa un fichero donde se definen las ordenes a ejecutar, que se conocen
normalmente como **recetas**. Este fichero usa una sintaxis inspirada en los
ficheros `Makefile` de `make`, que en esta caso debe llamarse `justfile`.

Veamos un ejemplo de fichero `justfile`:

```just
alias b := build
host := `uname -a`

# Build main
build:
    cc *.c -o main

# Test everything
test-all: build
    ./test --all

# Run a specific test
test TEST: build
    ./test --test {{TEST}}
```

Si ahora ejecutamos `just -l` se nos muestra un menú con las distintas recetas.
Si antes de la receta hemos puesto un comentario, este se muestra también en el
listado:

```shell
$ just -l
Available recipes:
    build     # Build main
    b         # Alias for build
    test TEST # Run a specific test
    test-all  # Test everything
```

Al especificar la receta `build` como un **requisito** para los _tests_, cada vez
que los ejecutemos se ejecutará previamente la receta `build`.

Algunas características intersantes:

- A diferencia de `make`, no es un sistema de construcción, solo se centra
  en realizar determinas tareas, esto hace que sea mucho más sencillo
  y evita algunas de las idiosincrasias de `make` [^1].

- Funciona en Linux, Mac y Windows, aunque en Windows hay que
  indicarle la shell a usar.

- Las recetas pueden aceptar argumentos

- Carga por defecto las variables definidas en un fichero `.env`

- Las recetas se pueden listar fácilmente (`just -l`)

- Escrito en Rust

- Se puede añadir autocompletado para los _shells_ habituales

- Ls recetas se pueden construir usando el _shell_ o cualquier otro
  lenguaje que tengamos disponible, como Python, node o ruby

- Las recetas se pueden  ejecutar desde cualquier subdirectorio, no solo
  en el que contenga el fichero `justfile`



### Cuál es la receta por defecto de just

Si se invoca sin indicarle ninguna receta, just ejectua la primera de as
recetas definnidas en el fichoro `justfile`. Lo ideal es que esta primera
receta sea la usada con más frecuencia, por ejemplo, ejecutar los tests.


### Alternativas a just

- **pydoit** <https://pydoit.org/>
- **Invoke** (Sucesor de Fabric) <https://www.pyinvoke.org/>

Fuentes:
- [Manual de Just](https://just.systems/man/en/chapter_21.html)

[^1] Por ejemplo, supongamos una receta `test` y que en nuestro proyecto tuviéramos
   también un fichero o carpeta con el mismo nombre, `test`. `Make` nunca llegaría a
   ejecutar la receta, porque entiende que es para crear ese fichero,
   y como ya existe, no la ejecuta.  Esto es muy ventajoso para un sistema de
   _build_ o construcción, pero no tanto para un ejecutor de tareas, así que
   Just no incorpora estas comprobaciones, y por tanto no necesita la orden
   `$PHONY`, que en `Make` se usa para indicar objetivos que **no** son ficheros.

