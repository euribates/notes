SAS-Viya
========================================================================

.. tags:: statistics,api,ia


¿Qué es SAS Viya?
------------------------------------------------------------------------

**SAS Viya** es una plataforma de análisis, gestión de datos e
inteligencia artificial desarrollado por `SAS Institute <>`__.

Cómo listar los grupos de usuarios
------------------------------------------------------------------------

.. code:: shell

    sudo sas-viya identities list-groups

Cómo ver los detalles de un grupo
------------------------------------------------------------------------

.. code:: shell

    sudo sas-viya identities show-group --id <id. del grupo>

Cómo listar los usuarios
------------------------------------------------------------------------

.. code:: shell

    sudo sas-viya identities list-users


Cómo ver los detalles de un usuario
------------------------------------------------------------------------

.. code:: shell

    sudo sas-viya identities show-user --id <username>


.. index:: single:caslib; SAS
¿Qué es un CASLIB?
------------------------------------------------------------------------

Una biblioteca CAS, o **CASLIB**, es un contenedor con dos áreas
principales: un área para tablas en memoria y otra área para archivos
de origen de datos. Los archivos de origen de datos pueden ser
SAS, CSV, Hadoop, Microsoft Excel y una variedad de bases de datos.

Una **CASLIB** puede contener cero o más tablas.

Toda CASLIB está asociada a una fuente de datos desde la cual el servidor
puede acceder a los datos. Proporciona información de conexión a la
fuente de datos, y tiene controles de acceso asociados que definen qué
grupos y usuarios individuales pueden usar el CASLIB.

La arquitectura del servidor añade automáticamente las CASlibs personales.
Además, cada usuario autenticado tiene otras dos: una para su directorio
personal (``CASUSER``) y otra para el directorio ``/user/userid`` en HDFS
(CASUSERHDFS), si se trata de un CAS distribuido.

El atributo ``LOCAL`` de un CASLIB indica su alcance, que puede ser local
o global. Cuando se define ``LOCAL=YES``, el ámbito del CASLIB es el de la
sesión. En este caso, solo está accesible desde la sesión CAS donde se
creó, y cuando la sesión CAS termine, se eliminará también el CASLIB.
Estos CASLIBS son útiles cuando **no se necesita compartir datos**.

Si, por el contrario, definimos ``LOCAL=NO``, el ámbito del CASLIB sera global.
Estos CASLIBS estarán siempre disponibles,  y están compartidos por todos
los usuarios y aplicaciones que inicien sesión. Lógicamente, no son
borrados cuando termina la sesión.


Cómo crear una CASLIB de conexión a PostgreSQL
------------------------------------------------------------------------

Solo pueden crear estas CASLIB los usuarios que pertenezcan al grupo *SAS
Administrators*.

- Crear una nueva conexión pinchando con botón derecho sobre *cas-shared-
  default*:

- Dentro de la pestaña *All* seleccionar el Data Source *PostgreSQL*

- Especificar los parámetros de conexión:

  * Nombre de la conexión (El que queramos)
  * Nombre corto
  * Dirección o nombre del servidor
  * Puerto
  * Nombre de la base de datos
  * Nombre del esquema
  * Usuario y *password*

  Se puede probar lo conexión con *Test connection*.

Cómo crear una CASLIB de conexión a Oracle
------------------------------------------------------------------------

Solo pueden crear estas CASLIB los usuarios que pertenezcan al grupo *SAS
Administrators*.

- Crear una nueva conexión pinchando con botón derecho sobre *cas-shared-
  default*:

- Dentro de la pestaña *All* seleccionar *Oracle Database*

- Especificar los parámetros de conexión:

  * Nombre de la conexión (El que queramos)
  * Nombre corto
  * Marcar la opción de *Global (Shared)*
  * Dirección o nombre del servidor
  * Puerto
  * Nombre de la base de datos
  * Nombre del esquema
  * Usuario y *password*

  Se puede probar lo conexión con *Test connection*.



Qué nodos de SAS-Viya necesitan acceso a las servidores de bases de datos
-------------------------------------------------------------------------

