Oracle
========================================================================

.. tags:: database,sql,sistemas,oracle


Sobre :index:`Oracle`
-----------------------------------------------------------------------

`Oracle`_ es un gestor
de bases de datos, propiedad de *Oracle Corporation*.

.. _Oracle: https://en.wikipedia.org/wiki/Oracle_Database

Configurar sqlplus
-----------------------------------------------------------------------

Al arrancar *sqlplus*, se ejecuta primero el fichero de configuración
global ``glogin.sql``, si existe, y luego el fichero de configuración
local o de usuario ``login.sql``, si existe. Las opciones definidas en
el fichero local sobreescriben las definidas a nivel global.

El fichero de opciones global se encuentra en
``$ORACLE_HOME/glogin.sql``.

El fichero local ``login.sql`` se busca en el directorio actual, y
después en los directorios especificados en la variable de entorno
``SQLPATH``. Atención porque no busca el fichero en el directorio
``$HOME``, como podría esperarse, y la variable ``SQLPATH`` por defecto
esta vacía.

Fuentes:

- `Administering SQLPlus <https://docs.oracle.com/cd/E11882_01/server.112/e10839/admn_sqlpls.htm#UNXAR156>`_

Cómo editar lineas e histórico usando sqlplus
-----------------------------------------------------------------------

Hay que instalar una utilidad de terceros llamada
`rlwrap <https://oracle-base.com/articles/linux/rlwrap>`__. Si no está
instalada:

.. code:: shell

    sudo apt install rlwrap

Y luego llamar a sqlplus usando rlwrap:

.. code:: shell

    rlwrap sqlplus <usr>/<pwd>@oracle

Podemos definir un alias, añadiendo esta linea a nuestro ``.bashrc``:

.. code:: bash

    alias sqlplus="rlwrap sqlplus"

Fuentes: - `sqlplus command line editing — oracle-tech <https://community.oracle.com/tech/developers/discussion/2184333/sqlplus-command-line-editing>`_

Cómo ajustar el ancho de las columnas en la salida de sqlplus
-----------------------------------------------------------------------

Se usa el comando ``COLUMN``:

.. code:: sql

    column username format A10
    column salary format 99999999,99

Define la columna que se llame *username* como de texto (``A``) de 10
caracteres, y *salary* como 10 dígitos, los dos últimos reservados para
decimales.

Fuentes:

- `Formatting SQLPlus Reports <https://docs.oracle.com/cd/B19306_01/server.102/b14357/ch6.htm>`_

Cómo crear una base de datos (usuario y tablespace) en Oracle
-----------------------------------------------------------------------

Para preparar una nueva base de datos hay que realizar los siguientes
pasos: crear un usuario por defecto, crear un *tablespace* para almacenar
los objetos propios de la base de datos (tablas, índices, secuencias,
etc..) y asignar el *tablespace* creado como *tablespace* por defecto del
nuevo usuario:

Cómo crear un nuevo usuario
~~~~~~~~~~~~~~~~~~~~~~~~~~~

La sentencia SQL es:

.. code:: sql

    CREATE USER <nombre_de_usuario> IDENTIFIED BY <contraseña>;

Por ejemplo:

.. code:: sql

    CREATE USER jarjar IDENTIFIED BY iamaloser;

La contraseña no es necesario entrecomillarla, y distinguirá entre
mayúsculas y minúsculas.

Ahora, tenemos que asignar al usuario, como mínimo, los permisos
``connect`` y ``resource``. El primer permiso permite al usuario
conectarse, el segundo le habilita para poder crear objetos (tablas,
índices, etc)

.. code:: sql

    GRANT CONNECT, RESOURCE TO jarjar;

Podemos cambiar en cualquier momento la contraseña del usuario con la
siguiente sentencia:

.. code:: sql

    ALTER USER jarjar IDENTIFIED BY istinks;

Cómo crear y asignar un nuevo *tablespace*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para crear un nuevo *tablespace*, hay que indicar, al menos, el nombre del
fichero de almacenamiento y un tamaño inicial. Se pueden el sufijo ``K``
para indicar kilobytes, y ``M`` para indicar megabytes.

