---
title: Notas sobre postgresql
tags:
    - database
    - python
---

## Sobre PostgreSQL

**PostgreSQL**, también llamado simplemente **Postgres**, es un sistema de
gestión de bases de datos relacional orientado a objetos y de código abierto,
publicado bajo la licencia PostgreSQL, similar a
la[BSD](https://es.wikipedia.org/wiki/Licencia_BSD) o la
[MIT](https://es.wikipedia.org/wiki/Licencia_MIT).


## Cómo instalar Postgresql en Ubuntu

Primero, refrescar el índice de paquetes local:

```shell
sudo apt update
```

Ahora instalamos el paquete `postgresql`, junto con `postgresql-contrib`, que
nos añade algunas utilidades y funcionalidad adicional:

```shell
sudo apt install postgresql postgresql-contrib
```

Podemos verificar que el _daemon_ está arrancado con:

```shell
sudo systemctl status postgresql.service
```

Si no lo estuviera, arrancarlo con:

```shell
sudo systemctl start postgresql.service
```

## Entender los roles de PostgreSQL

Postgres Usa un concepto llamado **roles** para gestionar la autenticación y la
autorización. Estos aspectos se gestiona de forma similar a los grupos y
usuarios de linux,

Tras la instalación, POstgres está configurado inicialmente pra utilizar un
esquema de autenticación llamado **`ident`** que funciona asociando los roles
de postgres con una cuenta de usuario de Linux/Unix. Si existe un role
determinado en postgres, entonces un usuario con el mismo login o _username_
que el rol puede vaidarse con este sistema.

La instalación también crea por defecto un usuario Linux/Unix llamada
`postgres`, que se asocia automáticamente, mediante el mecanismo explicado en
el párrafo anterior, con el Rol `Postgres`.

Podemos conectar a postgres con esta cuenta impersonandonos primero como el
usuario `postgres`:

```shell
sudo -i -u postgres
```

Y luego accedemos al cliente de postgres con:

```shell
psql
```

Otra forma de hacerlo es combinar los dos pasos anteriores en uno solo:

```shell
sudo -u postgres psql
```


## Cómo salir del intérprete psql (PostgreSQL)

Para salir del interprete psql hay que usar:

```
\q
```

## Cómo mostrar los roles/usuarios ya existentes en PostgreSQL

El comando `\du` es la forma más rápida.

Otro método puede ser consultar el catalogo del sistema, que almacena en la
tabla `pg_roles` esa información:

```sql
SELECT rolname FROM pg_roles;
```

Fuentes:

- [How to show all users in PostgreSQL: Commands & Examples](https://www.w3resource.com/PostgreSQL/snippets/postgresql-show-users.php)


## Cómo crear un nuevo rol en PostgreSQL

Si estamos conectados con el usuario `postgres`, la forma más fácil de crear un
nuevo rol es:

```shell
createuser --interactive
```

Si estamos con otro usuario podemos usar `sudo`:

```shell
sudo -u postgres createuser --interactive
```

El programa nos preguntará interactivamente por las propiedades del usuario.

Fuente:

- [How To Install PostgreSQL on Ubuntu 20.04 [Quickstart] | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart)


## Cómo crear una base de datos PostgreSQL

1) Suponiendo que el servidor de PostgreSQL esté activo, nos conectamos con un
usuario con privilegios de administrador, normalmente `postgres`:

```shell
sudo -u postgres psql postgres
```

2) Creamos el usuario (Rol) con el que nos conectaremos

```sql
CREATE ROLE epublisher WITH CREATEDB LOGIN PASSWORD 'epublisher';
```

3) Nos conectamos como ese usuario y creamos la base de datos con:

```sql
CREATE DATABASE epublisher OWNER epublisher;
```

O creamos la base de datos y le asignamos todos los privilegios de la
misma al usuario:

```sql
GRANT ALL PRIVILEGES ON DATABASE epublisher to epublisher;
```

## Cómo crear un esquema (Equivalente a un tablespace en Oracle)

Usando la sentencia `CREATE SCHEMA`:

```sql
CREATE SCHEMA [IF NOT EXISTS] schema_name [ AUTHORIZATION user_name ];
```

Por ejemplo:

```sql
CREATE SCHEMA IF NOT EXISTS test AUTHORIZATION joe;
```

