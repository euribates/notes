Meilisearch
========================================================================

.. tags:: python,web,linux,systemd,rust


Sobre Meilisearch
-----------------------------------------------------------------------

**MeiliSearch** es un motor de búsqueda de texto rápido, de fácil uso y
despliegue.

.. warning:: No tiene operadores lógicos

    En la versión $1.7.2$ no incluye operadores lógicos (`and`, `or`, `not`).
    Se espera que la version $1.8$ incluya el operador `not`. A fecha
    12/ene/2026 ya van por la versión 1.31.0.


Algunas de las características más interesantes son las siguientes:

- **Búsqueda mientras se teclea**: Encuentra resultados en menos de 50
milisegundos

- **Tolerancia a errores**: Encuentra resultados relevantes aunque haya
errores en el texto buscado.

- **Múltiples posibilidades de ordenación**: Se puede ordenar por
precios, fechas, o cualquier otro campo que se defina.

- **Filtrado** y **búsquedas refinadas**: Se pueden ir modificando las
consultas basándonos en las anteriores, para ir construyendo consultas
más complicadas.

- **Sinónimos**

- **API Resftul**

- **Fácil de instalar, personalizar y desplegar**

- Escrito en `Rust <notes-on-rust.md>`__.

Instalar Meilisearch en Ubuntu
-----------------------------------------------------------------------

Bajamos el *script* de instalación:

.. code:: shell

    sudo wget -qO /usr/local/bin/meilisearch https://github.com/meilisearch/meilisearch/releases/latest/download/meilisearch-linux-amd64
    sudo chmod a+x /usr/local/bin/meilisearch

Comprobemos la versión con:

.. code:: shell

    meilisearch --version

Debería producir:

.. code::

    meilisearch-http 1.31.0

Ver ahora `Como pasar Meilisearch a producción <#como-pasar-meilisearch-a-produccion>`_


Cómo instalar el cliente Python de Meilisearch
-----------------------------------------------------------------------

Esta es fácil:

.. code:: shell

    pip install meilsearch

Cómo configurar Meilisearch
-----------------------------------------------------------------------

Se puede configurar desde la línea de comandos, mediante variables de
entorno o con un fichero de configuración. Esta configuración afectara a
**todo** los índices.

Las opciones de línea de comando tiene precedencia sobre las variables
de entorno.


Qué es un índice (``index``) para Meiliseacrh
-----------------------------------------------------------------------

Un **índice** es un grupo de documentos, similar a una tabla o relación
en una base de datos. Un índice se define dándole un identificador único
(``uid``), y debe contener la siguiente información:

- La clave primaria
- Varios ajustes de configuración
- Un número arbitrario de documentos

Crear un índice y actualizar documentos
-----------------------------------------------------------------------

Aunque todas las peticiones a Meilisearch se pueden hacer mediante
peticiones a la API Web, también podemos usar las librerías de Python.

En este ejemplo suponemos que tenemos un servidor de Meilisearch
instalado y ejecutándose, escuchando en la máquina local en el puerto
:math:`7700`.

Vamos a usar una base de datos de películas que se puede descargar desde
aquí: `The movie
database <https://www.notion.so/meilisearch/A-movies-dataset-to-test-Meili-1cbf7c9cfa4247249c40edfa22d7ca87#b5ae399b81834705ba5420ac70358a65>`_.

Descargemos la base de datos en formato json al fichero ``movies.json``.

.. code:: shell

    curl -L https://docs.meilisearch.com/movies.json -o movies.json

Ahora, para crear el índice y alimentarlo con Curl:

.. code:: shell

    curl -i -X POST 'http://127.0.0.1:7700/indexes/movies/documents' \
         --header 'content-type: application/json' \
         --data-binary @movies.json


Si se referencia un índice inexistente, Meilisearch lo creará
automáticamente. Esto no siempre es deseable, porque hay ajustes que
asumirá y cuyo valor por defecto puede que no nos interesen.

En el ejemplo de Curl, si no se ha creado el índice antes, se creará
automáticamente un nuevo índice con ``uid`` **``movies``**.

Para crear un índice con la interfaz Python, haremos uso del método
``create_index``:

.. code:: python

    client.create_index('movies', {'primaryKey': 'id'})

En este caso, hemos especificado que la clave primaria para los
documentos será el campo ``id``. Como casi todas las llamadas, esta es
*asíncrona*, así que el valor que nos devuelve es un ``taskUid``: un
identificador de la tarea que podemos usar para 
`Comprobar el estado de una petición`_

