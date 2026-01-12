MySql / MariaDB
========================================================================

Sobre :index:`MySQL` / :index:`MariaDB`
-----------------------------------------------------------------------

**MySQL** es un sistema de gestión de bases de datos relacional
desarrollado bajo licencia dual: licencia pública general/licencia
comercial por Oracle Corporation. Está considerada la base de datos
de código abierto más popular del mundo, y una de las más populares en
general.

**MariaDB** es un sistema de gestión de bases de datos derivado de MySQL
con licencia GPL (General Public License). Es desarrollado por Michael
(Monty) Widenius —fundador de MySQL—, la fundación MariaDB y la comunidad
de desarrolladores de software libre. Introduce dos motores de
almacenamiento nuevos, uno llamado ``Aria`` —que reemplaza a ``MyISAM`` y
otro llamado ``XtraDB``, en sustitución de ``InnoDB``. Tiene una alta
compatibilidad con MySQL ya que posee las mismas órdenes, interfaces, API
y bibliotecas y su objetivo es poder cambiar un servidor por otro
directamente.


Crear una base de datos MySQL
-----------------------------------------------------------------------

Crear la base de datos

Usando el cliente de línea de comandos:

.. code:: shell

    mysql --user=root --password=laquesea

 Y una vez dentro:

.. code:: sql

    create database bonnet character set utf8  COLLATE utf8_spanish_ci;
    create user bonnet@localhost identified by "bonnet";
    grant all privileges on bonnet.* to bonnet@localhost;


¿Cómo conectarse a MySql sin que pregunte la password (En localhost)
-----------------------------------------------------------------------

Hay que almacenar la *password* en ``$HOME/.my.cnf`` con este
formato:

.. code::

    [client]
    password = asdfghjkl

Ya no preguntará el *password* para conexiones locales. Por defecto MySql
Server instala una *password* al azar por usuario, se puede cambiar dicha
*password* con el siguiente comando:

.. code:: shell

    mysqladmin -u root password 'asdfghjkl'


Como instalar el cliente MySql de python en Ububtu (y derivados)
----------------------------------------------------------------

Ejecutar:

.. code:: shell

    sudo apt-get install libmysqlclient-dev python-dev


Como hacer una copia de seguridad de una base de datos MySql
-----------------------------------------------------------------------

Para realizar la copia de seguridad:

.. code:: shell

    mysqldump --user=<username> --password=<password> --result_file=backup.sql --opt  <database>


Cómo importar desde la copia de seguridad
-----------------------------------------------------------------------

Desde la *shell*:

.. code:: shell

    mysql -u root -p [database_name] < /tmp/[database_name].sql


Cómo listar los usuarios en MySql
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nos conectamos con un usuario con privilegios, normalmente ``admin``, y
luego ejecutar el siguiente código:

.. code:: sql

    SELECT * FROM mysql.user;

Esto muestra todas las columnas de la tabla usuario, que pueden ser un
montón, una versión recortada puede ser:

.. code:: sql

    SELECT host, user, password FROM mysql.user;

Source: `Show Users I have created in MySQL <https://alvinalexander.com/blog/post/mysql/show-users-i-ve-created-in-mysql-database>`_


Cómo recuperar el ID des[pues de hacer un INSERT
-----------------------------------------------------------------------

Cuando se tiene un campo ``auto_increment`` en una tabla y se realiza
una importación por lotes de nuevos datos, a menudo se desea insertar
una fila y luego insertar más filas con una clave foránea que hace
referencia a la primera fila. Por ejemplo, se desea insertar una
entidad ``COMPANY`` y luego varias docenas de entidades ``PERSON`` bajo
esa empresa.

Una forma segura de conseguir el ultimo ID insertado en la base de datos
es con la propiedad ``lastrowid`` del cursor:

.. code:: python

    import MySQLdb

    connection = MySQLdb.connect(...)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO PERSON (name) VALUES ('Philihp')")
    print(cursor.lastrowid)

Source: `How to retrieve the ID After a MySQL Insert <https://philihp.com/2009/how-to-retrieve-the-id-after-a-mysql-insert-in-python.html>`_


Cómo usar Commit y Rollback para realizar transacciones en MySQL
---------------------------------------------------------------------

To manage MySQL transactions in python follow these steps:

- Create MySQL database connections in python.

- Prepare the SQL queries that you want to run as a part of a transaction.
  For example for bank transfer, we can combine two SQL queries(withdrawal
  money and deposit money query) in a single transaction.

- Set an auto-commit property of MySQL connection to false.

- Execute all queries one by one using cursor.execute()

- If all queries execute successfully commit the changes to the database

- If one of the queries failed to execute rollback all the changes.

- Catch any SQL exceptions that may occur during this process

- Close the cursor object and MySQL database connection

Python MySQL Connector provides the following method to manage database
transactions.

- ``commit`` sends a COMMIT statement

- ``rollback`` revert the changes made by the current transaction

- ``AutoCommit`` True or False property to enable or disable the
  auto-commit feature of MySQL. By default is False.

Example to manage MySQL transactions using commit and rollback:

.. code:: python

    import mysql.connector
    from mysql.connector import Error
    from mysql.connector import errorcode

    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='python_db',
            user='pynative',
            password='pynative@#29',
            )
        conn.autocommit = false
        cursor = conn.cursor()

        sql_withdraw_from_A = "UPDATE account SET balance = balance - 1000 WHERE id = 'A'"
        cursor.execute(sql_withdraw_from_A)
        
        sql_deposit_to_B = "Update account SET balance = balance + 1000 WHERE id = 'B'"
        cursor.execute(sql_deposit_to_B)
        
        conn.commit()  #  Commit your changes
        print ("Record Updated successfully ")
    except mysql.connector.Error as error :
        print("Failed to update record to database rollback: {}".format(error))
        conn.rollback() # reverting changes because of exception
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
        print("connection is closed")