Crea un esquema o espacio de nombres llamado `test`, que es propiedad del
usuario `joe`, a menos que ya existiera un esquema con ese nombre (Sin importar
quien sea el propietario de ese esquema).

Fuente: [PostgreSQL Documentation 9.3 CREATE
SCHEMA](https://www.postgresql.org/docs/9.3/sql-createschema.html).


## Como cambiar la contraseña de un usuario

Con una conexión establecida con el usuarios en cuestión, ejecutar
la siguiente orden (En el ejemplo se supone que el usuario es `postgres`):

```sql
ALTER USER postgres PASSWORD 'myPassword';
```

En caso de éxito, obtendremos una salida:

```
ALTER ROLE
```

Fuente: [How to Set the Default User Password in PostgreSQL | Tutorial by Chartio](https://chartio.com/resources/tutorials/how-to-set-the-default-user-password-in-postgresql/)


## Cómo cambiar la longitud de datos de una columna sin perder datos

```sql
ALTER TABLE table_name ALTER COLUMN column_name TYPE CHARACTER VARCHAR(120);
```

- Fuente: [HOW TO INCREASE THE LENGTH OF A CHARACTER VARYING DATATYPE IN
  POSTGRES WITHOUT DATA LOSS](https://www.carnaghan.com/knowledge-base/how-to-increase-the-length-of-a-character-varying-datatype-in-postgres-without-data-loss/)


## How to agregate string values in a comma-separated values

You can use the `STRING_AGG()` function to generate a list of
comma-separated values. Is an aggregate function that concatenates a
list of strings and places a separator between them. The function does
not add the separator at the end of the string.

The following shows the syntax of the function:

```sql
STRING_AGG ( expression, separator [order_by_clause] )
```

It accepts two arguments and an optional `ORDER BY` clause.

- `expression` is any valid expression that can resolve to a character
  string. If you use other types than character string type, you need
  to explicitly cast these values of that type to the character string
  type.

- `separator` is the separator for concatenated strings.

The next example uses the `STRING_AGG()` function to return a list of
actor's names for each film from the film table:

```sql
SELECT f.title,
       string_agg (
            a.first_name || ' ' || a.last_name,
            ','
            ORDER BY a.first_name, a.last_name) as actors
  FROM film f
       INNER JOIN role r ON f.id_film = r.id_film
       INNER JOIN actor a USING r.actor_id = a.actor_id
 GROUP BY f.title;
```

Source: [PostgreSQL STRING_AGG() Function By Practical
Examples](https://www.postgresqltutorial.com/postgresql-aggregate-functions/postgresql-string_agg-function/)

## How to switch Databases

Most Postgres servers have three databases defined by default:
`template0`, `template1` and `postgres`. Databases `template0` and
`template1` are skeleton databases that are or can be used by the
`CREATE DATABASE` command, while `postgres` is the default database you
will connect to before you have created any other databases.

Once you have created another database you will want to switch to it in
order to create tables and insert data. Often, when working with servers
that manage multiple databases, you'll find the need to jump between
databases frequently. This can be done with the `\connect` meta-command
or its shortcut `\c`:

```shell
postgres=# \c sales
You are now connected to database "sales" as user "ubuntu".
sales=#
```

## How to see the schema / list Tables

Tl/DR: Con la orden '\dt'.

Once you've connected to a database, you will want to inspect which
tables have been created there. This can be done with the `\dt`
meta-command:

```
sales=# \dt
        List of relations
    Schema | Name  | Type  | Owner
--------+-------+-------+--------
    public | leads | table | ubuntu
(1 row)
sales=#
```

Source: [Listing Databases and Tables in PostgreSQL Using
psql](https://chartio.com/resources/tutorials/how-to-list-databases-and-tables-in-postgresql-using-psql/)


## How do you describe a table in PostgreSQL

Usa la orden `\d+`:

```sql
\d+ tablename
```

See the [Postgres Meta-Commands
section](https://www.postgresql.org/docs/current/app-psql.html#APP-PSQL-META-COMMANDS)
of the manual for more info.

Source: [StackOVerflow Questions
109325](https://stackoverflow.com/questions/109325/postgresql-describe-table)

## How to change the User password

For most systems, the default Postgres user is `postgres` and a password
is not required for authentication. Thus, to add a password, we must
first login and connect as the postgres user:

```shell
$ sudo -u postgres psql
```

With a connection now established to Postgres at the psql prompt, issue
the ALTER USER command to change the password for the postgres user:

```sql
ALTER USER postgres PASSWORD 'myPassword';
```

If successful, Postgres will output a confirmation of `ALTER ROLE` as
seen above.

Source: [How to set the default user password in
PostgreSQL](https://chartio.com/resources/tutorials/how-to-set-the-default-user-password-in-postgresql/).


## No usar nunca mayúsculas en los nombres de los campos ni tablas

PostgreSQL convienrte internamente todos los nombres de tablas, funciuones o
columnas a minúsculas, a no ser que se espedifiquen entre comillas dobles. Por
ejemplo, si creamos la tabla `Foo`, internamente se creará una tabla `foo`, Pero
si creamos una tabla `"Bar"` si que se respeta la capitalización 
PostgreSQL folds all names - of tables, columns, functions and everything else
- to lower case unless they're "double quoted". So create table `Foo` will create a table called `foo`, while create table `"Bar"` will create a table called `Bar`.

All these select commands will work:

```sql
select * from Foo;
select * from foo;
select * from "Bar";
```

All these will fail with "no such table": 

```
select * from "Foo";
select * from Bar;
select * from bar;
```

Stick to using a-z, 0-9 and underscore for names and you never have to worry
about quoting them.

Fuente: [Don't Do This on PostgreSQL](https://wiki.postgresql.org/wiki/Don't_Do_This#Don.27t_use_upper_case_table_or_column_names)

## Como saber los parámetros de conexión desde dentro

Una vez conectado, podemos comprobar los datos de la conexión con
el siquiente comando:

```
\conninfo
```
Qué daría algo similar a:

```
You are connected to database "sammy" as user "sammy" via socket in "/var/run/postgresql" at port "5432".
```

Fuente:

- [How To Install PostgreSQL on Ubuntu 20.04 [Quickstart]  | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart)


## Cómo hacer una copia de seguridad de una base de datos PostgreSQL

La mejor forma es usando la utilidad `pg_dump`:

```
pg_dump --format=custom --username $DATABASE_USER -c $DATABASE_NAME > database.pgdump
```

Existen varios formatos, que se pueden especificar con el flag `-F` o
`--format`. Con el valor `sql` obtenemos la exportación en forma de sentencias
SQL. con `custom` obtenemos un formato binario, que no podemos leer directamente
pero en cambio es mucho máß rápido y el fichero resultante es más pequeñó, ya
que está comrpimido. Las opciones `-U`/`--username` especifican el usuario, como
es légico. La opción `-c`/`--clean` hace una importación limpia, es decir,
elimina todos los objetos (drop) antes de volver a crearlos.


## ¿Cómo pasarle la contraseña a pg_dump?

Crea un fichero `.pgpass` en el directorio `HOME` del usuario que va a ejecutar
el programa `pg_dump`.

El formato de este fichero es:

```
hostname:port:database:username:password
```

Por ejemplo:

```
localhost:5432:mydbname:postgres:mypass
```

**Importante**: poner el fichero e nodo `0600` (Solo el propietario puede leer
y modificar). Si no tiene este modo, `pg_dump` lo ignorará.

```shell
chmod 600 ~/.pgpass
```

Fuente: [bash - How to pass in password to pg_dump? - Stack Overflow](https://stackoverflow.com/questions/2893954/how-to-pass-in-password-to-pg-dump)


## Cómo listar las secuencias en PostgreSQL

Hay varias formas de listar las secuencias (_sequences_) en Postgtres.

Usando usa sentencia SQL:

```sql
SELECT sequence_schema, sequence_name 
  FROM information_schema.sequences 
 ORDER BY sequence_name 
```

O, si estamos usando `psql`, con el comando `\ds`.

```
                           List of relations
 Schema |                 Name                 |   Type   |   Owner    
--------+--------------------------------------+----------+------------
 public | acepcion_etiquetas_id_seq            | sequence | jileon_acl
 public | acepcion_id_acepcion_seq             | sequence | jileon_acl
 public | acl_anexo_id_anexo_seq               | sequence | jileon_acl
 public | acl_categoria_id_categoria_seq       | sequence | jileon_acl
 public | acl_cita_id_cita_seq                 | sequence | jileon_acl
 public | acl_contacto_id_contacto_seq         | sequence | jileon_acl
 public | acl_enlace_id_enlace_seq             | sequence | jileon_acl
```

Fuentes:

- [How to list sequences in PostgreSQL database - Softbuilder Blog](https://soft-builder.com/how-to-list-sequences-in-postgresql-database/)
- [PostgreSQL Sequences](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-sequences/)


## Cómo restaurar una base de datos PostgreSQL

Si tenemos una copia de la base de datos realizados con `pgdump`, podemos
recuperarla con `psql` si esta en formato sql:

```shell
psql -U username -f backupfile.sql
```

o con `pg_restore`, si está en formato `custom`:

```shell
pg_restore -d db_bame path/to/dump/filenane -U db_user
```

## Sobre la intercalación (_collation_) en postgreSQL

!!! note "TLDR"

    Ordenar, compara y agrupar textos no es tan sencillo como parece.
    Asegurarse de usar `es_ES` o `es_ES.utf8` como _collation_. Si puede
    ser como valor por defecto de la base de datos. Esto puede ser
    complicado si la base de datos se creó con otra codificación/intercalación.
    En ese caso se puede volver a definir la codificación y/o intercalación
    para determinados campos.

El término **intercalación** (_collation_) se refiere a las reglas que se deben
usar para la ordenación, comparación y agrupación de textos. La simple
ordenación numérica normalmente no es capaz de resolver diferentes aspectos de
este problema.

Por ejemplo, ¿se deben presentar primero las palabras que empiezan por
mayúsculas que las que empiezan por minúsculas? (Es decir, las letras `A` y `a`
deben ser consideradas iguales, o debe primar una sobre la otra? En ese caso,
¿Cuál? ¿Y entre las letras ̀a ̀ y `á`? Si usáramos solo el código Unicode
entonces `a` (Unicode 97 - `0x0061`) es muy diferente de `á` (Unicode 225 -
`0x00E1`). ¿Qué hay de las letras `ch` y `ll`? ¿Son letras diferentes y, por
tanto, en un diccionario deberían encontrarse en secciones separadas? 

!!! note "Sobre CH y LL"

    En el caso del Español, tanto la `ch` como la `ll` dejaron de considerarse
    letras individuales en la Ortografía de la lengua española de **2010**. Esto no
    significa, claro está, que desaparezcan de la escritura: simplemente, dejan
    de considerarse letras del abecedario.

las recomendaciones de la UOC para la intercalación en Español incluyen:

- Las palabras con **guion o apóstrofo** se clasifican **como si no lo tuvieran**. En
  el caso de palabras que solo se distinguen porque una tiene guion y la otra
  no, esta va en primer lugar.

- Las palabras que llevan **tilde o diéresis** suelen clasificarse **como si no la
  llevasen**. En el caso de palabras que solo se distinguen por la tilde o la
  diéresis (sea porque una lleva alguno de estos signos y la otra no, sea
  porque los llevan diferentes), el orden de clasificación es el siguiente:

    - primero sin tilde
    - segundo con tilde
    - tercero con diéresis

- Las **mayúsculas y minúsculas** se **igualan**. En el caso de que dos palabras
  coincidan en sus caracteres excepto en el hecho de tener una la primera letra
  minúscula y la otra mayúscula, esta se suele ordenar después de aquella. 

Por defecto, PostgreSQL solo tiene como intercalaciones disponibles, `default`,
`C`, y `POSIX`. Estas intercalaciones solo están bien para angloparlantes. Lo
bueno es que la instalación del servidor mirará las intercalaciones disponibles
como variaciones locales en el sistema operativo, y las incorporará
automáticamente. Por tanto, si el S.O. sobre el que está ejecutándose tiene
soporte para Español, entonces el servidor de PostgreSQL también lo tendrá.

Estas reglas están codificadas correctamente en la codificación
`modern_spanish_ci_as`. Donde `modern` indica que no consideramos
`ch` o `ll` como letras separadas, `ci` indica que no distingue entre las
mayúsculas y las minúsculas (Es decir, que considera que **no** son
letras diferentes) y `as` indica que tenga en cuenta los acentos.

En PostgreSQL, la intercalación y el _encoding_ de una Base de Datos no se
puede cambiar de forma trivial, y habitualmente implica reconstruir toda la
Base de Datos, ya que afecta a cómo se almacenan internamente los datos. Cómo
mínimo habría que exportar, reconstruir tablas, e importar de nuevo. No vale
con modificar directamente las tablas del sistema (UPDATE pg_database).

A estas alturas, la codificación esta claro que debería ser, a no ser que
hubiera razones muy poderosas en contra, UTF-8.

Podemos averiguar tanto el _encodig_ como la intercalación usada en una
instancia de PostgreSQL con el metacomando `\l`, que nos produciría una
tabla similar a esta:

```
     Name       |     Owner      | Encoding |   Collate   |    Ctype    |         Access privileges         
-----------------+----------------+----------+-------------+-------------+-----------------------------------
 bbdd            | bbdd_user      | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =Tc/bbdd_user                    +
                 |                |          |             |             | bbdd_user=CTc/bbdd_user
 parcanweb       | parcanweb      | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
 postgres        | postgres       | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
 pycheck         | pycheck_user   | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =Tc/pycheck_user                 +
                 |                |          |             |             | pycheck_user=CTc/pycheck_user
```

Independientemente del cliente que utilicemos, podemos saber cuál es el
codificador de caracteres que tenemos asignado en el servidor PostgreSQL y en el
cliente con la instrucción `SHOW`.

Para conocer el _encoding_ establecido en el servidor PostgreSQL, debemos de ejecutar la siguiente sentencia:

```sql
SHOW server_encoding;
```

Para saber el _encoding_ que está utilizando el cliente que estamos usando, ejecutamos esta otra:

```
SHOW client_encoding;
```

Obviamente, lo óptimo es que en todos los casos estemos usando la misma
codificación e intercalado, para evitar conversiones ineficaces.


Fuentes:

- [Collations - Wikipedia](https://en.wikipedia.org/wiki/Collation)

- [Ordenación alfabética - Lengua y estilo de la UOC](https://www.uoc.edu/portal/es/servei-linguistic/convencions/ordenacio-alfabetica/index.html)

- [Collations in postgres](https://pganalyze.com/blog/5mins-postgres-collations)

- [How collation works | Peter Eisentraut](https://peter.eisentraut.org/blog/2023/03/14/how-collation-works)

- [PostgreSQL: Documentation: 15: 24.2. Collation Support](https://www.postgresql.org/docs/15/collation.html)
- [Collations in PostgreSQL: The Good, the bad and the ugly](https://www.postgresql.eu/events/pgconfeu2022/sessions/session/4040/slides/337/Collationsdocs/notes-on-postgresql.md20indocs/notes-on-postgresql.md20PostgreSQLdocs/notes-on-postgresql.md20-docs/notes-on-postgresql.md20Thedocs/notes-on-postgresql.md20good,docs/notes-on-postgresql.md20thedocs/notes-on-postgresql.md20baddocs/notes-on-postgresql.md20anddocs/notes-on-postgresql.md20thedocs/notes-on-postgresql.md20uglydocs/notes-on-postgresql.md20-docs/notes-on-postgresql.md20Tobiasdocs/notes-on-postgresql.md20Bussmann.pdf)

## Coma cambiar la intercalación usada en un campo de una tabla en PostgreSQL

Aunque no podemos cambiar la intercalación por defecto de una base de datos de
forma sencilla, podemos definirla de nuevo para determinados campos, con la
siguiente sentencia `DDL`:

```sql
alter table <nombre_table> alter column {nombre_campo> set data type VARCHAR(75) COLLATE "es_ES";
```

Obviamente, la intercalación recomendada para español es `es_ES`.

## Cómo entender los _tablespaces_ en PostgreSQL

PostgreSQL introdujo el concepto de **tablespaces** en la versión 8. En
PostgreSQL, un _tablespace_ es un enlace a una directorio en el sistema de
ficheros. Funciona como un contenedor para todos los demás objetos, como tablas,
índices, etc.

Hay muchos escenarios donde esta capacidad resulta útil. Por ejemplo, si nos
quedamos sin espacio adicional en el almacenamiento por defecto, podemos crear
un _tablespace_ en otro disco con capacidad libre. Otro caso de uso puede ser el
que seamos conscientes de diferentes patrones de uso para diferentes objetos o
bases de datos, y usemos los _tablespaces_ para mejorar el rendimiento. Por
ejemplo, si sabemos que una tabla va a ser usada masivamente, podemos alojar en
un _tablespace_ que este sobre un disco más rápido.