Una vez credo el índice, sus parámetros por defecto no se pueden
cambiar. Tampoco podremos crear otro índice con el mismo `uid`.

Consultas usando la web
-----------------------------------------------------------------------

Se puede usar directamente la API web para realizar consultas, usado
curl (y ``jq`` en el ejmplo para mejorar la presentación del json
generado:

.. code:: shell

    curl 'http://127.0.0.1:7700/indexes/movies/search?q=botman+robin&limit=2' | jq

Produciría algo como:

.. code:: js

    {
    "hits": [
        {
            "id": "415",
            "title": "Batman & Robin",
            "poster": "https://image.tmdb.org/t/p/w1280/79AYCcxw3kSKbhGpx1LiqaCAbwo.jpg",
            "overview": "Along with crime-fighting partner Robin and new recruit Batgirl, Batman battles the dual threat of frosty genius Mr. Freeze and homicidal horticulturalist Poison Ivy. Freeze plans to put Gotham City on ice, while Ivy tries to drive a wedge between the dynamic duo.",
            "release_date": 866768400
        },
        {
            "id": "411736",
            "title": "Batman: Return of the Caped Crusaders",
            "poster": "https://image.tmdb.org/t/p/w1280/GW3IyMW5Xgl0cgCN8wu96IlNpD.jpg",
            "overview": "Adam West and Burt Ward returns to their iconic roles of Batman and Robin. Featuring the voices of Adam West, Burt Ward, and Julie Newmar, the film sees the superheroes going up against classic villains like The Joker, The Riddler, The Penguin and Catwoman, both in Gotham City… and in space.",
            "release_date": 1475888400
        }
    ],
    "nbHits": 8,
    "exhaustiveNbHits": false,
    "query": "botman robin",
    "limit": 2,
    "offset": 0,
    "processingTimeMs": 2
    }

Crear un índice en Meilisearch con Python
-----------------------------------------------------------------------

Para crear un índice en Meilisearch, hay que asignarle un nombre y
decirle el atributo que debe usar como clave primaria. Por ejemplo:

.. :: Python

    import meilisearch

    client = meilisearch.Client('http://127.0.0.1:7700', 'masterKey')
    client.create_index('notes', {'primaryKey': 'id'})


Añadir documentos a un índice Meilisearch con Python
-----------------------------------------------------------------------

Con el método ``add_documents`` podemos añadir una secuencia de
documentos al índice. Ejemplo:

.. code:: python

    import meilisearch

    client = meilisearch.Client('http://127.0.0.1:7700', 'masterKey')

    # An index is where the documents are stored.
    index = client.index('movies')

    documents = [
        { 'id': 1, 'title': 'Carol', 'genres': ['Romance', 'Drama'] },
        { 'id': 2, 'title': 'Wonder Woman', 'genres': ['Action', 'Adventure'] },
        { 'id': 3, 'title': 'Life of Pi', 'genres': ['Adventure', 'Drama'] },
        { 'id': 4, 'title': 'Mad Max: Fury Road', 'genres': ['Adventure', 'Science Fiction'] },
        { 'id': 5, 'title': 'Moana', 'genres': ['Fantasy', 'Action']},
        { 'id': 6, 'title': 'Philadelphia', 'genres': ['Drama'] },
        ]

    # If the index 'movies' does not exist, Meilisearch creates it when you first add the documents.
    index.add_documents(documents) # => { "uid": 0 }

Consultar un índice con Python
-----------------------------------------------------------------------

Primero, tenemos que instalar el cliente para meilisearch, si no
estuviera ya instalado:

.. code:: shell

    pip install meilisearch

El siguiente ejemplo muestra una consulta sencilla:

.. code:: python

    import datetime
    import meilisearch

    client = meilisearch.Client('http://127.0.0.1:7700')
    index = client.index('movies')
    for movie in index.search('spiderman')['hits']:
        release_date = datetime.datetime.utcfromtimestamp(movie['release_date'])
        print(movie['title'], release_date.year)

Debería producir un resultado similar a este:

.. code::

    Spider-Man: Into the Spider-Verse 2018
    Spider-Man: Homecoming 2017
    Spider-Man 2002
    Spider-Man 3 2007
    Spider-Man: Far from Home 2019
    Spider-Man 2 2004
    The Amazing Spider-Man 2 2014
    The Amazing Spider-Man 2012
    The Amazing Spider-Man 1978
    LEGO Marvel Super Heroes: Maximum Overload 2013
    LEGO Marvel Super Heroes: Avengers Reassembled! 2015


Cómo obtener un listado de los índices disponibles
-----------------------------------------------------------------------

Con el método ``get_indexes``:

.. code:: Python

    import meilisearch

    client = meilisearch.Client('http://localhost:7700', 'aSampleMasterKey')
    for idx in client.get_indexes():
        print(idx)


Cómo saber la versión de Meilisearch instalada
-----------------------------------------------------------------------

Se puede hacer desde la línea de comandos:

.. code:: shell

    $ meilisearch --version
    meilisearch-http 0.28.1

O desde la API web, si el servidor se está ejecutando, por ejemplo en:

.. code:: shell

    http://127.0.0.1:7700/version/

Nos daría la respuesta:

.. code:: js

    {
        "commitSha":"22aa349e31bc7662a065f4dc3229a93abd1f1f33",
        "commitDate":"2022-07-21T11:08:37Z",
        "pkgVersion":"0.28.1"
    }

Como pasar Meilisearch a producción
-----------------------------------------------------------------------

Necesitamos una versión de Linux moderna y un par de claves ssh.

1) Instalar Meilisearh

