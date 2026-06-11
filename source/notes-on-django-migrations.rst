Django migrations
=======================================================================

.. tags:: django, database, development, python, migrations, devops

.. contents:: Relación de contenidos
    :depth: 3


¿Qué es una migración?
------------------------------------------------------------------------

Las migraciones son la forma en que Django propaga los cambios
realizados en los modelos (agregar un campo, eliminar un modelo, etc.) al
esquema de tu base de datos. Están diseñadas para ser mayormente
automáticas, pero aun así necesitarás saber cuándo realizar las migraciones,
cuándo ejecutarlas y los problemas comunes que puedes encontrar.

Un archivo de migración es un módulo de Python que contiene una clase
`Migration` con dos atributos clave:

- **Dependencias**: Una lista de las migraciones que han de ejecutarse
  obligatoriamente antes de esta.

- **Operaciones**: Una lista de objetos de tipo ``Operation`` que
  describen los cambios a realizar en el esquema.

El siguiente ejemplo es una migración que añade un nuevo campo
``pnone_number`` al modelo ``user``:

.. code:: python

    # apps/users/migrations/0003_add_phone_number.py
    from django.db import migrations, models


    class Migration(migrations.Migration):

        dependencies = [
            ("users", "0002_add_avatar"),   # ← must run after 0002
        ]

        operations = [
            migrations.AddField(
                model_name="user",
                name="phone_number",
                field=models.CharField(max_length=20, null=True, blank=True),
            ),
        ]


La table ``django_migrations``
------------------------------------------------------------------------

Django mantiene un registro de todas las migraciones que ha aplicado en
una tabla en la base de datos, llamada ``django_migrations``. Cada vez
que se ejecuta el comando ``migrate``, Django comprueba esta tabla, la
compara con los ficheros de migraciones almacenados en las carpetas
``migrations``, y aplica aquellos que no estuvieran ya aplicados.

.. code:: sql

    SELECT app, name, applied
      FROM django_migrations
     ORDER BY applied DESC LIMIT 5;

    app        | name                             | applied
    ------------+----------------------------------+------------------------
    users      | 0003_add_phone_number            | 2025-03-15 14:22:11
    orders     | 0012_add_external_reference      | 2025-03-15 14:22:10
    catalog    | 0008_product_add_weight          | 2025-03-14 09:10:04
    users      | 0002_add_avatar                  | 2025-03-01 11:45:22
    users      | 0001_initial                     | 2025-02-20 08:30:11


Schema Migrations vs Data Migration
------------------------------------------------------------------------

There are two fundamentally different kinds of migrations:

**Schema migrations** alter the database structure: adding or removing
tables, adding or removing columns, creating indexes, changing column
types. These are generated automatically by ``makemigrations``.

**Data migrations** modify the data inside existing tables: backfilling
a new column, transforming existing values, splitting one table into
two. These must be written by hand using ``RunPython`` or ``RunSQL``.

The golden rule: **always separate schema migrations from data
migrations**. One migration should do one thing.

The Migration Graph
------------------------------------------------------------------------

Migration files are not executed linearly by file name. Django builds a
Directed Acyclic Graph (DAG) of all migrations based on their
dependencies declarations, then executes them in topological order.

This graph is what allows Django to handle branch merges, detect
conflicts, and squash migrations without losing history.

Architecture Design - The Five Internal Components
------------------------------------------------------------------------

Django's migration system has five key internal components that work together:

.. code::

    ┌─────────────────────────────────────────────────────────────┐
    │                   python manage.py makemigrations           │
    └──────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
            ┌──────────────────────────┐
            │      AUTODETECTOR        │
            │  Compares current model  │
            │  state to last migration │
            │  state → finds changes   │
            └───────────┬──────────────┘
                        │ list of changes
                        ▼
            ┌──────────────────────────┐
            │       OPTIMIZER          │
            │  Reduces redundant ops:  │
            │  AddField+RemoveField    │
            │  → no-op                 │
            └───────────┬──────────────┘
                        │ optimised ops
                        ▼
            ┌──────────────────────────┐
            │        WRITER            │
            │  Generates the Python    │
            │  migration file on disk  │
            └──────────────────────────┘

    ┌──────────────────────────────────────────────────────────┐
    │               python manage.py migrate                   │
    └───────────────────┬──────────────────────────────────────┘
                        │
                        ▼
            ┌──────────────────────────┐
            │        LOADER            │
            │  Reads all migration     │
            │  files → builds the DAG  │
            └───────────┬──────────────┘
                        │
                        ▼
            ┌──────────────────────────┐
            │       EXECUTOR           │
            │  Checks django_migrations│
            │  table, runs unapplied   │
            │  migrations in order     │
            └───────────┬──────────────┘
                        │
                        ▼
            ┌──────────────────────────┐
            │      RECORDER            │
            │  Inserts rows into the   │
            │  django_migrations table │
            └──────────────────────────┘

