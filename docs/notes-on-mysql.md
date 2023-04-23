---
title: Notes on MySQl
---

## MySQL

## Crear una base de datos MySQL

Crear la base de datos 

Usando el cliente de línea de comandos:

```shell
mysql --user=root --password=laquesea
create database bonnet character set utf8  COLLATE utf8_spanish_ci;
create user bonnet@localhost identified by "bonnet";
grant all privileges on bonnet.* to bonnet@localhost;    
```

## ¿Cómo conectarse a mysql sin que pregunte la password (En localhost)

Hay que definir un password y salvarlo en ``$HOME/.my.cnf`` con este formato:

```
[client]
password = asdfghjkl
```

Ya no preguntará el password para conexiones locales. Por defecto 
MySql Server instala una password al azar por usuario, se puede cambiar dicha
password con el siguiente comando:

```shell
mysqladmin -u root password 'asdfghjkl'
```

## Como instalar el cliente MySql de python en Ububtu (y derivados)

Ejecutar:

```shell
sudo apt-get install libmysqlclient-dev python-dev
```

label: python

## How to Migrate a MySQL database
 
Written by Guillermo Garron.

If you are moving to another hosting provider, or for any other reason you need to move or migrate your MySQL database you can use these instructions.

## Cómo hacer una copia de seguridad de una base de datos mysql

```
mysqldump -u root -p --opt [database_name] > /tmp/[database_name].sql
```


#### Copy the database to the new server

You can use rsync, scp or ftp, I will show you how to do it with scp:

```bash
scp /tmp/[database_name].sql menganito@server.com:/tmp/
```

#### Create the database in the new server:

```bash
mysql -u root -p
create database [database_name];
grant all privileges on [database_name].* to "some-user"@"hostname" identified by "some-strong-password";
flush privileges;
exit
```

#### Import the backup:

```
mysql -u root -p [database_name] < /tmp/[database_name].sql
```

### Como hacer una copia de seguridad de una base de datos MySql

Para realizar la copia de seguridad:

```
mysqldump --user=<username> --password=<password> --result_file=backup.sql --opt  <database>
```

Para restaurrar la copia:

```
mysql  --user=<usuario> --password=<clave> <basedatos> < respaldo.sql 
```

### How to show/list the users in a MySQL database

To show/list the users in a MySQL database, first log into your MySQL server as
an administrative user using the mysql command line client, then run this MySQL
query:

```sql
select * from mysql.user;
```

However, note that this query shows all of the columns from the `mysql.user`
table, which makes for a lot of output, so as a practical matter you may want
to trim down some of the fields to display, something like this:

```sql
select host, user, password from mysql.user;
```