.. code:: shell

    curl -L https://install.meilisearch.com | sh
    sudo mv ./meilisearch /usr/bin
    sudo chmod a+x /usr/bin/meilisearch

Y ver que funciona:

.. code:: shell

    $ meilisearch --version
    meilisearch-http 0.29.2

2) Convertir meilisearh en un servicio

Usaremos `systemd <notes-on-systemd.rst>`__. Los servicios de ``systemd``
están definidos como ficheros de texto en ``/etc/systemd/system``. Para
ejecutar Meilisearch en modo servidor hay que usar la opción ``--env``.
Para definir la clave maestra se usa ``--masterkey``.

Cuando se ejecuta por primera vez, Meilisearch crea dos claves API:
``Default Admin API Key`` y ``Default Search API Key``. Usaremos la
primera para operaciones de mantenimiento como crear nuevos documentos,
índices, o cambios en la configuración, mientras que la segunda se usará
para las búsquedas.

Es conveniente modificar la configuración de meilisearch en
``/etc/meilisearch/config.toml`` y definir como mínimo los siguientes
valores:

- ``db_path``
- ``env``
- ``http_addr``
- ``master_key``

Ejemplo:

.. code::

    # Path to database indexes
    db_path = "/var/meilisearch/data.ms"

    # Enviroment
    env = "development" # `production` or `development`.

    # The address on which the HTTP server will listen.
    http_addr = "localhost:7700"

    # Sets the instance's master key
    # automatically protecting all routes except GET /health.
    # https://www.meilisearch.com/docs/learn/configuration/instance_options#master-key
    master_key = "747bdd8f-25c5-4be0-8d66-bf3c545de7c3"

Ahora el fichero en ``/etc/systemd/system/meilisearch.service`` podría
ser algo como esto:

.. code:: systemd

    [Unit]
        Description=Meilisearch
        After=systemd-user-sessions.service

    [Service]
        Type=simple
        ExecStart=/usr/local/bin/meilisearch --config-file-path /etc/meilisearch/config.toml

    [Install]
        WantedBy=default.target

En esta configuración el servidor está vinculado a la dirección
``127.0.0.1`` lo que significa que solo aceptará conexiones desde la
máquina local. En producción habría que ponerla en la IP ``0.0.0.0``.

Ahora arrancamos el servicio:

.. code:: bash

    $ sudo systemctl enable meilisearch.service
    $ sudo systemctl start meilisearch.service

Y comprobamos que esté funcionando:

.. code:: bash

    $ sudo systemctl status meilisearch.service

Debería producir algo parecido a:

