ckan
========================================================================

.. tags:: opendata,foss,python

.. contents:: Relación de contenidos
    :depth: 3


Qué es :index:`CKAN`
------------------------------------------------------------------------

**CKAN** es una herramienta para crear sitios web de datos abiertos.
Como un gestor de contenidos, del estilo de *Wordpress*, pero para
datos. En vez de páginas, publica colecciones de datos.

Una vez que los datos han sido publicados, los usuarios pueden realizar
búsquedas segmentadas para navegar y localizar los datos que necesitan,
y previsualizarlos usando mapas, gráficos y tablas.


CKAN es `código abierto`_, desarrollado por la Open Knowledge
Foundation (`OFKN`_).

Algunas caractersitcas claves de CKAN son:

- Publicación y compartición de datos

- Visualización de conjuntos de datos

- Control de acceso y gestión de usuarios

- Acceso mediante API para desarrolladores

- Soporte de plugins para ampliar funcionalidades


.. _OFKN: https://okfn.org/en/


Qué es un DataSet en CKAN
------------------------------------------------------------------------

En CKAN, los datos se publican en unidades llamadas **datasets**.

Un **dataset** es un conjunto de datos, por ejemplo, puede ser
estadísticas de crímenes acumulados por región, los gastos de un
departamento gubernamental, o las lecturas de temperatura de diferentes
estaciones meteorológicas. Los resultados de las búsquedas de un
usuario siempre son *datasets*.

Un *dataset* consta de dos partes:

- Los **Metadatos**, es decir, la información acerca de los datos.
  Ejemplos pueden ser el autor, la fecha, el formato o formatos en los
  que están disponibles los datos, la licencia que regula su uso, etc.

  Todos los metadatos en CKAN se almacenan versionados. A cada versión se
  la llama **revisión**.

- Un número de **recursos** (*resources*) que contiene los datos en si.
  A CKAN no le importa demasiado el formato que se haya usado:
  puede ser un fichero CSV, una hoja de cálculo, un fichero XML,
  un documento PDF, una imagen, datos enlazados en formato :term:`RDF`,
  etc.

CKAN puede almacenar los datos localmente, o solo guardar el
enlace a los mismos, residiendo los datos, por tanto, en otro sitio.

Un *dataset* puede contener un número arbitrario de recursos. Por
ejemplo, puede usar diferentes recursos para segmentar los datos por
año, o pueden usarse también para almacenar los mismo datos, pero en
diferentes formatos.

Nota: En versiones anteriores, los *datasets* eran llamados *packages*,
y ese nombre todavía puede encontrarse en algunas partes, como en la
documentación, llamadas –especialmente internas– de la API. Hay que
considerarlos como sinónimos.

Qué es el catálogo
------------------------------------------------------------------------

Se denomina **catálogo** a el conjunto de todos los *datasets*.


Usuarios, organización y autorización
------------------------------------------------------------------------

Los usuarios de CKAN pueden registrar cuentas e iniciar sesión.
Normalmente (dependiendo de la configuración del sitio), no se necesita
iniciar sesión para buscar y encontrar datos, pero sí para todas las
funciones de publicación: los conjuntos de datos pueden ser creados,
editados, etc., por usuarios con los permisos adecuados.

Normalmente, cada conjunto de datos pertenece a una organización. Una
instancia de CKAN puede tener cualquier número de organizaciones. Por
ejemplo, si CKAN se utiliza como portal de datos por un gobierno
nacional, las organizaciones podrían ser diferentes departamentos
gubernamentales, cada uno de los cuales publica datos. Cada organización
puede tener su propio flujo de trabajo y autorizaciones, lo que le
permite gestionar su propio proceso de publicación.