Understanding these components is what lets you debug migration
failures, resolve conflicts, and override default behaviour when needed.

The ProjectState Object
------------------------------------------------------------------------

At its core, the migration system works by replaying the entire history
of migration files to reconstruct a model of your database schema — the
``ProjectState``. This is how makemigrations knows what changed: it
computes ProjectState from existing migrations, compares it to your
current ``models.py``, and generates operations for the difference.

This is also why migrations must use ``apps.get_model()`` inside
``RunPython`` functions rather than importing models directly — the
migration is running against a historical version of the model, not the
current one.


Cómo hacer migraciones propias en Django
------------------------------------------------------------------------

Podemos crear nuestras propias migraciones. Este es realmente útil para
cambios en las bases de datos que ya estén en producción.

Primero creamos una migración vacía (*empty*):

.. code:: shell

   ./manage.py makemigrations --empty --name nombre_que_quieras_para_la_migracion app_name

Esto creará un fichero de migración, que no hace nada, con un contenido
similar a este:

.. code:: python

   # Generated by Django 3.2.12 on 2022-03-22 09:04

   from django.db import migrations


   class Migration(migrations.Migration):

       dependencies = [
           ('agora', '0003_alter_table_add_field_flag'),
       ]

       operations = [
       ]

Como vemos, solo se define el campo de dependencias, las operaciones a
realizar en esta migración están vacías. Vamos a incluir código SQL para
crear la secuencia:

.. code:: sql

   CREATE SEQUENCE Agora.seq_foto_diputado START WITH 1 INCREMENT BY 1;

Para ello haremos uso de la clase `migration.RunSQL`_, que nos permite
definir la migración tanto en una dirección como en otra, es decir,
crearemos este objeto con dos sentencias SQL, una para definir como
aplicar la migración, y otra para deshacerla. En nuestro caso, quedaría
así:

.. _migratons.RunSQL: https://docs.djangoproject.com/en/1.10/ref/migration-operations/#runsql

.. code:: python

   # Generated by Django 3.2.12 on 2022-03-22 09:04

   from django.db import migrations


   class Migration(migrations.Migration):

       dependencies = [
           ('agora', '0003_asunto_bop_cargo_claseiniciativa_composicion_diputado_diputadogrupo_ds_dsc_dsdp_fotodiputado_grupopa'),
       ]

       operations = [
           migrations.RunSQL(
               'CREATE SEQUENCE Agora.seq_foto_diputado START WITH 1 INCREMENT BY 1',
               'DROP SEQUENCE Agora.seq_foto_diputado',
           )
       ]

Fuentes:

- `Executing Custom SQL in Django Migrations`_ - End Point Dev

- `A Pony On The Move: How Migrations Work In Django`_ - DjangoCon.eu - Porto - 2020

.. _`A Pony On The Move: How Migrations Work In Django`: https://www.youtube.com/watch?v=u6cVvbuUzlk
.. _Executing Custom SQL in Django Migrations: https://www.endpointdev.com/blog/2016/09/executing-custom-sql-in-django-migration/

Cómo crear migraciones propias usando código Python en vez de SQL
------------------------------------------------------------------------

Si las migraciones usando solo SQL se quedan cortas, también podemos
hacer migraciones personalizadas que usen código Python e incluso, con
ciertas limitaciones, nuestro código ya existente.

Para ello, en vez de usar la clase ``RunSQL`` usaremos la clase
``RunPython``. Esta clase espera un *callable*, normalmente una función.
Esta función debe aceptar dos parámetros: el primero es un registro que
mantiene los versiones a lo largo de la historia de todos los modelos,
de forma que podamos acceder al modelo tal y como era en la evolución
del proyecto. El segundo parámetro es una instancia de a clase
``SchemaEdior``, que se puede usar para realizar cambios manuales en el
esquema de la base de datos (Pero que no es recomendable usar, ya que
puede confundir, y mucho, al sistema de migraciones).

Veamos un ejemplo, en el que calculamos la letra inicial, normalizada,
de un texto y lo almacenamos en otro campo. Esto puede ser útil a
efectos de filtrar y clasificar las entradas:

.. code:: py

   from django.db import migrations


   def make_inicial(text):
       if text:
           normaliza_table = str.maketrans("ÁÉÍÓÚ", "AEIOU")
           char = text[0].upper()
           return char.translate(_normaliza_table)
       return ''


   def set_inicial(apps, schema_editor):
       # No podemos usar el modelo Entrada directamente, porque puede
       # que a estas alturas exista una version posterior al modelo
       # que espera la migración. Por eso tenemos que _viajar en el tiempo_
       # y cargar elmodelo que se corresponda con el momento histórico
       # de esta migración.
       Ejemplo = apps.get_model("dc2", "Ejemplo")
       for ejemplo in Ejemplo.objects.filter(inicial=None):
           ejemplo.inicial = make_inicial(ejemplo.entrada)
           ejemplo.save()


   class Migration(migrations.Migration):
       dependencies = [
           ("dc2", "0001_initial"),
       ]

       operations = [
           migrations.RunPython(set_inicial),
       ]

Al igual que con ``RunSQL``, podemos implementar la operación que
deshaga este cambio, y pasarla como segundo parámetro. Si hacemos esto
con todas nuestras migraciones personales (Las automáticas lo realizan
siempre), podemos viajar atrás y adelante en la historia del esquema de
la base de datos, que puede ser una capacidad interesante. Para el
ejemplo anterior, quedaría así:

.. code:: py

   from django.db import migrations


   def make_inicial(text):
       if text:
           normaliza_table = str.maketrans("ÁÉÍÓÚ", "AEIOU")
           char = text[0].upper()
           return char.translate(_normaliza_table)
       return ''


   def set_inicial(apps, schema_editor):
       # No podemos usar el modelo Entrada directamente, porque puede
       # que a estas alturas exista una version posterior a el modelo
       # que espera la migración. Por eso tenemos que _viajar en el tiempo_
       # y cargar elmodelo que se corresponda con el momento histórico
       # de esta migración.
       Ejemplo = apps.get_model("dc2", "Ejemplo")
       for ejemplo in Ejemplo.objects.filter(inicial=None):
           ejemplo.inicial = make_inicial(ejemplo.entrada)
           ejemplo.save()


   def unset_inicial(apps, schema_editor):
       Ejemplo = apps.get_model("dc2", "Ejemplo")
       for ejemplo in Ejemplo.objects.exclude(inicial=None):
           ejemplo.inicial = None
           ejemplo.save()


   class Migration(migrations.Migration):
       dependencies = [
           ("dc2", "0001_initial"),
       ]

       operations = [
           migrations.RunPython(set_inicial, unset_inicial),
       ]


Cómo condensar/simplificar (*squash*) las migraciones en Django
------------------------------------------------------------------------

Existe una opción en el ``manage.py`` llamada **``squashmigrations``**
que nos permite condensar todas las migraciones aplicadas (o un
subconjunto de ellas) de forma que se sustituyan por una única
migración. Además, intenta optimizar las migraciones al mezclarlas, de
forma que se eliminan los cambios que son sobrescritos por migraciones
posteriores.

Por ejemplo, si tenemos una acción de tipo ``CreateModel()`` y más tarde
aparece otra de tipo ``DeleteModel()`` para el mismo modelo, se pueden
eliminar no solo las dos acciones indicadas, sino también cualquier
acción intermedia que modifique al modelo.

Igualmente, acciones como ``AlterField()`` o ``AddField()`` son
trasladadas a la versión final de la acción ``CreateModel``.

La versión final condensada también mantiene referencias al conjunto de
migraciones que reemplaza. De esa forma Django puede entender cosas como
el histórico de grabaciones o las dependencias entre migraciones.

Django enumera de forma automática los ficheros de migraciones,
partiendo de ``0001_initial.py``. De esa forma puede determinar el orden
de aplicación de las migraciones, y nosotros podemos usarlo para indicar
el conjunto de las migraciones que queremos condensar, en forma de
rango.

Por ejemplo, supongamos que tenemos la siguiente lista de migraciones:

::

   ./foo
       ./migrations
           0001_initial.py
           0002_userprofile.py
           0003_article_user.py
           0004_auto_20190101_0123.py

En la mayoría de los casos, querríamos condensarlas todas en un único
fichero. Para ello, ejecutamos la siguiente orden:

.. code:: shell

   python manage.py squashmigrations foo 0004

El resultado será condensar todas las migraciones, desde la 1 hasta la
4, generando una nueva migración con el nombre:
``0001_squashed_0004_auto_<timestamp>.py``

Si examinamos este fichero, descubriremos dos cosas interesantes:

-  La nueva migración está marcada como ``initial=True``, lo que
   significa que sera la nueva migración inicial de esta aplicación. Si
   se aplicara en una nueva base de datos, las migraciones anteriores se
   ignorarían.

-  Se ha añadido un nuevo atributo, ``replaces``, que es una lista de
   las migraciones que son reemplazadas por esta.

Fuentes:

-  `How to Squash and Merge Django Migrations ·
   Coderbook <https://coderbook.com/@marcus/how-to-squash-and-merge-django-migrations/>`__

Cómo *resetear* las migraciones
------------------------------------------------------------------------

