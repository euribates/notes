Wagtail
========================================================================

Wagtail es un sistema de gestión de contenido de código abierto (CMS) que
se basa en Django, un popular marco web de Python. Ha ganado popularidad
entre los desarrolladores y editores de contenido por sus potentes
características e interfaz intuitiva, proporcionando una experiencia de
edición optimizada. Wagtail ofrece un conjunto de herramientas completas
para la creación y administración de contenido, que incluye un **editor de
texto enriquecido** con opciones de formato, **gestión de imágenes y
documentos**, **control de versiones**, **flujos de trabajo** y
**programación de contenido**.

Los desarrolladores aprecian la arquitectura altamente personalizable y
modular de Wagtail, que incluye soporte integrado para la estructura de
aplicaciones de Django. Esto les permite crear e integrar fácilmente la
funcionalidad personalizada, haciendo que Wagtail sea adecuado para
proyectos de cualquier tamaño. Wagtail se destaca en el manejo de
estructuras de contenido complejas, ofreciendo características como la
**organización jerárquica** de la página, las **capacidades de búsqueda**
robustas y la localización de contenido.

Wagtail se destaca como la opción preferida para decenas de miles de
organizaciones en todo el mundo, incluidos nombres de renombre como
Google, la Administración Nacional de Aeronáutica y del Espacio (NASA) y
el Servicio Nacional de Salud de Gran Bretaña (NHS). Ha demostrado
escalabilidad y es capaz de manejar grandes volúmenes de tráfico de
millones de visitantes cada mes. Lo que distingue a Wagtail es su
capacidad de extenderse más allá de la gestión de contenido tradicional,
proporcionando una integración perfecta con herramientas de datos y ricas
visualizaciones de datos.

Empezar con Webtail
------------------------------------------------------------------------

Primero instalamos Wagtail. Incluyo como requerimiento la librea
``pillow``, así que posiblemente tenemos que instalar en el sistema las
librerías ``libjpeg`` y ``zlib``.

.. code:: bash

    pip install wagtail

O si usamos ``uv``:

.. code:: bash

    uv add wagtail


Si empezamos un proyecto de cero, podemos usar el comando, similar al
``django-admin``, que sería ``wagtail start <site>``. Pero si lo que
queremos es integrarlo con un proyecto ya existente, temos que realizar
los siguientes pasos:

1. Añadir a la variable ``wagtail`` a la variable ``INSTALLED_APPS`` del
   fichero ``settings.py``.

2. Añadir en la variable ``MIDDLEWARE`` del fichero ``settings.py``:

   .. code:: python

        ("wagtail.contrib.redirects.middleware.RedirectMiddleware",)

3. Si no hemos defino la variable ``STATIC_ROOT``, definirla. Lo mismo con
   ``MEDIA_URL`` y ``MEDIA_ROOT``.

4. Cambiar la variable ``DATA_UPLOAD_MAX_NUMBER_FIELDS`` a :math:`10000` o
   superior. Esto especifica el número máximo de campos permitidos en un
   envío de formularios, y se recomienda aumentarlo (el valor
   predeterminado de Django de 1000), ya que los modelos de página
   particularmente complejos pueden exceder este límite dentro del editor
   de páginas de Wagtail:


   .. code:: python

       DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000

5.- Definir una variable ``WAGTAIL_SITE_NAME``, que se mostrará en el panel principal del *backend* de administración de Wagtail:

    .. code::

        WAGTAIL_SITE_NAME = "Blog de Python Canarias"

6. Definir la variable ``WAGTAILADMIN_BASE_URL`` que será la URL base
   utilizada por el sitio de administración de Wagtail. Por lo general, se
   utiliza para generar URL para incluir en los correos electrónicos de
   notificación:

   .. code:: python

       WAGTAILADMIN_BASE_URL = "https://example.com"

   Si esta configuración no está presente, Wagtail recurrirá a
   ``request.site.root_url`` o al nombre de host de la solicitud. Aunque
   esta configuración no es estrictamente necesaria, es **muy
   recomendable** porque dejarlo fuera puede producir URL inutilizables en
   los correos electrónicos de notificación.

