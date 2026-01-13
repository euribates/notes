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


¿Qué es un CASLIB?
------------------------------------------------------------------------

Una **CASLIB** es una biblioteca que puede contener cero o más tablas
CAS.

Una CASLIB está asociado a una fuente de datos desde la cual el servidor
puede acceder a los datos. Proporciona información de conexión a la
fuente de datos, y tiene controles de acceso asociados que definen qué
grupos y usuarios individuales pueden usar el CASLIB.

La arquitectura del servidor añade automáticamente las CASlibs
personales. Además, cada usuario autenticado tiene dos CASlibs: una para
su directorio personal (``CASUSER``) y otra para el directorio
``/user/userid`` en HDFS (CASUSERHDFS), si se trata de un CAS
distribuido.

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


.. _ISO-8601: https://es.wikipedia.org/wiki/ISO_8601
