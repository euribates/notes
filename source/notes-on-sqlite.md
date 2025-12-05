---
title: Notas sobre SQLite
tags: 
    - database
    - foss
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


## Como ver los índices en una base de datos SQLite

La forma más sencilla es usar el comando `.indexes`

```sql
sqlite> .indexes
auth_group_permissions_group_id_b120cbf9                      
auth_group_permissions_group_id_permission_id_0cd325b0_uniq   
auth_group_permissions_permission_id_84c5c92e                 
auth_permission_content_type_id_2f476e4b                      
auth_permission_content_type_id_codename_01ab375a_uniq        
auth_user_groups_group_id_97559544                            
auth_user_groups_user_id_6a12ed8b
...
```

Se puede indicar el nombre del indice o un patrón de tipo SQL, con `%` como
comodín:

```sql
sqlite> .indexes auth_user_user%
auth_user_user_permissions_permission_id_1fbb5f2c             
auth_user_user_permissions_user_id_a95ead1b                   
auth_user_user_permissions_user_id_permission_id_14a6b632_uniq
```

La otra es haciendo una consulta a la tabla `sql_master`:

```sql
SELECT name 
  FROM sqlite_master 
 WHERE type = 'index';
```


## Cómo ver las tablas en una base de datos SQLite

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

## Como usar la extensión FTS5 de Sqlite para búsqueda de texto

La extensión **FTS5** proporciona la funcionalidad de búsqueda de texto
avanzada. Esto permite realizar búsquedas de forma eficiente, ya que se
crea un índice por contenidos.

Para poder usarlo, solo hay que crear una o más tables marcadas como
fts5:

```sql
CREATE VIRTUAL TABLE email USING fts5(sender, title, body);
```

Obsérvese que **no** se especifican los tipos de datos, de hacho, da un
error si se intenta. Igualmente está prohibido el uso de _constraints_,
y tampoco se pueden definir claves primarias. Una vez creada la tabla,
se pueden insertar, actualizar y borrar registros como en cualquier otra
tabla. Aunque no permite definir una clave primaria, existe una clave
primaria implícita, llamada `rowid`.

Existen algunas opciones más avanzadas, que no se han mostrado en el
ejemplo inicial. Algunas de las cosas que podemos hacer son definir como
se extrae los términos del texto original, crear índices extra en disco
para acelerar las consultas, o crear una tabla virtual FTS4 que actue
como índice de un contenido almacenado en otro sitio.

Una vez cargados los datos, hay tres tipos de consultas que podemos
hacer:

- Usar un operador `MATCH` en el `WHERE` de una sentencia ``SELECT`

- Usar el operador _es igual que_ ("=") en el `WHERE` de una sentencia `SELECT`

- Usar funciones específicas llamadas `table-valued functions` 

Ejemplos:

```sql
SELECT * FROM email WHERE email MATCH 'fts5';
SELECT * FROM email WHERE email = 'fts5';
SELECT * FROM email('fts5');
```

Por defecto, todas las búsquedas con FTS5 **no** distinguen entre
mayúsculas y minúsculas. Si no se ha especificado un orden, los
resultados vendrán, como en cualquier otra consulta, en un orden
arbitrario. Se pueden ordenar los resultados por **relevancia** usando
la palabra clave `rank`, como en el siguiente ejemplo:

```sql
SELECT * FROM email WHERE email MATCH 'fts5' ORDER BY rank;
```

Además de los campos definidos en la tabla, se pueden usar una serie de
funciones axiliares para ampliar la información. Por ejemplo, la
función auxiliar `highlight` devuelve una copia del texto original con
las ocurrencias encotradas rodeadas por las marcas que queramos, como
por ejemplo `<b>` y `</b>`:

```sql
SELECT highlight(email, 2, '<b>', '</b>') FROM email('fts5');
```
