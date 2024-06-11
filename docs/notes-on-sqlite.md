---
title: Notas sobre SQLite
tags: 
    - db
    - sql
    - python
    - c
    - c++
---

## Sobre SQLite

**SQLite** es un sistema de gestión de bases de datos relacional compatible con
capacidades [ACID](https://es.wikipedia.org/wiki/ACID), contenida en una
biblioteca relativamente pequeña (~275 kiB) escrita en
[C](https://es.wikipedia.org/wiki/C_%28lenguaje_de_programaci%C3%B3n%29). Es un
proyecto de dominio público creado por D.  Richard Hipp.

## Inconvenientes y rarezas de SQLite

- No es un gestor de base de datos, es una librería pensada para _sotfware_
  **embebido**.

- **Tipos de datos _flexibles_**: Los tipos de datos se consideran más
  recomendaciones que obligaciones. Si, por ejemplo, insertamos la cadena de
  texto `'1234'` en un campo de tipo `INTEGER`, la base de datos almacenará
  el número $1234$. Pero si intentamos insertar `'wzxy'`, en vez de dar un
  error, guardará el dato en forma de cadena de texto. Si, es raro de cojones.

- **No hay un tipo de dato para fechas**. En vez de eso, podemos guardar fechas
  como:

    - Una cadena de texto (`TEXT`) en formato `ISO-8601`

    - Un `INTEGER` con el número de segundos desde 1/1/1989 (_Unix time_)

    - Un valor `REAL` como una fracción del [día juliano](https://es.wikipedia.org/wiki/Fecha_juliana)

  Las funciones de fechas de SQLite entienden todos estos formatos.

- **No hay un campo de datos para _booleanos_**. Se suele usar los entero $0$ y $1$
  para representar falso y verdadero respectivamente. Desde la versión
  3.23.0 (Marzo de 2018) se pueden usar las palabras clave `TRUE` y `FALSE` como
  sinónimos de $1$ y $0$.

Hay [más rarezas y cosas curiosas de SQLite
aquí](https://sqlite.org/quirks.html).


## Cómo ver las tablas e índices en una base de datos SQLite

Con la orden `.tables` listamos todas las tablas de la base de datos.  Si
queremos más información, `.schema` muestras información adicional, como los
índices. Cualquiera de los dos comandos puede ser seguido de una expresión de
tipo `LIKE` para restringir los resultados listadas

Otra forma seria haciendo un `SELECT` a la tabla `SQLITE_SCHEMA`. Esta table
existe en todas las bases de datos SQLite y tiene la siguiente estructura:

```sql
CREATE TABLE sqlite_schema (
    type TEXT,
    name TEXT,
    tbl_name TEXT,
    rootpage INTEGER,
    sql TEXT
    );
```

Para las tablas, el campo `type` siempre valdrá `table` (Para los índices, sería
`index`), así que podemos conseguir los nombres de todas las tablas con la
siguiente consulta:

```sql
SELECT name
  FROM sqlite_schema
 WHERE type = 'table'
 ORDER BY name;
```

Tanto para índices como para tablas, el campo `text` contiene las sentencias `DDL`
de creación correspondiente (`CREATE TABLE | CREATE INDEX`).

## Cómo crear un campo auto incremental en SQLite

**tldr**; Declarar el campo como `INTEGER PRIMARY KEY AUTOINCREMENT`.

Explicación larga:

Una columna declarada como `INTEGER PRIMARY KEY` ya **por defecto** será auto
incremental. Si se inserta un nuevo registro con un valor `NULL` para la
columna, se reemplaza automáticamente por el número entero mayor que exista, más
uno. Si no existe ningún registro previo, entonces valdrá $1$.

El problema de usar esto es que no sabemos que valor de clave primaria va a ser
asignada. SQLite incluye la función `last_insert_rowid` para obtenerlo. Lo ideal
sería usar secuencias, pero por el momento SQLite no las soporta.

Un posible problema de esta solución es que asigna el número basándose **en los
registros que haya en ese momento en la tabla**. Esto implica que, si se han
borrado registros, existe la posibilidad de que reutilice una clave primaria de
un registro borrado previamente. Si queremos evitar que pase esto, debemos
añadir la palabra clave `AUTOINCREMENT` en la declaración del campo. En ese
caso, usará como base el mayor número que **haya habido en algún momento**, con
lo que no se reutilizan las claves primarias de registros borrados.

La opción de `AUTOINCREMENT` implica un cálculo más complejo, así que si no
importa que se reutilizan claves primarias y la eficiencia es importante, se
puede omitir.