Los administradores de una organización pueden agregar usuarios
individuales, con diferentes roles según el nivel de autorización
necesario. Un usuario de una organización puede crear un conjunto de
datos propiedad de dicha organización. En la configuración
predeterminada, este conjunto de datos es inicialmente privado y solo es
visible para otros usuarios de la misma organización. Cuando esté listo
para su publicación, se puede publicar con solo pulsar un botón. Esto
puede requerir un nivel de autorización más alto dentro de la
organización.

.. note:: La guía del usuario abarca todas las funciones principales
   de la interfaz de usuario web (IU). En la práctica, dependiendo de la
   configuración del sitio, algunas de estas funciones pueden ser
   ligeramente diferentes o no estar disponibles. Por ejemplo, en una
   instancia oficial de CKAN en un entorno de producción, el
   administrador del sitio probablemente haya impedido que los usuarios
   creen nuevas organizaciones a través de la IU. Puede probar todas las
   funciones descritas en http://demo.ckan.org.

Cómo instalar CKAN (Desde las fuentes)
------------------------------------------------------------------------

Primero, instalar el software extra necesario
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suponemos linux Ubuntu o derivado:

.. code::  shell

    $ sudo apt-get install python3-dev libpq-dev python3-pip \
                   python3-venv git-core redis-server \
                   libmagic1

Crear un entorno virtual de Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Crear un entorno virtual de Python sobre el que ejecutar
CKAN, y activarlo:

.. code:: shell

    sudo mkdir -p /usr/lib/ckan/default
    sudo chown `whoami` /usr/lib/ckan/default
    python3 -m venv /usr/lib/ckan/default
    source /usr/lib/ckan/default/bin/activate
    pip install --upgrade pip


Instalar el código fuente de CKAN en el entorno virtual
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nos traemos el repositorio de CKAN:

.. code:: shell

   gh repo clone ckan/ckan

Instalamos las dependencias del fichero de ``requirements.txt`` del repo:

.. code:: shell

    pip install -r ckan/requirements.txt

Y finalmente instalamos CKAN, en modo de desarrollo local:

.. code:: shell

   pip install -r ckan/

Crear la base de datos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comprobamos que PostgreSQL está instalado correctamente con la siguiente
orden:

.. code:: shell

   sudo -u postgres psql -l

Que lista las bases de datos disponibles.

Ahora creamos la base de datos. Es importante especificar la
codificación como UTF-8. Vamos a crear una base de datos con el
nombre ``ckan``, con un usuario ``ckan_user``:

.. code:: 

    sudo -u postgres createuser -S -D -R -P ckan_user

Esta línea preguntará por el *password* del usuario. Hay que recordarlo
para la posterior cobfiguración. Una vez creado el usuario que va a ser
el propietario de la base de datos, podemos crearla con:

.. code:: 

   sudo -u postgres createdb -O ckan_user ckan -E utf-8

Creamos el fichero de configuración de CKAN
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creamos un directorio para almacenar los fichero de configuración:

.. code:: shell

   sudo mkdir -p /etc/ckan/default
   sudo chown -R `whoami` /etc/ckan/

Creamos el fichero de configuración ``ckan.ini``:

.. code:: shell

   ckan generate config /etc/ckan/default/ckan.ini

Cambiar en el fichero de configuración los siguientes valores:

- La ruta de la base de datos:

  .. code::

     sqlalchemy.url = postgresql://ckan_user:<password>@localhost/ckan

- El identificador del sitio:

  Todos los servidores de CKAN necesitan un identificador propio:

  .. code::

      ckan.site_id = pruebas_ckan

- URL pública

  En la variable ``ckan.site_url`` va la URL publica de nuestro servidor
  CKAN

  .. code::

      ckan.site_url = http://demo.ckan.org

Instalar Solr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CKAN utiliza Solr_ como motor de búsqueda. Ahora que tenemos CKAN
instalado, debemos instalar y configurar Solr.

Vamos a instalarlo con Docker, ya que es la forma más fácil y esta guía se
centra sobre todo en instalar CKAN:

.. code::

   docker run --name ckan-solr -p 8983:8983 -d ckan/ckan-solr:2.11-solr9

Creamos el esquema de la base de datos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Con los parámetros correctos en el fichero de configuración, podemos
crear el esquema en la base de datos con:

.. code:: shell

   ckan -c /etc/ckan/default/ckan.ini db init

Creamo un usuario admin o root
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Las ordenes para gestionar usuario de CKAN son:

- ``ckan user add``         : Añadir un nuevo usuario
- ``ckan user list``        : Listar todos los usuarios
- ``ckan user remove``      : Borrar un usuario
- ``ckan user setpass``     : Asignar un *password* a un usuario
- ``ckan user show``        : Ver detalles de un usuario

Por ejemplo, para crear un nuevo usuario ``admin``:

.. code::

   ckan -c /etc/ckan/default/ckan.ini user add admin email=admin@localhost

Nota: Falló en mis pruebas, tuve que crear a mano el siguiente
directorio:

.. code:: 

   sudo mkdir -p /var/lib/ckan/default/storage/uploads/user


.. _Solr: https://solr.apache.org/



Cómo instalar CKAN (Usando Docker)
------------------------------------------------------------------------

El repositorio ``ckan-docker`` contiene todo lo necesario para instalar
CKAN mediante *Docker Compose*. La imagen viene configurada con las
extensiones ``Filestore`` y ``DataStore``, pero se le pueden añadir (y
personalizar) más extensiones.

Si bien se centra en un entorno de desarrollo, puede utilizarse como
base para avanzar a un entorno de producción. Tenga en cuenta que un
sistema de producción de CKAN completo con contenedores Docker queda
fuera del alcance de la configuración proporcionada.

Le recomendamos instalar CKAN desde Docker Compose si está en alguno de
estos casos:

- Desea instalar CKAN con menos esfuerzo que una instalación de
  código fuente pero con mayor flexibilidad que una instalación de
  paquete

- Desea ejecutar o incluso desarrollar extensiones con un mínimo
  esfuerzo de configuración

- Desea comprobar si CKAN, Docker y su infraestructura se integran, y
  de qué manera.

Fuentes:

- `Configuration and setup files to run a CKAN site`_

- `Official Docker images for CKAN`_

.. _Configuration and setup files to run a CKAN site: https://github.com/ckan/ckan-docker
.. _Official Docker images for CKAN: https://github.com/ckan/ckan-docker-base


La API de CKAN
------------------------------------------------------------------------

Las APIs de CKAN están versionadas. Si se hace una solicitud sin
especificar la versión, CKAN utilizara la última versión publicada.

    http://demo.ckan.org/api/action/package_list

Para especificar la versión, la incluimos en la URL de la petición, como
en el siguiente ejemplo:

    http://demo.ckan.org/api/3/action/package_list


Se pueden agregar *datasets* mediante la interfaz web de CKAN, pero al
importar muchos conjuntos de datos, generalmente es más eficiente
y menos propenso a errores automatizar el proceso de alguna manera.

Aquí hay un ejemplo de un *script* de Python que utiliza el paquete
`ckanapi`_ para importar conjuntos de datos a CKAN.

.. code:: python

    import pprint
    from ckanapi import RemoteCKAN

    # Create a connection to the CKAN site with your API token
    # Replace 'your-api-token' with your actual API token
    ckan = RemoteCKAN('http://www.my_ckan_site.com', apikey='your-api-token')

    # Put the details of the dataset we're going to create into a dict.
    dataset_dict = {
        'name': 'my_dataset_name',
        'notes': 'A long description of my dataset',
        'owner_org': 'org_id_or_name'
        }

    # Use the ckanapi action shortcut to create a new dataset
    created_package = ckan.action.package_create(**dataset_dict)

    # See the result
    pprint.pprint(created_package)


.. _ckanapi: https://github.com/ckan/ckanapi