A veces, especialmente al principio del desarrollo, damos varios pasos
en falso hasta que la estructura de la base de datos queda más o menos
bien establecida. Esto puede provocar una serie de migraciones que no
aportan nada realmente. En estos casos, puede ser útil **resetar
todas las migraciones** y quedarnos con solo una migración inicial para
cada *app* (O quizá solo algunas de ellas).

Para hacer esto, tenemos que considerar dos escenarios posibles:

- El proyecto todavía está en el entorno de desarrollo y se desea
  una limpieza completa. No importa descartar toda la base de datos

- Se quiere borrar todo el historial de migración, pero manteniendo
  la base de datos existente.

Veamos los dos casos.

Escenario 1: Podemos descartar la base de datos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Paso **Uno**: Quitar todos los archivos de migraciones dentro de
  cada app. Revise cada una de las carpetas de migración de aplicaciones
  de proyectos y elimine todo lo que hay dentro, excepto el fichero 
  ``__init__.py``.

- Paso **Dos**: Borrar la base de datos. Si es *sqlite*, el fichero
  ``db.sqlite3``.

- Paso **Tres**: Crear las migraciones iniciales y generar el 
  esquema de la base de datos:

    .. code:: 

        python manage.py makemigrations
        python manage.py migrate

Y listo.

Escenario 2: No queremos descartar la base de datos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Paso **Uno**: Verificar que todos los modelos se ajustan al esquema
  actual de la base de datos. La forma más fácil de hacerlo es tratando
  de crear nuevas migraciones: ``python manage.py makemigrations``. Si
  no hay ninguna, ya está. Si no, ejecutamos las migraciones primero.

- Paso **Dos**: Borrar el historial de migración para cada aplicación.
  Ahora hay que borrar la aplicación del historial de migración por 
  aplicación. Esto es, la tabla ``django_migrations`` (En el paso
  anterior no hay que hacer esto porque hemos borrado toda la base de
  datos).

  Para cada app: Borrar el historial de migración, ejecutar:

  .. code:: shell

        python manage.py migrate --fake <app> zero

  Esto borrará el registro de migraciones para la app, sin hacer
  realmente ningún otro cambio en la base de datos, por eso
  es **muy importante** el *flag* ``--fake``.

  El comando ``showmigrations`` debería mostrarnos todas las
  migraciones de cada app, pero en estado "no aplicada".

- Paso **Tres**: Quitar los archivos de migración reales.
  Revisar cada una de las carpetas de migración de aplicaciones
  de proyectos y eliminar todo lo que esté dentro, excepto el
  fichero ``__init__.py``. El comando ``showmigrations`` debería
  mostrarnos que no hay ninguna migración.

- Paso **Cuatro**: Crear las migraciones iniciales

  .. code:: python

      python manage.py makemigrations

  Que debe crear migraciones iniciales para cada una de las
  aplicaciones.  

- Paso **Cinco**: Falsificar la migración inicial. Como las tablas
  de cada modelo realmente ya existen en la base de datos, lo único que
  queda por hacer es marcar estas migraciones iniciales como ya
  aplicadas, pero sin que realmente modifiquen el esquema. Si intentamos
  aplicarlar realmente, nos darán problemas, por ejemplo al intentar
  crear una tabla con ``CREATE TABLE ...`` cuando la tabla ya existe.
  Por eso aplicamos el *flag** ``--fake``:

  .. code:: shell

      python manage.py migrate --fake-initial

Fuente: `Django Reset Migrations`_

Cómo usar la base de datos actual y librarme de migraciones anteriores
------------------------------------------------------------------------

Si sabe que sus modelos coinciden **totalmente** con el esquema
existente, y que no hay migraciones generadas que necesiten ser
contabilizadas (es decir, no ha creado ninguna migración de datos u
otras migraciones a mano):

- Haga una copia de seguridad de todo (incluida su base de datos de
  producción)

- eliminar todos los archivos de migración (pero mantener el directorio
  y los archivos ``__init__.py``),

- Crear una nueva base de datos

- Cambie su proyecto para referirse a esa base de datos.

- Ejecute ``makemigrations`` para crear un conjunto de migraciones que
  describan sus modelos actuales.

- Cambie su proyecto para consultar la base de datos de producción
  original

- Vacíe la tabla ``django_migrations`` de su base de datos de
  producción

- ejecutar migrar con la opción ``--fake`` (esta actualizará la tabla
  ``django_migrations``)

- Ejecute ``showmigrations`` para verificar que todas sus nuevas
  migraciones iniciales se muestren como aplicadas.







Fuentes:

- `Django Migrations explained`_

.. _Django Migrations Explained: https://dev.to/alansomathew/django-migrations-explained-a-complete-production-guide-2k2m
