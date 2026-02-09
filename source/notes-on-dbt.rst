DBT (*Data Build Tool*)
========================================================================


:index:`Dbt` (`Data Build Tool`_) es una solución de código
abierto diseñada específicamente para el modelado de datos, que
aprovecha plantillas SQL y funciones de referencia
para establecer relaciones entre varias instancias de bases de datos,
como tablas, vistas, esquemas, etc. Su flexibilidad es adecuada para
quienes siguen el principio *DRY* (*Do Not Repeat Yourself*).

La plantilla dbt que aparece a continuación es una simple definición de
una tabla, pero lleva metadatos que indican al usuario qué base de datos
y esquema debe utilizar:

.. code::

    /*
       models/example/table_a.sql
       Welcome to your first dbt model!
       Did you know that you can also configure models
       directly within SQL files?
       This will override configurations stated in dbt_project.yml
       Try changing "table" to "view" below
    */
    
    {{ config(
       materialized='table',
       alias='table_a',
       schema='events',
       tags=["example"]
    ) }}
    
    select
       1                 as id        
       , 'Some comments' as comments  
    union all
       2                 as id        
       , 'Some comments' as comments


Qué son las funciones de referencia
------------------------------------------------------------------------

Las funciones de referencia se declaran con ``ref()``, y permiten conectar
dos etapas para formar una tubería. En el caso de nuestra tabla anterior,
podemos definir una nueva tabla ``table_b.sql`` a partir de ella:

.. code::

    -- models/example/table_b.sql
    -- Use the ref function to select from other models
    {{ config(
        materialized='view',
        tags=["example"],
        schema='events'
        ) }}

    select *
      from {{ ref('table_a') }}
    where id = 1


Al usar estas referencias, definimos de forma implícita el 
:term:`linaje de datos`, en este caso:

.. graphviz::

  digraph Linaje {
    rankdir=LR;
    edge[label="Proviene de" dir="back"]
    table_a -> table_b
  }


    

.. _Data Build Tool: https://www.getdbt.com/
