Django: Migrando de versión
========================================================================

Migrar a la versión 1.7 (last version in this branch is 1.6.11)
------------------------------------------------------------------------

The Django 1.6 series is the last to support Python 2.6. Django 1.7 is
the first release to support Python 3.4. Add built-in support for schema
migrations. New concept of Django Applicastions

-  Django applications

   As the concept of `Django
   applications <https://docs.djangoproject.com/en/2.2/ref/applications/>`__
   matured, this code showed some shortcomings. It has been refactored
   into an “app registry” where models modules no longer have a central
   role and where it’s possible to attach configuration data to
   applications.

   Improvements thus far include:

   -  Applications can run code at startup, before Django does anything
      else, with the ``ready()`` method of their configuration.

   -  Application labels are assigned correctly to models even when
      they’re defined outside of ``models.py``. You don’t have to set
      ``app_label`` explicitly any more.

   -  It is possible to omit ``models.py`` entirely if an application
      doesn’t have any models.

   -  Applications can be relabeled with the label attribute of
      application configurations, to work around label conflicts.

   -  The name of applications can be customized in the admin with the
      ``verbose_name`` of application configurations.

   -  The admin automatically calls ``autodiscover()`` when Django
      starts. **You can consequently remove this line from your
      URLconf**.

   -  Django imports all application configurations and models as soon
      as it starts, through a deterministic and straightforward process.
      This should make it easier to diagnose import issues such as
      import loops.

-  Improvements to Form error handling

   Previously there were two main patterns for handling errors in forms:

   -  Raising a ``ValidationError`` from within certain functions
      (e.g. ``Field.clean()``, ``Form.clean_<fieldname>()``, or
      ``Form.clean()`` for non-field errors.)

   -  Fiddling with ``Form._errors`` when targeting a specific field in
      ``Form.clean()`` or adding errors from outside of a “clean” method
      (e.g. directly from a view).

   Using the former pattern was straightforward since the form can guess
   from the context (i.e. which method raised the exception) where the
   errors belong and automatically process them. This remains the
   canonical way of adding errors when possible. However the latter was
   fiddly and error-prone, since the burden of handling edge cases fell
   on the user.

   The new ``add_error()`` method allows adding errors to specific form
   fields from anywhere without having to worry about the details such
   as creating instances of ``django.forms.utils.ErrorList`` or dealing
   with Form.cleaned_data. This new API replaces manipulating
   Form._errors which now becomes a private API.

   See Cleaning and validating fields that depend on each other for an
   example using Form.add_error().

..

   ⚠️ Files affected:

   -  api3.py ❓
   -  admin.py
   -  view.py

More information in `Django 1.7 release
notes <https://docs.djangoproject.com/en/2.2/releases/1.7/>`__
Migrar a la versión 3.1.1
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


Migrar a la versión 4.xx
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


Migrar a la versión 1.5 (last version in this branch is 1.5.12)
------------------------------------------------------------------------

First release to be compatible with Python3. Also add `configurable User
model <https://docs.djangoproject.com/en/2.2/releases/1.5/#configurable-user-model>`__.
Uses python’s built-in json lib instead of a custom one.

Things to consider:

-  ``ALLOWED_HOSTS`` required in production

-  Context in year archive class-based views

   For consistency with the other date-based generic views,
   ``YearArchiveView`` now passes year in the context as a
   ``datetime.date`` rather than a string. If you are using
   ``{{ year }}`` in your templates, you must replace it with
   ``{{ year|date:"Y" }}``.

-  Context in year and month archive class-based views

   ``YearArchiveView`` and ``MonthArchiveView`` were documented to
   provide a dates list sorted in ascending order, like their
   function-based predecessors, but it actually was in descending order.
   In 1.5, the documented order was restored. You may want to add (or
   remove) the reversed keyword when you’re iterating on ``date_list``.

-  Cleaned_data dictionary kept for invalid forms

   The ``cleaned_data`` dictionary is now **always** present after form
   validation. When the form doesn’t validate, it contains only the
   fields that passed validation. You **should** test the success of the
   validation with the ``is_valid()`` method and not with the presence
   or absence of the ``cleaned_data`` attribute on the form.

-  Deprecated ``django.contrib.markup``

   The markup contrib module has been deprecated and will follow an
   accelerated deprecation schedule. Direct use of Python markup
   libraries or 3rd party tag libraries is preferred