Source: Python MySQL Transaction Management using Commut and Rollback](https://pynative.com/python-mysql-transaction-management-using-commit-rollback/)

How to make the Mysql GROUP BY statment to work the right way
-----------------------------------------------------------------------

This is the way:

.. code:: sql

    SET GLOBAL sql_mode=(SELECT @@sql_mode||','||'ONLY_FULL_GROUP_BY');

And to do the opposite (make the GROUP BY work as only assholes could
like):

.. code:: sql

   SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));

How to show running queries in MySQL
-----------------------------------------------------------------------

MySQL tiene una sentencia llamada para mostrar las consultas en
ejecución. Esto puede ser útil para averiguar qué sucede si hay
consultas largas y extensas que consumen muchos ciclos de CPU, o
si se obtienen errores como "demasiadas conexiones".

La sintaxis es simple:

.. code:: sql

    SHOW [FULL] PROCESSLIST;


Source: https://dev.mysql.com/doc/refman/8.4/en/show-processlist.html


Como solucionar “Error: SET PASSWORD has no significance ..."
-----------------------------------------------------------------------

Resulta que al instalar MySQL, incluso en una versión recién instalada
de tu sistema operativo Linux preferido puedes encontrarte con un error
similar al siguiente (usualmente al correr el comando
``mysql_secure_installation``):

.. code::

    Failed! Error: SET PASSWORD has no significance for user
    'root'@'localhost' as the authentication method used doesn't store
    authentication data in the MySQL server. Please consider using ALTER
    USER instead if you want to change authentication parameters

La solución a este error es bastante sencilla, entra a mysql de la
siguiente manera:

.. code:: shell

sudo mysql

Una vez logueado se debe cambiar la clave del usuario root con el
siguiente comando.

.. code:: sql

    ALTER USER 'root'@'localhost'
          IDENTIFIED WITH mysql_native_password
          BY 'mynewpassword';


Si el nivel de seguridad es medio, tendrás que poner una contraseña que
incluya mayúsculas y minúsculas, de al menos 8 caracteres, debe incluir
al menos un número y al menos un símbolo. Si el nivel es alto, se
validará también contra un fichero diccionario.

- Fuente: `Solución al error SET PASSWORD has no significance ... <https://blog.pleets.org/article/soluciworkarea/notes/docs/notes-on-mysql.mdC3workarea/notes/docs/notes-on-mysql.mdB3n-al-error-set-password-has-no-significance-for-user>`_


Cómo arreglar “ERROR 1819 (HY000): Your password does not satisfy ...
-----------------------------------------------------------------------

There are three levels of password validation policy enforced when
Validate Password plugin is enabled:

- ``LOW`` Length >= 8 characters.

- ``MEDIUM`` Length >= 8, numeric, mixed case, and special characters.

- ``STRONG`` Length >= 8, numeric, mixed case, special characters and
dictionary file.

Based on these policy levels, you need to set an appropriate password.
To find the current password policy level, run the following command:

.. code:: shell

    mysql> SHOW VARIABLES LIKE 'validate_password%';

Cuya salida es similar a:

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

Hot to Change password validation policy in MySQL

You can also solve the “ERROR 1819 (HY000)…” by setting up a lower level
password policy. To do so, run the following command from the mysql
prompt:

.. code:: shell

    mysql> SET GLOBAL validate_password.policy = 0;

O:

.. code:: shell

    mysql> SET GLOBAL validate_password.policy=LOW;

Then check if the password validation policy has been changed to low:

.. code:: shell

    mysql> SHOW VARIABLES LIKE 'validate_password%';

Fuente: `Fix - MySQL ERROR 1819 (HY000): Your password does not satisfy the current policy requirements -
OSTechNix <https://ostechnix.com/fix-mysql-error-1819-hy000-your-password-does-not-satisfy-the-current-policy-requirements/>`_


Cómo saber la versión del gestor de la base de datos en MySql
-----------------------------------------------------------------------

Con el comando SQL:

.. code:: sql

    select VERSION();

Fuente: https://marcelitux.wordpress.com/2011/11/16/comando-para-saber-la-version-de-la-base-de-datos-oracle-ms-sql-server-mysql/