Source: [Show Users I have created in
MySQL](https://alvinalexander.com/blog/post/mysql/show-users-i-ve-created-in-mysql-database)

## How to retrieve the ID after a MySQL Insert in Python

When you have an `auto_increment` field on a table, and you're doing a batch
import of new data, you often want to insert a row, then insert more rows that
have a foreign key referencing the first row. For example, you want to insert a
COMPANY entity, then insert a few dozen PERSON entities under that company.

Assuming you have no unique and not-null fields on the COMPANY entity (if
`company_name` were unique and not-null, then you could just issue a select
immediately after inserting to get its ID), and assuming you want a thread-safe
solution (you could just select for the highest ID in the table immediately
after inserting, but since MySQL is by default not transaction-safe, another
thread could come in and insert another company right after you insert and
before your select), you simply need to have `mysql_insert_id()`.

The MySQLdb documentation mentions `conn.insert_id()`, however this appears to
have been deprecated, maybe? This really should be on the cursor object anyway.
And behold! There is a `lastrowid` on it! It's just a little bit undocumented:

```python
import MySQLdb

connection = MySQLdb.connect(...)
cursor = connection.cursor()
cursor.execute("INSERT INTO PERSON (name) VALUES ('Philihp')")
print(cursor.lastrowid)
```

Source: [How to retrieve the ID After a MySQL Insert](https://philihp.com/2009/how-to-retrieve-the-id-after-a-mysql-insert-in-python.html)

label: python

## How to use Commit and Rollback to Manage MySQL Transactions in Python

To manage MySQL transactions in python follow these steps:

- Create MySQL database connections in python.

- Prepare the SQL queries that you want to run as a part of a
  transaction. For example for bank transfer, we can combine two SQL
  queries(withdrawal money and deposit money query) in a single
  transaction.

- Set an auto-commit property of MySQL connection to false.

- Execute all queries one by one using cursor.execute()

- If all queries execute successfully commit the changes to the
  database

- If one of the queries failed to execute rollback all the changes.

- Catch any SQL exceptions that may occur during this process

- Close the cursor object and MySQL database connection

Python MySQL Connector provides the following method to manage database
transactions.

- `commit` sends a COMMIT statement

- `rollback` revert the changes made by the current
  transaction

- `AutoCommit` True or False property to enable or disable
  the auto-commit feature of MySQL. By default is False.

Example to manage MySQL transactions using commit and rollback:

```python
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

try:
    conn = mysql.connector.connect(host='localhost',
                            database='python_db',
                            user='pynative',
                            password='pynative@#29')
    conn.autocommit = false
    cursor = conn.cursor()
    # withdraw from account A 
    sql_update_query = "Update account_A set balance = balance - 1000 where id = 1"
    cursor.execute(sql_update_query)
    # Deposit to account B 
    sql_update_query = "Update account_B set balance = balance + 1000 where id = 2"
    cursor.execute(sql_update_query)
    #Commit your changes
    conn.commit()
    print ("Record Updated successfully ")
except mysql.connector.Error as error :
    print("Failed to update record to database rollback: {}".format(error))
    conn.rollback() # reverting changes because of exception
finally:
    #closing database connection.
    if(conn.is_connected()):
        cursor.close()
        conn.close()
        print("connection is closed")
```

Source: Python MySQL Transaction Management using Commut and Rollback](https://pynative.com/python-mysql-transaction-management-using-commit-rollback/)


## How to make the Mysql GROUP BY statment to work the right way

This is the way:

```sql
SET GLOBAL sql_mode=(SELECT @@sql_mode||','||'ONLY_FULL_GROUP_BY');
```

And to do the opposite (make the GROUP BY work as only assholes could
like)

```
SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
```

## How to show running queries in MySQL

MySQL has a statement called `show processlist` to show you the running
queries on your MySQL server. This can be useful to find out what's
going on if there are some big, long queries consuming a lot of CPU
cycles, or if you're getting errors like "too many connections".

The syntax is simply:

```sql
show processlist;
```
    
which will output something along these lines:

```
---- --- ------ --- ----- --- ------------- -----------------------
Id   U s Host   d b Com   T i State         Info
     e r            man d m e               

70   r o loca   N U Que   0 2 NULL Copying  show processlist select
81 6 o t lhos t L L ry        to tmp table  dist.name,
70   t e loca   t e Que                     dist.filename, ...
81 7 s t lhos t s t ry                      
---- --- ------ --- ----- --- ------------- -----------------------
```

Source: <https://www.electrictoolbox.com/show-running-queries-mysql/>


## Como solucionar "Error: SET PASSWORD has no significance for user 'root'@'localhost' as ..."

Resulta que al instalar MySQL, incluso en una versión recién instalada de tu
sistema operativo Linux preferido puedes encontrarte con un error similar al
siguiente (usualmente al correr el comando `mysql_secure_installation`):

```
Failed! Error: SET PASSWORD has no significance for user 'root'@'localhost' as the authentication method used doesn't store authentication data in the MySQL server. Please consider using ALTER USER instead if you want to change authentication parameters
```

La solución a este error es bastante sencilla, entra a mysql de la siguiente manera:

```
sudo mysql
```

Una vez logueado se debe cambiar la clave del usuario root con el siguiente comando.

```
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password by 'mynewpassword';
```

Si el nivel de seguridad es medio, tendrás que poner una contraseña que
incluya mayúsculas y minúsculas, de al menos 8 caracteres, debe incluir al
menos un número y al menos un simbolo. Si el nivel es alto, se validará
también contra un fichero diccionario.

- Fuente: [Solución al error SET PASSWORD has no significance for user "root"@&"localhost" ...](https://blog.pleets.org/article/soluciworkarea/notes/docs/notes-on-mysql.mdC3workarea/notes/docs/notes-on-mysql.mdB3n-al-error-set-password-has-no-significance-for-user)


## Cómo arreglar "MySQL ERROR 1819 (HY000): Your password does not satisfy the current policy requirements"

There are three levels of password validation policy enforced when Validate Password plugin is enabled:

- `LOW` Length >= 8 characters.

- `MEDIUM` Length >= 8, numeric, mixed case, and special characters.

- `STRONG` Length >= 8, numeric, mixed case, special characters and dictionary file.

Based on these policy levels, you need to set an appropriate password.
To find the current password policy level, run the following command:

```
mysql> SHOW VARIABLES LIKE 'validate_password%';
```

Sample output:

```
+--------------------------------------+--------+
| Variable_name                        | Value  |
+--------------------------------------+--------+
| validate_password.check_user_name    | ON     |
| validate_password.dictionary_file    |        |
| validate_password.length             | 8      |
| validate_password.mixed_case_count   | 1      |
| validate_password.number_count       | 1      |
| validate_password.policy             | MEDIUM |
| validate_password.special_char_count | 1      |
+--------------------------------------+--------+
7 rows in set (0.09 sec)
```

Hot to Change password validation policy in MySQL

You can also solve the "ERROR 1819 (HY000)..." by setting up a lower level password policy.
To do so, run the following command from the mysql prompt:

```
mysql> SET GLOBAL validate_password.policy = 0;
```

O:

```
mysql> SET GLOBAL validate_password.policy=LOW;
```

Then check if the password validation policy has been changed to low:

```
mysql> SHOW VARIABLES LIKE 'validate_password%';
```

- Fuente: [Fix - MySQL ERROR 1819 (HY000): Your password does not satisfy the current policy requirements - OSTechNix](https://ostechnix.com/fix-mysql-error-1819-hy000-your-password-does-not-satisfy-the-current-policy-requirements/)
