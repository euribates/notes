---
title: Notas sobre SQLite
tags: 
    - db
    - sql
    - python
---

## Sobre SQLite

**SQLite** es un sistema de gestión de bases de datos relacional compatible con
ACID, contenida en una relativamente pequeña (~275 kiB) biblioteca escrita en C.
Es un proyecto de dominio público creado por D.  Richard Hipp.

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

## Como crear un campo auto incremental en SQLite?

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