.. code:: sql

    CREATE TABLESPACE transparencia DATAFILE 'transprencia.dbf' SIZE 120M;

Si queremos crearlo con un tamaño base pero que pueda crecer si lo
necesita:

.. code:: sql

    CREATE TABLESPACE transparencia DATAFILE 'transparencia.dbf' SIZE 12M AUTOEXTEND on;

Se pueden definir muchas más propiedades del tablespace a la hora de
crearlo, pero no se explicarán aquí.

Posteriormente, asignaremos el tablespace recien creado al usuario como
valor por omisión.

.. code:: sql

    ALTER USER jarjar DEFAULT TABLESPACE naboo;


Cómo ver el código de creación de una tabla
-----------------------------------------------------------------------

Este es el camino:

.. code:: sql

    set long 10000
    set pagesize 0
    set head off
    set echo off
    set verify off
    set feedback off
    select DBMS_METADATA.GET_DDL('TABLE','TABLE NAME'[,'SCHEMA']) from DUAL

Por ejemplo para ver la tabla ``tareas.tarea_proyectos``:

.. code:: sql

    SELECT dbms_metadata.get_ddl('TABLE', 'TAREAS_PROYECTO', 'TAREAS') FROM DUAL;

- Fuente: `Stackoverflow: How can I generate or get a DDL script on an existing table in Oracle <https://stackoverflow.com/questions/26249892/>`_


Cómo listar los *tablespaces*
-----------------------------------------------------------------------

This is the way:

.. code:: sql

    SELECT tablespace_name, file_name, bytes / 1024/ 1024  MB
      FROM dba_data_files
     WHERE tablespace_name like 'A%'
     ORDER BY tablespace_name;


Como listar las tablas definidas en la base de datos
-----------------------------------------------------------------------

This is the way:

.. code:: sql

    SELECT owner, table_name
      FROM dba_tables

Assuming that you have access to the ``DBA_TABLES`` data dictionary
view. If you do not have those privileges but need them, you can request
that the DBA explicitly grants you privileges on that table or that the
DBA grants you the ``SELECT ANY DICTIONARY`` privilege or the
``SELECT_CATALOG_ROLE`` role (either of which would allow you to query
any data dictionary table). Of course, you may want to exclude certain
schemas like ``SYS`` and ``SYSTEM`` which have large numbers of Oracle
tables that you probably don't care about.

Alternatively, if you do not have access to ``DBA_TABLES``, you can see
all the tables that your account has access to through the
``ALL_TABLES`` view:

.. code:: sql

    SELECT owner, table_name
      FROM all_tables

although that may be a subset of the tables available in the database
(``ALL_TABLES`` shows you the information for all the tables that your
user has been granted access to).

If you are only concerned with the tables that you own, not those that
you have access to, you could use ``USER_TABLES``:

.. code:: sql

    SELECT table_name
      FROM user_tables

Since ``USER_TABLES`` only has information about the tables that you
own, it does not have an ``OWNER`` column –the owner, by definition, is
you.

Cómo usar la codificación UTF-8 en Oracle
-----------------------------------------

Definiendo la variable de entorno ``NLS_LANG`` con este valor:

.. code:: bash

    export NLS_LANG=SPANISH_SPAIN.UTF8


Cómo desbloquear (UNLOCK) una cuenta de usuario de ORACLE
-----------------------------------------------------------------------

Podemos comprobar el estado de la cuenta de un usuario, por ejemplo
``WEBPUBLIC`` con:

.. code:: sql

    SELECT username, account_status
      FROM dba_users
     WHERE username = 'WEBPUBLIC';

Cuya salida debería ser similar a esta:

.. code::

    USERNAME ACCOUNT_STATUS PROFILE
    -------------------- -------------------- ---------------
    WEBPUBLIC LOCKED(TIMED) DEFAULT

Posiblemente está bloqueado por haber realizado varios intentos de login
infructuosos. El número de intentos antes de bloquear la cuenta en el
perfil por defecto es de **10**.

Para volver a habilitar la cuenta:

.. code:: sql

    ALTER USER webpublic ACCOUNT UNLOCK;


Cómo salvar la salida de sqlplus (oracle) a fichero
-----------------------------------------------------------------------