7. Definir el conjunto de extensiones de ficheros que vamos a habilitar
   para poder ser gestionados por Wagtail, con la variable
   ``WAGTAILDOCS_EXTENSIONS``. Si se omite, se puede omitir para permitir
   cualquier tipo de archivos, pero esto puede presentar un riesgo de
   seguridad.

   .. code:: python

       WAGTAILDOCS_EXTENSIONS = [
           "csv",
           "docx",
           "key",
           "odt",
           "pdf",
           "pptx",
           "rtf",
           "txt",
           "xlsx",
           "zip",
           ]

Y ahora configuramos las URL:

.. code:: python

    from django.urls import path, include

    from wagtail.admin import urls as wagtailadmin_urls
    from wagtail import urls as wagtail_urls
    from wagtail.documents import urls as wagtaildocs_urls

    urlpatterns = [
        ...
        path('cms/', include(wagtailadmin_urls)),
        path('documents/', include(wagtaildocs_urls)),
        path('pages/', include(wagtail_urls)),
        ...
        ]


Las rutas exactas pueden ser cambiadas, claro.

- ``wagtailadmin_urls`` proporciona la interfaz de administración para
  Wagtail.  Es independiente de la interfaz de administración de Django,
  ``django.contrib.admin``. Los proyectos que consisten solo en  Wagtail
  pueden alojar el administrador de Wagtail en /admin/, pero si esto choca
  con el *backend* de administrador existente de su proyecto, se puede
  usar una ruta alternativa, como /cms/.

- Wagtail sirve los archivos de documentos desde la ubicación indicada en ``wagtaildocs_urls``.
  Se Puede omitir si no se van a utilizar las funciones de gestión de documentos.

- Finalmente, Wagtail sirve las páginas desde la ubicación
  ``wagtail_urls``. En el ejemplo anterior, Wagtail maneja las URL en
  ``/pages/``, dejando su proyecto Django para manejar la URL raíz y otras
  rutas como de costumbre. Si desea que Wagtail maneje todo el espacio de
  URL, incluida la URL raíz, coloque ``path('', include(wagtail_urls))``
  al final de la lista de ``urlpatterns``. La colocación de ``path('',
  include(wagtail_urls))`` al final de los ``urlpatterns`` asegura que no
  anule patrones de URL más específicos.

Por último, hay que configurar el proyecto para que sirva archivos cargados
por el usuario desde ``MEDIA_ROOT``. Su proyecto de Django ya puede tener esto
habilitado. Si no es el caso, hay que agregar el siguiente fragmento a ``urls.py``:

.. code:: python

   from django.conf import settings
   from django.conf.urls.static import static
   
   urlpatterns = (
       [
           # ... the rest of your URLconf goes here ...
       ]
       + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   )

.. warning:: Esto solo funciona en modo de desarrollo (DEBUG = True); en
   producción hay que configurar el servidor web para que sirva archivos
   de ``MEDIA_ROOT``. 

Con esta configuración en su lugar, está listo para ejecutar ``python
manage.py migrate`` para crear las tablas de base de datos utilizadas
por ``Wagtail``.

El Zen de Wagtail
------------------------------------------------------------------------

Wagtail no es una solución "lista para usar" de forma instantánea
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No se puede crear un sitio web atractivo simplemente ensamblando módulos
prefabricados; hay que escribir código.

Adopta siempre el rol adecuado
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La clave para utilizar Wagtail es reconocer que la creación de un sitio
web inplica la definición de múltiples roles: el autor de contenido, el
administrador del sitio, el desarrollador y el diseñador. Aunque pueden
ser personas distintas, no es obligatorio que sea así.

