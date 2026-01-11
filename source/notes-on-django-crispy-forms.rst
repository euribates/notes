django-crispy-forms
========================================================================

.. tags:: python,django,patterns,css


Sobre django-crispy-forms
------------------------------------------------------------------------

**django-crispy-forms** propociona filtros y etiquetas adicionales para
las plantillas Django que permiten controlar la presentación de
formularios Django de forma elegante y respetando el principio DRY.

Form Helpers
------------------------------------------------------------------------

La clase ``FormHelper`` nos permite definir varias características que
deseemos para un formulario. El primer paso será importarlo:

.. code:: python

    from crispy_forms.helper import FormHelper

Podemos usar el *helper* como una variable de clase o como una
instancia. Como regla general, si no vamos a modificar el *helper*
dinámicamente, deberíamos usarlo como variable de clase.

Veamos un ejemplo creado una instancia de clase:

.. code:: python

    from crispy_forms.helper import FormHelper

    class ExampleForm(forms.Form):

        ...

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()

Una vez creado la instancia (Podemos llamarla como queramos, pero es
mejor usar el nombre ``helper``, por razones que se verán más adelante),
podemos definir una serie de propiedad, la mayoría de las cuales
afectarán a la forma en que se representan los atributos del formulario
y sus campos.

Por ejemplo, podemos definir que ``id`` tendrá el formulario definiendo
en la instancia del *helper* el atributo ``form_id``:

.. code:: python

    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Submit

    class ExampleForm(forms.Form):

        ...
    
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_id = 'id-exampleForm'

Igualmente, podemos definir la clase o clases asignadas al formulario
con el atributo ``form_class``, el método a usar con ``form_method`` y
la acción con ``form_action``. Veamos un ejemplo más extenso en que
asignamos al formulario la clase ``BlueForm``, el método ``POST`` y como
acción, ``submit_survey``:

.. code:: python

    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Submit

    class ExampleForm(forms.Form):

        ...
    
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_id = 'id-exampleForm'
            self.helper.form_class = 'blueForms'
            self.helper.form_method = 'POST'
            self.helper.form_action = 'submit_survey'
            self.helper.add_input(Submit('submit', 'Submit'))

Con ``add_input`` hemos añadido un botón de *submit*, esto es necesario
para poder representar el formulario funcional en la plantilla, ya que
el *tag* ``crispy``, al contrario que los *filtros* para formularios de
Django como ``as_tabla`` o ``as_div``, se ocupará de mostrar **todo** el
formulario, incluyendo las etiquetas de ``<form>`` y ``</form>``.
Volveremos más adelante sobre ``add_input``.

Para poder mostrar todos estos cambios en la plantilla, tenemos que
indicarle al tag ``crispy`` tanto el formulario como la clase o
instancia *helper* a usar:

.. code:: django-template

    {% load crispy_forms_tags %}
    {% crispy example_form example_form.helper %}

Pero, y aquí viene la importancia del nombre, si hemos seguido el
consejo anterior sobre llamar al *helper* ``helper``, solo tendremos que
especificar el primer parámetro:

.. code:: django-template

    {% crispy example_form %}

Una ventaja de usar el *helper* es que se añade automáticamente el *tag*
de Django ``{% csrf_token %}``, algo que yo siempre olvido.


Como definir el framework CSS a utilizar para los formularios
------------------------------------------------------------------------

La librería viene con **Bootstrap 4** como opción por defecto para
mostrar los formularios. Podemos forzar otra opción o bien localmente en
la definición del *helper*, ajustando la propiedad ``template_pack``, o
definiendo esta preferencia a nivel global con la constante
``CRISPY_TEMPLATE_PACK``.

Por ejemplo, podemos usar *Bootstrap* 3 con:

.. code:: python

    CRISPY_TEMPLATE_PACK = 'bootstrap3'


Cómo usar Crispy Forms con dos o más formularios
------------------------------------------------------------------------

Si el *tag* ``{% crispy form %}`` pone por nosotros las etiquetas de
principio y fin del formulario, no podríamos en principio representar
dos formularios, con sus respectivos *helpers*, dentro de un único
bloque ``<form>...</form>``. Para eso existe el atributo ``form_tag``,
que podemos poner a ``False`` para indicarle que seremos nosotros los
que nos ocuparemos de poner las etiquetas de principio y fin de
formulario.

De igual manera, podemos usar el atributo booleano ``disable_csrf`` y
ponerlo a ``False`` (Por defecto es ``True``) para indicarle que
nosotros nos encargaremos de incluir el token por nuestra cuenta.

.. code:: python

    class FormSomething(...):

        ...

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False
            self.helper.disable_csrf = True

Cómo marcarlos campos obligatorios usando crispy forms
------------------------------------------------------

Por defecto, *Crispy Forms* destaca los campo obligatorios con un
asterisco rojo. Hay dos opciones para cambiar esto:

La primera es redefiniendo la clase *CSS* ``asteriskField``, que
*crispy* usa para este tipo de asteríscos. Por ejemplo, el siguiente
fragmento de *CSS* cambia el color a un tono azul:

.. code:: css

    .asteriskField {
      color: #2F437E;
      }