Desde los servidores **Compute**, **CAS Controller**, y **CAS Workers**.
Esta conectividad ya está pedida dado que las Caslibs ya están creadas y
validadas su acceso a las fuentes de datos correspondientes.

Cómo saber que ``plugins`` tiene instalados el cliente de SAS-Viya
------------------------------------------------------------------------

Con el comando:

.. code:: shell

    sudo sas-viya plugins list


Cómo vincular un grupo Unix local a un grupo de usuarios en SAS-Viya
------------------------------------------------------------------------

Necesitamos usar el comando ``update-group`` del *plugin*
``identities``. Por ejemplo para vincular el grupo local :math:`2005`
con el grupo de SAS-Viya ``CAPJS-DGTNT-HiperReg-D``, el comando sería:

.. code:: shell

    sudo sas-viya --output text identities update-group --id "CAPJS-DGTNT-HiperReg-D" --gid 2005


Cómo listar los grupos de usuarios creados en SAS-Viya
------------------------------------------------------------------------

Con ``sas-cli`` podemos listar los grupos de usuarios, (necesitamos
tener instalado el ``plugin`` ``identities``):

.. code:: shell

    sudo ./sas-viya --output text identities list-groups

El *flag* ``--after`` puede ser de utilidad, solo lista los grupos
creados a partir de una determinada fecha. La fecha tiene que ir en
formato `ISO-8601`_. Por ejemplo ``2025-10-27T13:00:00Z`` para
indicar el 27 de octubre de 2025, a partir de la una de la tarde.

.. code:: shell

    sudo ./sas-viya --output text identities list-groups --after 2025-10-27T13:00:00Z

El lenguajes SAS
------------------------------------------------------------------------

Consiste en una serie de sentencias (*statements*), terminados con el
carácter punto y coma (``;``). La indentación es opcional, ya que no tiene
valor semántico. Los nombre de las variables no distinguen entre
mayúsculas y minúsculas.

.. code:: sas

    data class_report;
        set sashelp.class;
        if sex = 'F';
    run;

Consta de dos partes diferentes: ``DATA`` y ``PROC``, que veremos más
adelante.

Para comentar el código, hay dos formas: Empezar con un asterisco (``*``)
y terminar con un punto y coma (``;``), apto para comentar líneas, y
comenzar con la secuencia ``/*`` y terminar con ``*/``, apto para comentar
bloques de código.

La sección ``DATA``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Los datos en SAS tiene naturaleza tabular. Las columnas son llamadas
**variables**, mientras que las filas se denominan **observaciones** o a
veces *data points*. Los conjuntos de datos o *Data sets* son la
combinación de los dos.

Los tipos de datos son principalmente texto o números. Los valores de
texto pueden almacenar hasta 32767 caracteres. En los data sets se
muestran alineados a la izquierda. Los números pueden ser enteros o en
coma flotante, y se alinean por defecto a la derecha.

Los nombres de variables tienen como máximo 32 caracteres, deben empezar
con una letra o subrayado, y no aceptan ningún otro carácter especial. El
resto de caracteres aparte del primero pueden también usar dígitos.

Si un dato de texto falta, se marca con una cadena vacía. Si son datos
numéricos, se usa un punto ``.``.


La sección ``PROC``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``DATA`` da pasos para crear o modificar los SAS *Data sets*

- ``PROC`` realiza procesos de análisis, visualización y generación de informes

Los dos consisten en sentencias, pero ciertas sentencias son específicas
de cada etapa


Librerías en SAS
------------------------------------------------------------------------

Las libreras se refieren a *data sets*.
Hay tres librerías predefinidas:

- ``WORK`` para *data sets* temporales y de trabajo.

- ``SASHELP`` contiene *data sets* de ejemplo, que se pueden usar para
  aprender. Es de solo lectura.

- ``SASUSER`` Donde se pueden almacenar los *data sets* del usuario.

Se pueden crear otras librerías con ``LIBNAME``:

.. code:: sas

    libname mydata '/home/euribates/mylib';
    run;

El nombre de la librería no puede tener más de 8 caracteres, letras,
dígitos o el carácter subrayado, excepto que el primer caracter no puede
ser un dígito.


.. _ISO-8601: https://es.wikipedia.org/wiki/ISO_8601