Si utilizas Wagtail para crear tu *blog* personal, es probable que
tengas que alternar entre estos diferentes roles. En cualquier caso, es
importante ser consciente de qué rol estás desempeñando en cada momento
y utilizar las herramientas adecuadas para esa tarea.

El autor de contenidos o el administrador del sitio realiza la mayor
parte de su trabajo a través de la interfaz de administración de Wagtail,
mientras que el desarrollador o el diseñador dedica la mayor parte de su
tiempo a escribir código Python, HTML o CSS.

Esto es algo positivo. Wagtail no se ha diseñado para sustituir la labor
de programación. Quizás algún día alguien cree una interfaz de «arrastrar
y soltar» para construir sitios web que sea tan potente como escribir
código, pero Wagtail no es esa herramienta, ni pretende serlo.

Un error común es otorgar demasiado poder y responsabilidad a los
autores de contenido y a los administradores del sitio. De hecho, si estas
personas son tus clientes, es muy probable que lo reclamen con insistencia.
Sin embargo, el éxito de tu sitio depende de tu capacidad para decir que no.
La verdadera potencia de la gestión de contenidos no reside en ceder el
control a los usuarios del CMS, sino en establecer límites claros entre los
distintos roles. Entre otras cosas, esto implica evitar que los editores se
encarguen del diseño y la maquetación dentro de la interfaz de edición de
contenidos, o que los administradores del sitio creen flujos de trabajo
interactivos complejos que se pueden implementar mejor mediante código.

Un CMS debe llevar información a la BD de forma eficiente y directa
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ya sea que tu sitio trate sobre coches, gatos, pasteles o trámites
inmobiliarios, los autores de contenidos llegarán a la interfaz de
administración de Wagtail con información específica de su ámbito que
desean publicar en el sitio web. Tu objetivo como creador del sitio es
extraer y almacenar esta información en su forma original (o «en
bruto»), y no según la idea que un autor concreto tenga sobre cómo
debería verse dicha información.

Mantener las cuestiones de diseño separadas del contenido de la página
ofrece numerosas ventajas. Garantiza que el diseño se mantenga coherente
en todo el sitio, sin quedar sujeto a los caprichos de los editores de
un día para otro. Permite aprovechar al máximo el contenido informativo
de las páginas. Por ejemplo, si tus páginas tratan sobre eventos, contar
con un tipo de página específico para «Eventos» —con campos de datos
para la fecha y la ubicación— te permite presentar los eventos en una
vista de calendario o en un listado filtrado; algo que no sería posible
si simplemente se hubieran implementado mediante diferentes estilos de
encabezado en una página genérica. 

Por último, si en el futuro rediseñas el sitio o lo trasladas a una
plataforma totalmente distinta, tendrás la tranquilidad de que el
contenido funcionará en el nuevo entorno sin depender de un formato
específico.

Imagina que un autor de contenido te hace una petición: «Necesitamos que
este texto aparezca en color rosa intenso y con la fuente Comic Sans».
Tu respuesta debería ser: «¿Por qué? ¿Qué tiene de especial este
fragmento de texto en concreto?». Si responden «Simplemente me gusta
cómo queda», tendrás que convencerles amablemente de que la toma de
decisiones sobre el diseño no les corresponde a ellos. Pero si la
respuesta es «es para nuestra sección infantil», entonces dispondrás de
una forma de separar los aspectos editoriales de los de diseño. Así,
podrás permitir que los editores marquen ciertas páginas como
pertenecientes a la «sección infantil» mediante etiquetas, diferentes
modelos de página o la jerarquía del sitio, dejando que los diseñadores
decidan cómo aplicar los estilos en función de esa clasificación.

Para un programador, la mejor interfaz es un lenguaje de programación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Es habitual encontrar en los sistemas de gestión de contenidos una
interfaz de tipo «apuntar y hacer clic» que permite definir el modelo de
datos que compone una página:

