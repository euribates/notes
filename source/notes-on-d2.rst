D2
========================================================================

.. tags: art,backend,cloud,design,devops,graphics, graphs,network,server, teaching

.. contents:: Relación de contenidos
    :depth: 3

Qué es D2
------------------------------------------------------------------------

**D2** es una herramienta de creación de diagramas basada en texto. Sigue 
un esquema declarativo, en el que se describe cómo queremos que sea
el diagrama, y D2 genera la imagen.


Cómo instalar D2
------------------------------------------------------------------------

La forma recomendada es mediante su propio script de instalación, que
encontrará la mejor manera de instalarlo basado en su máquina. Por
ejemplo, si D2 está disponible a través de un gestor de paquetes
instalado, utilizará ese gestor de paquetes.

.. code:: shell

    # Con --dry-run el script de instalación imprimirá los comandos que utilizará
    # instalar sin instalar realmente para que sepas lo que va a hacer.
    curl -fsSL https://d2lang.com/install.sh | sh -s -- --dry-run
    # Si las cosas se ven bien, instalar de verdad.
    curl -fsSL https://d2lang.com/install.sh | sh -s --

Se puede verificar la instalación haciendo:

.. code:: shell

    d2 version


Como sería el Hola, mundo en D2
------------------------------------------------------------------------

La forma más sencilla es crear un fichero sencillo D2 y pedir al cliente
que nos lo muestre:

.. code:: shell

    $ echo 'x -> y: Hello, world' > input.d2
    $ d2 -w input.d2 out.svg

Esto arranca un servidor web que muestra el fichero, incluso con refresco
automático si se cambia la fuente.

El resultado debería ser:

.. d2::
   :scale: 0.8

    x -> y: Hello, World

Formas en D2
------------------------------------------------------------------------

Cualquier identificador se interpreta como una forma, siendo el
identificador el nombre que se muestra dentro de la misma. Los siguientes
son todos formas/identificadores válidos:

- ``imAShape``
- ``im_a_shape``
- ``im a shape``
- ``i'm a shape``
- ``a-shape``

No hacen falta comillas para definir ni los identificadores ni las
etiqetas, aunque se pueden usar, si se desea, tanto comillas simples como
dobles.  Los identificadores son indiferentes a las mayúsculas/minúsculas,
así que ``abc``, ``Abc`` y ``ABC`` se refieren todos al mismo
identficador.

Nótese que el último ejemplo es un identificador, porque solo tiene
un guión, pero si tuviera dos (``a--shape``), esos dos se interpretarían
como una conexión entre las dos formas.

Se puede usar el símbolo punto y como ``;`` para definir varias formas en
una sola línea.

.. code::

    SqLite; Cassandra; PostgrSQL

Si quisiéremos que el texto de la forma sea diferente del identificador,
podemos asignar un texto con el símbolo de dos puntos:

.. code::

    pg: PostgrSQL DB

La forma por defecto es un rectángulo, pero se puede modificar con el
sufijo ``shape``:

.. code::

    Cloud: my cloud
    Cloud.shape: cloud

El siguiente diagrama muestra los valores más usados de ``shape``:

.. d2::
   :scale: 0.7

    grid-rows: 4

    rectangle.shape: rectangle
    square.shape: square
    page.shape: page
    parallelogram.shape: parallelogram
    
    document.shape: document
    cilynder.shape: cylinder
    queue.shape: queue
    package.shape: package
    step.shape: step

    callout.shape: callout
    stored_data.shape: stored_data
    person.shape: person
    diamond.shape: diamond

    oval.shape: oval
    circle.shape: circle
    hexagon.shape: hexagon
    cloud.shape: cloud
    c4-person.shape: c4-person


Conexiones en D2
------------------------------------------------------------------------

Las conexiones entre identificadores/formas se definen con guiones y
símbolos de mayor/menor que forman líneas y flechas. Hay cuatro formas
diferentes de definir una conexión en D2:

- ``--``
- ``->``
- ``<-``
- ``<->``

Se pueden usar guiones extras, por ejemplo ``<---------->`` es igual de
válido que ``<->``.

Por ejemplo, el siguiente código D2:

.. code::

    Write Replica Canada <-> Write Replica Australia

    Read Replica <- Master
    Write Replica -> Master

    Read Replica 1 -- Read Replica 2

Muestra los diferentes tipos de conexiones:

.. d2::
   :scale: 0.8

    Write Replica Canada <-> Write Replica Australia

    Read Replica <- Master
    Write Replica -> Master

    Read Replica 1 -- Read Replica 2

Si se hace referencia a una entidad que no existe en una conexión, se
crea. Las referencias de una conexión **siempre deben hacerse contra los
identificadores, no contra las etiquetas**. Las conexiones también pueden
tener etiquetas:

Si una conexión se repite, la última no sobreescribe la primera, sino que
se duplican. Con los identificadores/formas es al reves, si se duplican,
el último declarado sobreescribe la definición del primero:


.. code::

    Database -> S3: backup
    Database -> S3
    Database -> S3: backup

Produce:

.. D2::
   :scale: 0.8

    Database -> S3: backup
    Database -> S3
    Database -> S3: backup

Se pueden definir, por comodidad, varias conexiones en una única línea>

.. code::

    High Mem Instance -> EC2 <- High CPU Instance: Hosted By

Produce:

.. d2::
   :scale: 0.8

    High Mem Instance -> EC2 <- High CPU Instance: Hosted By


