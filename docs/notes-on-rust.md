---
title: Notas sobre Rust
tags:
    - rust
    - languages
    - devops
---

## Sobre Rust

Rust es un lenguaje de programación compilado,
de propósito general y multiparadigma 
que está siendo desarrollado por la 
[Fundación Rust](https://foundation.rust-lang.org/).

Soporta programación funcional pura, por
procedimientos, imperativa y orientada a objetos. 

Rust es desarrollado de forma totalmente abierta
y busca la opinión y contribución de la comunidad.
El diseño del lenguaje se ha ido perfeccionando
a través de las experiencias en el desarrollo
del motor de navegador Servo, y el propio compilador de Rust.
Aunque es desarrollado y patrocinado por Mozilla y Samsung,
es un proyecto comunitario. Gran parte de las contribuciones
proceden de los miembros de la comunidad.

En 2022, Rust se convirtió en el tercer lenguaje de programación
usado en el núcleo Linux, después de C y ensamblador.

## El sistema de tipos de Rust

El sistema de tipos soporta un mecanismo similar
a las clases de tipos, llamado _traits_, inspirados directamente
por el lenguaje **Haskell**. Esta es una facilidad para el polimorfismo
que soporta distintos tipos de argumentos (polimorfismo _ad-hoc_),
lograda mediante la adición de restricciones
para escribir declaraciones de variables.
Otras características de Haskell,
como el polimorfismo de diferente tipo (_higher-kinded_),
no están soportadas.

Rust cuenta con **inferencia de tipos**, para las variables declaradas
con la palabra clave `let`. Tales variables no requieren ser inicializadas
con un valor asignado con el fin de determinar su tipo.
En tiempo de compilación produce un error
si cualquier rama de código falla al asignar un valor a la variable.

Las funciones pueden recibir parámetros genéricos
pero deben ser delimitados expresamente por los _traits_,
no hay manera de dejar fuera de declaraciones de tipo
sin dejar de hacer uso de los métodos y operadores de los parámetros.

## Hola, Mundo en Rust

```rust
fn main() {
    println!("¡Hola, mundo!");
}
```

