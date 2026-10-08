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

.. warning:: Esto solo funciona en modo de desarrollo (DEBUG = True); en producción hay
   que configurar el servidor web para que sirva archivos de ``MEDIA_ROOT``. 

Con esta configuración en su lugar, está listo para ejecutar ``python manage.py migrate`` 
para crear las tablas de base de datos utilizadas por ``Wagtail``.
