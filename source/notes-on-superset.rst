Superset
========================================================================

.. tags:: opendata,foss

:index:`Superset`` is a modern data exploration and data visualizatioon
platform.  Superset can replace or augment proprietary business
intelligence tools for many teams. Superset integrates well with a variety
of data sources.


Ventajas de Superset
------------------------------------------------------------------------

- Posibilidad de crear gráficas con una interfaz visual, sin código.

- Un editor web, basado en SQL, para consultas avanzadas.

- Un nivel semántico ligero para definir de forma rápida métricas y
  dimensiones personalizadas.

- Soporte para casi todas las bases de datos.

- Un catálogo de diferentes diagramas, desde sencillas gráficas de barras
  a visualizaciones geo-espaciales.

- Sistema de caches ligero y configurable, para aliviar la carga de las
  bases de datos.

- Autenticación y roles de seguridad, extensibles.

- Una API para personalización mediante programas

- Una rquitectura nativa *cloud*, diseñada desde un principio pensando en
  la escalabilidad.


Ejecutar Superset en Docker
-----------------------------------------------------------------------

.. code:: shell

    $ docker run -i -p 8088:8088 --add-host host.docker.internal:host-gateway --name superset vizdata:latest

Para crear un usuario administrador:
------------------------------------------------------------------------
.. code::

    superset fab create-admin

Usar plantillas para el código SQL
------------------------------------------------------------------------

Se puede usar el sistema de plantillas de Jinja2 para personalizar las
consultas SQL tanto en el SQl Lab como en *datasets* virtuales. Esta
capacidad debe ser activada/permitida el *flag*
``ENABLE_TEMPLATE_PROCESSING``. Existen funciones predefinidas que
podemos usar desde Jinja2, como por ejemplo ``current_username()``, que
nos devuelve el ``username`` del usuario conectado, o
``current_user_roles()``, que devuelve una lista Python con los roles
que tiene habilitados.

.. code:: jinja2

    {% if 'Finance' in current_user_roles() %}revenue{% else %}NULL{% endif %} AS finance_revenue

Se pueden definir parámetros personalizados en SQL Lab mediante el menú
de parámetros, especificandolo en JSON:


.. code:: json

   {
     "my_table": "sales",
     "start_date": "2024-01-01"
   }

Que despues pueden ser referencias en la consulta:

.. code:: sql

   SELECT *
     FROM {{ my_table }}
    WHERE order_date >= '{{ start_date }}'


Podemos usar los bloques lógicos de Jinja:

.. code:: sql

   SELECT *
     FROM orders
    WHERE 1 = 1
     {% if start_date %}
      AND order_date >= '{{ start_date }}'
     {% endif %}
     {% if end_date %}
      AND order_date < '{{ end_date }}'
     {% endif %}
    ...


Pass custom values via URL query strings:

.. code:: slq

   SELECT *
     FROM orders
    WHERE country = '{{ url_param('country') }}'

Acederiamos, por ejemplo, con ``superset.example.com/sqllab?country=US``