More information in `Django 1.5 release
notes <https://docs.djangoproject.com/en/2.2/releases/1.5/>`__

To version 1.6 (last version in this branch is 1.6.11)
------------------------------------------------------------------------

Django 1.6 will be the final release series to support Python 2.6;
beginning with Django 1.7, the minimum supported Python version will be
2.7. The admin is now enabled by default in new projects. A new
``django.db.models.BinaryField`` model field allows storage of raw
binary data in the database. A check management command was added,
enabling you to verify if your current configuration (currently oriented
at settings) is compatible with the current version of Django.

Things to consider:

-  GeoDjango form widgets¶

   GeoDjango now provides form fields and widgets for its
   geo-specialized fields. They are OpenLayers-based by default, but
   they can be customized to use any other JS framework.

-  New type attributes available in HTML5

   The default widgets for ``EmailField``, ``URLField``,
   ``IntegerField``, ``FloatField`` and ``DecimalField`` use the new
   type attributes available in HTML5 (``type='email'``, ``type='url'``,
   ``type='number'``).

-  The jQuery library embedded in the admin has been upgraded to version
   1.9.1.

-  `Pillow <https://pypi.org/project/Pillow/>`__ is now the preferred
   image manipulation library.

   PIL is pending deprecation (support to be removed in Django 1.8). To
   upgrade, you should first uninstall PIL, then install Pillow.

-  ``ModelForm`` accepts several new ``Meta`` options.

   The ``labels``, ``help_texts`` and ``error_messages`` options may be
   used to customize the default fields, see Overriding the default
   fields for details.

-  BoundField.label_tag now includes the form’s label_suffix

   This is consistent with how methods like Form.as_p and Form.as_ul
   render labels.

   If you manually render label_tag in your templates:

   ::

      {{ form.my_field.label_tag }}: {{ form.my_field }}

   you’ll want to remove the colon (or whatever other separator you may
   be using) to avoid duplicating it when upgrading to Django 1.6. The
   following template in Django 1.6 will render identically to the above
   template in Django 1.5, except that the colon will appear inside the
   ``<label>`` element.

   ::

      {{ form.my_field.label_tag }} {{ form.my_field }}

   will render something like:

   ::

      <label for="id_my_field">My Field:</label> <input id="id_my_field" type="text" name="my_field" />

   If you want to keep the current behavior of rendering ``label_tag``
   without the ``label_suffix``, instantiate the form
   ``label_suffix=''``. You can also customize the label_suffix on a
   per-field basis using the new ``label_suffix`` parameter on
   ``label_tag()``.

More information in `Django 1.6 release
notes <https://docs.djangoproject.com/en/2.2/releases/1.6/>`__



Migrar a 6.xx
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

>   RemovedInDjango60Warning: The default scheme will be changed from
>   ‘http’ to ‘https’ in Django 6.0. Pass the
>   ``forms.URLField.assume_scheme argument`` to silence this warning, or
>   set the ``FORMS_URLFIELD_ASSUME_HTTPS`` transitional setting to True
>   to opt into using ‘https’ as the new default scheme.

Django 5.1 lo trata como un ``DeprecationWarning`` pero en Django 6.0
cambiará el valor por defecto y eliminara el aviso.

Hasta Django 6.0, seguirá existiendo el aviso. Esto se puede controlar
de dos maneras:

-  Adoptar el comportamiento futuro con el valor de configuración
   ``FORMS_URLFIELD_ASSUME_HTTPS``.

   .. code:: python

      FORMS_URLFIELD_ASSUME_HTTPS = True

   Esto hará que **todos** los campos de tipo ``URLField`` asumen que el
   esquema por defecto es ``https``.

-  Migrar individualmente los campos de tipo ``forms.URLField``
   añadiendo el esquema por defecto.

   Con esta opción, hay que añadir el parámetro opcional
   ``assume_schema`` a cada instancia de ``URL Field``. Se puede ajustar
   el valor a ``https``, que el el comportamiento futuro por defecto, o
   ``http`` para mantener el comportamiento anterior.

De cualquiera de las dos maneras desactivaremos el aviso.

Fuente: `Fix version 5.0’s URLField.assume_scheme warnings`_ - `Adam Johnson`_

.. _Fix version 5.0’s URLField.assume_scheme warnings: https://adamj.eu/tech/2023/12/07/django-fix-urlfield-assume-scheme-warnings/
.. _Adam Johnson: https://adamj.eu/


