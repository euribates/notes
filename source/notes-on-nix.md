---
title: Notas sobre Nix (Lenguaje)
tags:
    - devops
    - linux
---

## Sobre Nix

En realidad, podemos estar hablando de dos cosas cuando hablamos de Nix:

- **[NIX el gestor de paquetes](https://en.wikipedia.org/wiki/Nix_(package_manager))**

- **[Nix el lenguaje](https://nixos.org/manual/nix/stable/language/index.html)**.

En estas notas nos centraremos en el lenguaje. Sus características principales
son:

- **Funcional puro**: No existe concepto de pasos secuenciales. Cualquier
  dependencia entre operaciones viene dictada por los datos. Cualquier
  fragmento válido de código Nix es un expresión que devuelve un valor.

- **lazy**: Solo evaluará una expresión cuando y si es necesario. Por ejemplo,
  el siguiente fragmento de código eleva una excepción, pero eso no llega a
  pasar porque nunca se evalúa la parte que lo eleva:


    ```nix
    let attrs = { a = 15; b = builtins.throw "Oh no!"; };
    in "The value of 'a' is ${toString attrs.a}"
    ```

- **De propósito específico**: El lenguaje Nix solo esta pensado para ser
  usado con el gestor de paquetes Nix. No es un lenguaje de propósito general.


## Primitivas de NIX

  Los tipos de datos reconocidos por Nix son:

- Números: `42`, `1.72394`

- Cadenas de texto y rutas: `"hello"`, `./some-file.json`

  Las cadenas de texto soportan interpolación: `"Hello ${name}"`

  También soporta cadenas de texto con múltiples lineas:

```Nix
# multi-line strings (common prefix whitespace is dropped)
''
first line
second line
''
```

- listas (Ojo, sin comas): `[ 1 2 3 ]`

- Conjuntos de atributos o estructuras `{ a = 15; b = "something else"; }`

  Se acceden por nombre.

  Pueden ser recursivo, los campos pueden hacer referencia unos a otros:
  
    ```nix
    rec { a = 15; b = a * 2; }
    ```

## Operadores

Nix tiene varios operadores, ninguno de los cuales es demasiado sorprendente:


| Sintaxis         | Descripción                                   |
|------------------|-----------------------------------------------|
| `+, -, *, /`     | Operaciones numéricas                         |
| `+`              | Concatenación de cadenas                      |
| `++`             | Concatenación de listas                       |
| `==`             | Igualdad                                      |
| `>, >=, <, <=`   | Operadores de comparación                     |
| `&&`             | AND lógico                                    |
| `||`             | OR lógico                                     |
| `e1 -> e2`       | Implicación lógica (es decir, `!e1 || e2`)    |
| `!`              | Negación lógica                               |
| `set.attr `      | Acceso al atributo `attr` dentro de `set`     |
| `set ? attr`     | Comprueba si existe un atributo               |
| `left // right ` | Mezcla los dos conjuntos*                     |

* En caso de conflicto en la mezcla, tiene preferencia el conjunto de la
  derecha

