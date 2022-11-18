---
title: Notas sobre pgsql (SQL de postgresql)
tags:
  - database
  - postgresql
---

## Sobre pgSQL

**PL/pgSQL** (*Procedural Language/PostgreSQL*) is a loadable procedural
programming language supported by the PostgreSQL. PL/pgSQL, as a fully
featured programming language, allows much more procedural control than
SQL, including the ability to use loops and other control structures.
Functions created in the PL/pgSQL language can be called from an SQL
statement, or as the action that a trigger performs

## Supported argument and result data types

- Functions can accept as arguments any scalar or array data type
  supported by the server, and return the same data type result.
- Also, accept or return any composite type (row type) specified by
  name.
- Functions can be declared to accept a variable number of arguments
  by using the `VARIADIC` marker.
- Functions can also be declared to accept and return the polymorphic
  types any element, any array.
- PL/pgSQL functions can also be declared to return a \"set\" (or
  table) of any data type that can be returned as a single instance.
- A PL/pgSQL function can be declared to return void if it has no
    useful return value


## Structure of PL/pgSQL

PL/pgSQL is a block-structured language and each statement within a
block is terminated by a semicolon. A block that appears within another
block must have a semicolon after END, however, the final END that
concludes a function body does not require a semicolon. **All keywords
are case-insensitive** and **identifiers are implicitly converted to
lower case** unless double-quoted, just as they are in ordinary SQL
commands.See the following syntax:

```
[ <<label>> ]
[ DECLARE
    declarations ]
BEGIN
    statements
END [ label ];
```

The label is optional and is only needed if you want to identify the
block for use in an `EXIT` statement, or to qualify the names of the
variables declared in the block. If a label is given after `END`, it
must match the label at the block\'s beginning. Comments work the same
way in PL/pgSQL code as in ordinary SQL.

All **variables must be declared in the declarations section** of the
block. The only exceptions are that the loop variable of a `FOR` loop
iterating over a range of integer values is automatically declared as an
integer variable. The types of PL/pgSQL variables are similar to SQL
data types, such as integer, varchar, and char.

Here is the general syntax of a variable declaration:

```
name [ CONSTANT ] type [ COLLATE collation_name ] [ NOT NULL ] [ { DEFAULT | := } expression ];
```

The `DEFAULT` clause, if given, specifies the initial value assigned to
the variable when the block is entered. If the `DEFAULT` clause is not
given then the variable is initialized to the SQL `null` value.


## Declaring Function Parameters

Parameters passed to functions are named with the identifiers `$1`,
`$2`, etc. Optionally, aliases can be declared for `$n` parameter names
for increased readability. The preferred way is to give a name to the
parameter in the CREATE FUNCTION command, for example:

```sql
CREATE FUNCTION sum_of_two_numbers(m integer, n integer)
RETURNS integer AS $$
    BEGIN
            RETURN m + n;
    END;
$$ LANGUAGE plpgsql;
```

La expresion `%TYPE` se usa para obtener el tipo de la variable que la precece.
En el siguiente ejemplo devuelve el tipo de dato de la columna `roll_no` de la
tabla `student`:

```sql
variable_name student.roll_no%TYPE
```

Here is another Example:

```
CREATE FUNCTION get_employee(text) RETURNS text AS $$
DECLARE
    frst_name ALIAS FOR $1;
    lst_name employees.last_name%TYPE;
BEGIN
    SELECT INTO lst_name last_name FROM employees 
    WHERE first_name = frst_name;
    return frst_name || '' '' || lst_name;
END;
$$ LANGUAGE 'plpgsql';
```


## Row Types

A variable of a composite type is called a row variable which can hold a
whole row of a `SELECT` or `FOR` query result, so long as that query's
column set matches the declared type of the variable:

```sql
name table_name%ROWTYPE;
name composite_type_name;
```

The individual fields of the row value are accessed using the usual dot
notation, for example, `rowvar.table_field`. The fields of the row type
inherit the table\'s field size or precision for data types such as
`char(n)`. See the following example:

```sql
CREATE FUNCTION get_employee (integer) RETURNS text AS $$
DECLARE
    emp_id ALIAS FOR $1;
    found_employee employees%ROWTYPE;
BEGIN
SELECT INTO found_employee * FROM employees WHERE employee_id = emp_id;
    RETURN found_employee.first_name || '' '' || found_employee.last_name;
END;
$$ LANGUAGE 'plpgsql';
```

Fuente: <https://w3resource.com/PostgreSQL/pl-pgsql-declarations.php>