Cómo modificar los extremos de las conexiones en D2
------------------------------------------------------------------------

Para modificar la forma de punta de flecha predeterminada o dar una
etiqueta junto a las puntas de flecha, hay que definir una entradas
especiales en las conexiones llamadas ``source-arrowhead`` y/o
``target-arrowhead``. Los valores posibles son:

- ``triangle`` (valor por defecto): Se puede indicar un estilo en el que
  el triángulo no esté relleno con ``style.filled: false``.


- ``arrow``: Como ``triangle`` pero más puntiagudo.

- ``diamond``: Diamante. También acepta ``style.filled: false``

- ``circle``: Círculo. También acepta ``style.filled: false``

- ``box``: Recuadro: También acepta ``style.filled: false``

- ``cf-one``, ``cf-one-required``, ``cf-many`` y ``cf-many-required`` (``cf`` viene
  de *crows foot*), útiles para `diagramas de entidad relación`_.

- ``cross``: Cruz


.. _diagramas de entidad relación: https://es.wikipedia.org/wiki/Modelo_entidad-relaci%C3%B3n

El siguiente diagrama muestra algunas de estas posibilidades:

.. d2::
   :scale: 0.8

    direction: right 

    A <-> B: {
    source-arrowhead.shape: diamond
    }

    C <-> D: {
    target-arrowhead.shape: cross
    source-arrowhead.shape: cf-one
    }

    C <-> D: {
    target-arrowhead.shape: circle
    }

    Entidad Fuerte <--> Entidad débil: {
    target-arrowhead.shape: cf-many
    source-arrowhead.shape: arrow
    }


.. warning::
    
   Atención, si el extremo de la flecha no tiene punta (Es decir, no
   esta indicado con ``<`` o ``>``, las opciones de estilo de la punta
   se ignoran.

   Po ejemplo, en el siguiente diagrama, las opciones de flecha se
   ignorarán, porque no hay flecha en el origen:

   .. code::

       x -> y: {
         source-arrowhead.shape: diamond
       }


Contenedore en D2
------------------------------------------------------------------------

Los contenedores se pueden crear declarando una forma dentro de otra:

.. code::

    server

    server.process


Se pueden declarar ambos en una misma línea:

.. code::

    parent.child

Las conexiones funcionan sin problema entre contenedores:

.. code::

    apartment.Bedroom.Bathroom -> office.Spare Room.Bathroom: Portal

Ejemplos:

.. d2::
   :scale: 0.8

    direction: right

    server

    server.process

    parent.child

    apartment.Bedroom.Bathroom -> office.Spare Room.Bathroom: Portal

Puedes evitar repetir contenedores creando mapas anidados:

.. code::

    clouds: {

        aws: {
            load_balancer -> api
            api -> db
        }

        gcloud: {
            auth -> db
        }

        gcloud -> aws
        
        }

Produce:


.. d2::
   :scale: 0.8

    clouds: {
      aws: {
        load_balancer -> api
        api -> db
      }
      gcloud: {
        auth -> db
      }
    
      gcloud -> aws
    }

Hay dos formas de asignar etiquetas de texto a los contenedores, la
forma abreviada:


.. code::

    gcloud: Google Cloud {
      AWS
      S2
      }

O usando la palabra clave ``label``:

.. code::

   gcloud: {
     label: Google Cloud
     AWS
     S2
   }


Ambas producen el mismo resultado:

.. d2::
   :scale: 0.8

    gcloud: {
      label: Google Cloud
      AWS
      S2
    }

   



Diagramas UML con D2
------------------------------------------------------------------------

D2 Tiene soporte para algunos de los diagramas UML, por ejemplo el
diagrama
de clase:

.. code::

    Point: {
      shape: class

      +x: float
      +y: float
      __init__(x float, y float)
      module(): float
      }

Produce:

.. d2::
   :scale: 0.8

    Point: {
      shape: class

      +x: float
      +y: float
      __init__(x float, y float)
      module(): float
      }

Cada clave de una forma de tipo ``class`` define un campo o un método.
El valor de una clave de campo es su tipo.  Cualquier clave que contenga
``(`` es un método, cuyo valor es el tipo de retorno.  Una clave de
método sin un valor tiene un tipo de retorno de vacío. 


Iconos en D2
------------------------------------------------------------------------

Se puede usar cualquier icono al que se haga referencia por una URL
válida:


.. code::

    Página Web: {
      icon: https://www.gobiernodecanarias.org/gcc/img/logos/logo.gif
      Intranet
      Organigrama
      }

Se ve como:

.. d2::

    Página Web: {
      icon: https://www.gobiernodecanarias.org/gcc/img/logos/logo.gif
      Intranet
      Organigrama
      }

Pero la gente de D2 mantiene una serie de iconos de uso habitual en
<https://icons.terrastruct.com/>, por ejemplo:

.. image:: https://icons.terrastruct.com/dev%2Fapache.svg



Tablas y esquemas de bases de datos en D2
------------------------------------------------------------------------


    


Comentarios en D2
------------------------------------------------------------------------

Los comentarios de línea comienzan con un hash (``#``)
y continúan hasta la próxima nueva línea o el fin del fichero.

.. code::

    x -> y # Estoy al final

Los comentarios de bloque comienzan y terminan con tres citas dobles:

.. code::

    x -> y

    """
    Esto es un
    comentario de bloque
    """

    y -> z
    