La otra opción es sobreescribir la plantilla ``field.html`` con tu
versión personalizada.

Cómo hacer que crispy-forms informe de los fallos.
------------------------------------------------------------------------

Por defecto, ``crispy-forms`` no reporta los errores, en caso de fallo,
envía un error usando el sistema de *log* y continua, si puede. Podemos
definir en el ``settings.py`` una variable ``CRISPY_FAIL_SILENTLY``. Si
se pone a ``True``, en vez de simplemente enviar el error al *log*,
eleva una excepción. Una forma sugerida de usar este valor es:

.. code:: python

    CRISPY_FAIL_SILENTLY = not DEBUG

Cómo usar Layouts
------------------------------------------------------------------------

Existe una clase ``Layout``, que nos permite definir la forma en que se
visualiza el formulario. Podemos por ejemplo definir el orden en que
queremos visualizar los campos, y si queremos organizarlos en grupos de
``divs``, por ejemplo, sin tener que tocar las plantillas.

Los *Layouts* son opcionales, pero seguramente es la parte más potente
de ``django-crispy-forms``.

Los *layouts* se construyen como un árbol, veamos un ejemplo (Los
*imports* se han omitido, pero la clase ``Layout`` y derivadas, como
``FieldSet`` o ``Submit`` en el ejemplo, están en
``crispy_forms.layout``):

.. code:: python

    class ExampleForm(forms.Form):

        ...

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Fieldset(
                    'first arg is the legend of the fieldset',
                    'like_website',
                    'favorite_number',
                    'favorite_color',
                    'favorite_food',
                    'notes'
                    ),
                Submit('submit', 'Submit', css_class='button white'),
            )

Si usamos la etiqueta ``crispy`` para mostrar este formulario, veremos que
agrupa dentro de cada *fieldset* los campos que le hemos indicado. Atentos
a que el primer parámetro no es un campo,
sino la descripción textual o encabezado que se muestra para cada
sección. Además, incluye el botón de *submit* que hemos incluido en el
*layout*.

Cómo incluir contenido extra en el formulario
------------------------------------------------------------------------

Usando *layouts*, Podemos incluir dentro del ``FieldSet``, en cualquier
posición, el contenido que queramos, usando ``HTML``, ``Div``,
``Multifield``, ``SubmiyButton`` o ``Button`` entre otros (Todos estas
clases están definidcas en ``crispy_forms.layout``.

Todos estos objetos de tipo *layout* pueden ser creado con atributos por
nombre, que serán luego representados como atributos del *tag* Html. Hay
tres excepciones, sin embargo:

- Para atributos que tengan un guión en su nombre, como por ejemplo
  ``data-name``, como Python no considera el guión un símbolo apto para
  nombres de variables, hay que usar el mismo nombre que queremos pero
  sustituyendo el guión por el carácter subrayado ``_``. Por ejemplo:

.. code:: python

    Field('field_name', data_name="whatever")

- Para especificar la clase, como ``class`` es una palabra reservada en
  Python, usaremos ``css_class`` como nombre del parámetro. Por ejemplo:

.. code:: python

    Field('field_name', css_class="black-fields")

- Igualmente para el identificador ``id``. En este caso no es una
  palabra reservada, sino una de las funciones básicas incluidas en el
  intérprete, (Ver `Función id en python`_

  Para este caso usaremos el atributo ``css_id``. Por ejemplo:

.. code:: python

    Field('field_name', css_id="custom_field_id")

.. note:: ``Field`` se puede utilizar cuando queremos un control más
   completo, si no es el caso, a funciones como ``Div`` o ``Fieldset``
   basta con pasarle el nombre del campo, y el propio componente crea el
   valor ``Field`` necesario.

Los elementos que podemos usar para formar el Layout son:

- **Div**: Para incluir los componentes en un elemento ``div``

- **HTML**: Html genérico: Lo bueno es que podemos usar etiquetas y
  filtro del sistema de plantillas, teniendo acceso a todo el contexto
  de la página. Este componente no acepta atributos. Podemos incluso
  cargar extensiones con ``load``.

- **FIeld**

- **Submit**

- **Button**

- **Hidden**

- **Reset**

- **Fieldset**

- **MultiField**

Cómo determinar el control o *widget* a usar en un campo
------------------------------------------------------------------------

Lo más sencillo es sobreescribir el método ``__init__``, y realizar las
modificaciones usando el atributo ``fields`` del formulario, que nos da
acceso a los campos definidos en el mismo.

.. code:: python

    class DeviceFilterForm(forms.Form):

        def __init__(self, *args, **kwargs):
            super(DeviceFilterForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.fields['updated_date'].widget = forms.DateInput(attrs={
                'required': True,
                'class': 'date-time-picker',
                'data-options': '{"format":"Y-m-d H:i", "timepicker":"true"}'
                })

.. note:: Esto funciona tambien para formularios que no usen
          Crispy-forms. Solo tenemos que modificar con ``fields`` los
          valores que nos interese.

Fuente: `jquery - How to use widgets in Django Crisp Forms - Stack
Overflow <https://stackoverflow.com/questions/57500962/how-to-use-widgets-in-django-crisp-forms>`_

.. _Función id en python: https://docs.python.org/es/3/library/functions.html#id
