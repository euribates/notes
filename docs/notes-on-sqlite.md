---
title: Notas sobre SQLite
tags: 
    - db
    - sql
    - python
---

## Sobre SQLite

**SQLite** es un sistema de gestión de bases de datos relacional compatible con
ACID, contenida en una relativamente pequeña (~275 kiB) biblioteca
escrita en C. SQLite es un proyecto de dominio público creado por D.
Richard Hipp.

## Cómo ver las tablas e índices en una base de datos sqlite

Con la orden `.tables` listamos todas las tablas de la base de datos.
Si queremos más información, `.schema` muestras información adicional, como los
índices. Cualquiera de los dos comandos puede ser seguido de una expresión
de tipo `LIKE` para restringir los resultados listadas

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
 WHERE type='table'
 ORDER BY name;
```

Tanto para índices como para tablas, el campo `text` contiene las sentencias DDL
de creación correspondiente (`CREATE TABLE | CREATE INDEX`).