Usar la orden ``spool``:

.. code::

    spool /tmp/myoutputfile.txt
    select * from users;
    spool off;

Unas opciones útiles pueden ser:

.. code::

    HEAD OFF

Para que no ponga los cabeceras, y:

.. code::

    SET PAGES 0

Para que no pagine los resultados


Cómo Instalar cxOracle en Linux
-----------------------------------------------------------------------

Primero: Instalar las dependencias de Oracle Instant CLient:

.. code:: bash

    sudo apt-get install alien libaio1 python-dev

Segundo: Instalar el **InstantClient de Oracle**.

Descargar los paquetes de OracleIntantClient en formato rpm (RedHat) y
pasarlo a .deb (Debian) con alien. Podemos indicar que ademas de
convertir se instale el paquete con la opción ``-i``:

.. code:: bash

    sudo alien -i oracle-instantclient12.1-basic-12.1.0.2.0-1.x86_64.rpm
    sudo alien -i oracle-instantclient12.1-devel-12.1.0.2.0-1.x86_64.rpm
    sudo alien -i oracle-instantclient12.1-sqlplus-12.1.0.2.0-1.x86_64.rpm

Si da el error
``BDB0091 DB_VERSION_MISMATCH: Database environment version mismatch``
es que la caché del programa alien es corrupta u obsoleta, hay que
borrar la caché con ``rm -r ~/.rpmdb/``.

Tercero: Instalar las dependencias de cx_Oracle:

.. code:: bash

    sudo pip install cx_oracle

Cuarto: Definir variables de entorno

Definir las variables de entorno ``ORACLE_HOME``, ``LD_INCLUDE_PATH`` y
``NLS_LANG`` dentro del fichero ``/etc/environment``. (Ojo porque este
fichero no es parte de un script de shell ni nada de eso, no entiende
variables definidas antes ni nada, solo parejas nombre="valor"). Si
además queremos activar el cgi traceback por defecto, definir también la
variable de entorno ``PYTHON_CGITB_ENABLE`` con un valor verdadero, si
se desea.

Debería quedar algo así:

.. code::

    IPATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/opt/oracle"
    ORACLE_HOME="/opt/oracle"
    LD_INCLUDE_PATH="/opt/oracle"
    NLS_LANG="SPANISH_SPAIN.WE8MSWIN1252"
    PYTHON_CGITB_ENABLE="yes"

Quinto: Crear fichero ``tnsnames.ora``

Creamos en ``$ORACLE_HOME`` el directorio ``network/admin`` y dentro
creamos el fichero ``tnsnames.ora``, cuyo contenido (para acceder a la
instancia de oracle en ORACLE) es tal que así:

.. code:: shell

    ORACLE = 
        (DESCRIPTION =  (
            ADDRESS = (
                PROTOCOL = TCP
                )
            (HOST = <hostname>)
            (PORT = <port:1521>))
        (CONNECT_DATA =
            (SERVER = DEDICATED)
            (SERVICE_NAME = srv-oracle)
        )
    )

Sexto: Incluir librerías

Hay que incluir la referencia a las librerías en el directorio
``/etc/ld.so.conf.d``, por ejemplo, con el siguiente comando:

.. code:: shell

    sudo sh -c "echo /opt/oracle >> /etc/ld.so.conf.d/instant_client.conf"

y luego ejecutar:

.. code:: shell

    sudo ldconfig

Creo que este paso hace que no tengamos que definir la variable de
entorno ``LD_LIBRARY_PATH``, pero no estoy seguro.

Séptimo: Definir Parámetros de conexión

También es conveniente definir algunos parámetros de la conexión,
incluyendo un archivo ``sqlnet.ora`` en el mismo directorio que el
``tnsnames.ora``, con los siguientes valores:

.. code::

    SQLNET.EXPIRE_TIME = 60
    SQLNET.OUTBOUND_CONNECT_TIMEOUT = 60
    SQLNET.ALLOWED_LOGON_VERSION = 10


Cómo obtener el código fuente de una función
-----------------------------------------------------------------------

Si sabemos el propietario (``OWNER``) y nombre de la función, podemos
hacer:

.. code:: sql

    SELECT text
      FROM all_source
     WHERE name = 'funcion'
       AND owner = 'propietario'
     ORDER BY line;

Fuente: `plsql - How to see PL/SQL Stored Function body in Oracle <https://stackoverflow.com/questions/14212295/`_


Como ocultar/mostrar los nombres de los campos en SqlPlus
-----------------------------------------------------------------------

Por defecto se muestran los nombres de las columnas en la salida de
SqlPlus. Podemos ocultarlas con el comando:

.. code::

    SET HEADING OFF

Para volver a verlos:

.. code::

    SET HEADING ON

Si no aparece, mirar la variable ``PAGESIZE``. Si esta a ``0`` tampoco
se muestran los nombres de las columnas.

Cómo saber qué huso horario (*time zone*) está usando Oracle
-----------------------------------------------------------------------

Para saber en que huso horario o *timezone* cree Oracle que está,
podemos usar la siguiente sentencia SQL:

.. code:: sql

    SELECT DBTIMEZONE FROM DUAL;

Por otro lado, la sesión con la que estamos conectados puede estar
usando otro valor diferente. Para saber el *timezone* de la sesión, el
comando SQL es:

.. code:: sql

    SELECT SESSIONTIMEZONE FROM DUAL;

Cómo cambiar el huso horario o *time zone* por defecto en Oracle
-----------------------------------------------------------------------

Necesitamos cambiar la base de datos con un comando ``ALTER DATABASE``:

.. code:: sql

    ALTER DATABASE SET TIME_ZONE='Atlantic/Canary';

Si queremos especificar la diferencia con UTC en vez de usar nombres,
podemos usar:

.. code:: sql

    ALTER DATABASE SET TIME_ZONE='-04:00';

Fuentes:

- `Check and Set the Database and Session Time Zone in Oracle <https://linuxhint.com/check-and-set-the-database-and-session-time-zone-in-oracle/>`_

Cómo volver a compilar un procedimiento almacenado en Oracle
-----------------------------------------------------------------------

Para compilar un procedimiento se usa la sentencia ``ALTER PROCEDURE``.
Por ejemplo, para compilar el procedimiento ``CIERRE_LIQUIDA``,
perteneciente a ``PRODUCTIVIDAD``, ejecutaríamos la siguiente sentencia:

.. code:: sql

    ALTER PROCEDURE productividad.cierre_liquida COMPILE;

Si Oracle no encuentra errores de compilación (
Ver :ref:`como_ver_los_errores_de_compilacion_de_oracle`), el
procedimiento pasará a estado válido. Se puede comprobar el estado del
procedimiento usando:


.. code:: sql

    SELECT object_type, object_name, status
      FROM sys.dba_objects
     WHERE object_type = 'PROCEDURE'
       AND object_name = 'CIERRE_LIQUIDA'
       AND owner = 'PRODUCTIVIDAD';

Debería devolver ``VALID`` en el campo ``status``.

Cómo saber el nombre de la instancia de la base de datos
-----------------------------------------------------------------------

Si tenemos acceso por SQL:

.. code:: sql

    SELECT host_name
    FROM v$instance

Si no tenemos acceso a las vistas ``v$...`` también puede funcionar:

.. code:: sql

    SELECT utl_inaddr.get_host_name
      FROM dual

O esta otra:

.. code:: sql

    SELECT sys_context('USERENV','SERVER_HOST')
    FROM dual

Cómo saber la versión del gestor de base de datos en Oracle
-----------------------------------------------------------------------

Usando el siguiente comando SQL:

.. code:: sql

    SELECT * FROM v$version;

Fuente: `Comando para saber la versión de la base de datos ORACLE, MS SQL SERVER, MYSQL <https://marcelitux.wordpress.com/2011/11/16/comando-para-saber-la-version-de-la-base-de-datos-oracle-ms-sql-server-mysql/>`_

.. _como_ver_los_errores_de_compilacion_de_oracle:

Cómo ver los errores de compilación de Oracle
-----------------------------------------------------------------------

En sqlplus:

.. code: shell

    show errors

Fuente: `How to see errors after compilation - Oracle forums <https://forums.oracle.com/ords/apexds/post/how-to-see-errors-after-compilation-3248>`_