Aunque el discurso de ventas pueda hacerlo parecer atractivo, lo cierto
es que al usuario promedio de un sistema de gestión de contenidos (CMS)
le resultaría prácticamente imposible realizar un cambio tan
fundamental. Esto es especialmente cierto en el caso de un sitio web en
producción, ya que requiere un profundo conocimiento de programación y
conciencia de las posibles consecuencias de la modificación. Por tanto,
la gestión de esa interfaz de «apuntar y hacer clic» recaerá siempre en
el programador. Lo único que se ha hecho es apartarlos del cómodo
entorno de la escritura de código, donde disponen de todo un ecosistema
de herramientas —desde editores de texto hasta sistemas de control de
versiones— para desarrollar, probar y desplegar sus cambios.

Wagtail reconoce que la mayoría de las tareas de programación se
realizan mejor escribiendo código y no intenta convertirlas en
ejercicios de rellenar casillas cuando no hay una razón de peso para
hacerlo. Del mismo modo, al desarrollar funcionalidades para su sitio,
debe tener en cuenta que algunas características están destinadas a ser
mantenidas por el programador en lugar de por un editor de contenidos;
asimismo, conviene valorar si hacerlas configurables a través de la
interfaz de administración de Wagtail supondrá más un estorbo que una
ventaja.

Por ejemplo, Wagtail incluye un generador de formularios que permite a
los autores de contenido crear formularios de recopilación de datos de
uso general. Podría sentir la tentación de utilizarlo como base para
formularios más complejos que se integren, por ejemplo, con un sistema
CRM o una pasarela de pago. Sin embargo, en este caso no existe forma de
editar los campos del formulario sin reescribir la lógica del *backend*,
por lo que hacerlos editables a través de Wagtail aporta poco valor. Lo
más probable es que resulte más conveniente crearlos utilizando el
*framework* de formularios de Django, donde los campos se definen
íntegramente mediante código.

Adapar las plantillas de Wagtail a yu diseño
------------------------------------------------------------------------

Wagtail utiliza el sistema normal de plantillas de Django para cada tipo
de página. Por defecto, para generar el nombre de la plantilla
se combina el nombre de la app con el nombre del modelo. Las mayúsculas,
si las hay, se pasan a minúsculas y se separan del texto anterior con
el carácter subrayado ``_``. Por ejemplo, si la *app* es ``home`` y el
modelo se llama ``HomePage```, el nombre de la plantilla será
``home/home_page.html``.

las plantillas pueden residir un cualquiera de las localizaciones que se
permiten para las plantillas normales de Django. Lo normal es ponerlas
dentro de una carpeta ``templates/<app_name>/``.

En ``wagtailcore_tags`` se definen filtros y etiquetas específicas de
Wagtail.  Cargamos ``wagtailcore_tags`` al principio de las plantilla
para ganar acceso a estas etiquetas propias de Wagtail.

.. warning:: Se debe incluir ``{% load wagtailcore_tags %}`` en todas y
   cada una de las plantillas que utilicen las etiquetas de Wagtail. Si
   las etiquetas no se cargan, ``Django genera un TemplateSyntaxError``.

Una plantilla típica podría ser:

.. code: html

    {% extends 'base.html' %}
    {% load wagtailcore_tags %}

    {% block body_class %}template-homepage{% endblock %}

    <!-- replace everything below with: -->
    {% block content %}
        {{ page.body|richtext }}
    {% endblock %}

Donde ``base.html`` se refiere a la plantilla padre. Al extender de esta
plantilla estamos centralizando toda la apariencia común en un solo
sitio, como se recomiendo al usar Django. Podemos reescribir
determinadas partes de la plantilla común usando ciertos bloques con
nombre concretos.

Las etiquetas (*tags*) definidas por Wagtail
------------------------------------------------------------------------

Ya vimos el filtro ``richtext`` que nos permite mostrar el contenido de
un campo de tipo ``RichTextField``.