.. code::

    ● meilisearch.service - Meilisearch
    Loaded: loaded (/etc/systemd/system/meilisearch.service; enabled; vendor preset: enabled)
    Active: active (running) since Wed 2022-11-23 11:30:09 WET; 1s ago
    Main PID: 30162 (meilisearch)
    Tasks: 10 (limit: 9256)
    Memory: 7.4M
    CPU: 47ms
    CGroup: /system.slice/meilisearch.service
    └─30162 /usr/bin/meilisearch --http-addr 127.0.0.1:7700 --env production --master-key Y0urVery>

    Nov 23 11:30:10 nova meilisearch[30162]: Thank you for using Meilisearch!
    Nov 23 11:30:10 nova meilisearch[30162]: We collect anonymized analytics to improve our product and your ex>
    Nov 23 11:30:10 nova meilisearch[30162]: Anonymous telemetry:        "Enabled"
    Nov 23 11:30:10 nova meilisearch[30162]: Instance UID:                "1d6ead4c-3d21-42d9-ba0b-b91b031c9bd5"
    Nov 23 11:30:10 nova meilisearch[30162]: A Master Key has been set. Requests to Meilisearch won't be author>
    Nov 23 11:30:10 nova meilisearch[30162]: Documentation:                https://docs.meilisearch.com
    Nov 23 11:30:10 nova meilisearch[30162]: Source code:                https://github.com/meilisearch/meilise>
    Nov 23 11:30:10 nova meilisearch[30162]: Contact:                https://docs.meilisearch.com/resources/con>
    Nov 23 11:30:10 nova meilisearch[30162]: [2022-11-23T11:30:10Z INFO  actix_server::builder] Starting 4 work>
    Nov 23 11:30:10 nova meilisearch[30162]: [2022-11-23T11:30:10Z INFO  actix_server::server] Actix runtime fo>

En este momento el sistema está funcionando y preparado para posibles
caídas, reinicias del sistema, etc.

3) Usar el sistema desde ``nginx``

Si queremos dar acceso directo al sistema en el puerto (:math:`7000`,
por defecto) probablemente tendremos que definir una entrada especifica
en ``nginx``.

Comprobar el estado de una petición
-----------------------------------------------------------------------

Sabiendo el ``taskUid`` de un tarea, podemos interrogar al índice con el
método ``get_task(task_id)``.

Cómo saber donde está guardando los índices Meilisearch
-----------------------------------------------------------------------

Meilisearch crea por defecto una carpeta llamada ``data.ms``, en la
misma carpeta en la que esté localizado el ejecutable ``meilisearch``.

La ubicación de la carpeta puede ser modificada ya sea mediante
parámetros, variables de entorno o un fichero de configuración.

Atributos visibles y buscables
-----------------------------------------------------------------------

Displayed and searchable attributes

Por defecto, al añadir cualquier documento a un índice todos los
atributos nuevos que se encuentren se añaden automáticamente a **dos**
listas: La lista de atributos visibles (*displayed*, es decir, que se
mostrarán en los resultados) y buscables (*searchable*, es decir, que se
usaran para las b↓squedas).

A causa de esto, todos los atributos son, por defecto, visibles y
buscables. Pero podemos modificar estos ajustes mediante la
configuración del índice.

Si se define la lista ``displayedAttributes``, entonces **solo** Los
campos cuyos nombres estén la lista serán visibles, y saldrán por lo
tanto en los resultados de las búsquedas.

De forma similar, si se define la lista ``searchableAttributes``, solo
se considerán los campos incluidos en la lista.

Ejemplo:

.. code:: python3

    client.index('movies').update_displayed_attributes([
        'title',
        'overview',
        'genres',
        'release_date'
        ])

Cómo usar filtros en Meilisearch
-----------------------------------------------------------------------

Los filtros se usan para refinar búsquedas y también son las bases para
las búsquedas segmentadas.

Supongamos una colección de películas que contenga los siguiente
títulos:

.. code:: js

    [
        {
            "id": 458723,
            "title": "Us",
            "director": "Jordan Peele",
            "genres": [
                "Thriller",
                "Horror",
                "Mystery"
                ],
            "rating": {
            "critics": 86,
            "users": 73
            },
            "overview": "Husband and wife Gabe and Adelaide Wilson take their…"
        },
        ...
    ]

Para filtrar por los campos de director (*director*) y géneros (*genres*),
primero hay que añadir ambos campos a la lista ``filterableAttributes``,
usando la llamada ``update_filterable_attributes``:

.. code:: Python

    client.index('movies').update_filterable_attributes(['director', 'genres'])

Este paso es **obligatorio**, ya que la lista ``filterableAttributes``
está vacía por defecto.

Es mejor establecer esto **en el momento de crear el índice**, ya que
implicar una reorganización del mismo, que podría llevar un tiempo
apreciable si contiene muchos documentos.
