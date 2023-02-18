---
title: Notas sobre formularios con django-crispy-forms
tags:
  - python
  - django
  - patterns
  - css
---

## Sobre django-crispy-forms

**django-crispy-forms** propociona filtros y etiquetas adicionales para las plantillas
Django que permiten controlar la presentación  de formularios Django de forma
elegante y respetando el principio DRY.


## Form Helpers

La clase `FormHelper` nos permite definir varias características que deseemos
para un formulario. El primer paso será importarlo:

```python
from crispy_forms.helper import FormHelper
```

Podemos usar el _helper_ como una variable de clase o como una instancia.
Como regla general, si no vamos a modificar el _helper_ dinámicamente,
deberíamos usarlo como variable de clase.

Veamos un ejemplo creado una instancia de clase:

```python
from crispy_forms.helper import FormHelper

class ExampleForm(forms.Form):
    [...]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
```

Una vez creado la instancia (Podemos llamarla como queramos, pero es mejor
usar el nombre `helper`, por razones que se verán más adelante), podemos
definir una serie de propiedad, la mayoría de las cuales afectarán a la forma
en que se representan los atributos del formulario y sus campos.

Por ejemplo, podemos definir que `id` tendrá el formulaario definiendo en la
instancia del _helper_ el atributo `form_id`:

```python
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ExampleForm(forms.Form):
    [...]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
```

Igualmente, podemos definir la clase o clases asignadas al formulario con el
atributo `form_class`, el método a usar con `form_method` y la acción con
`form_action`. Veamos un ejemplo más extenso en que asignamos al formulario la
clase `BlueForm`, el método `POST` y como acción, `submit_survey`:

```python
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ExampleForm(forms.Form):
    [...]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'POST'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Submit'))
```

Con `add_input` hemos añadido un botón de _submit_, esto es necesario para
poder representar el formulario funcional en la plantilla, ya que el _tag_
`crispy`, al contrario que los _filtros_ para formularios de Django como
`as_tabla` o `as_div`, se ocupará de mostrar **todo** el formulario, incluyendo
las etiquetas de `<form>` y `</form>`. Volveremos más adelante sobre
`add_input`.

Para poder mostrar todos estos cambios en la plantilla, tenemos que indicarle
al tag `crispy` tanto el formulario como la clase o instancia _helper_ a usar:

```python
{% load crispy_forms_tags %}
{% crispy example_form example_form.helper %}
```

Pero, y aquí viene la importancia del nombre, si hemos seguido el consejo anterior
sobre llamar al _helper_ `helper`, solo tendremos que especificar el primer
parámetro:

```python
{% crispy example_form %}
```

Una ventaja de usar el _helper_ es que se añade automáticamente el _tag_
de Django `{% csrf_token %}`, algo que yo siempre olvido.


## Como definir el framework CSS a utilizar para los formularios

La librería viene con **Bootstrap 4** como opción por defecto para
mostrar los formularios. Podemos forzar otra opción o bien localmente en la
definición del _helper_, ajustando la propiedad `template_pack`, o definiendo
esta preferencia a nivel global con la constante `CRISPY_TEMPLATE_PACK`.

Por ejemplo, podemos usar _Bootstrap_ 3 con:

```python
CRISPY_TEMPLATE_PACK = 'bootstrap3'
```


## Cómo usar Crispy Forms con dos o más formularios

Si el _tag_ `{% crispy form %}` pone por nosotros las etiquetas de principio y
fin del formulario, no podríamos en principio representar dos formularios, con
sus respectivos _helpers_, dentro de un único bloque `<form>...</form>`. Para
eso existe el atributo `form_tag`, que podemos poner a `False` para indicarle
que seremos nosotros los que nos ocuparemos de poner las etiquetas de principio
y fin de formulario.

De igual manera, podemos usar el atributo booleano `disable_csrf` y ponerlo a
`False` (Por defecto es `True`) para indicarle que nosotros nos encargaremos de
incluir el token por nuestra cuenta.

```python
class FormSomething(...):
    ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_tag = False
        self.disable_csrf = True
```

## Cómo marcarlos campos obligatorios usando crispy forms

Por defecto, _Crispy Forms_ destaca los campo obligatorios con un asterisco
rojo. Hay dos opciones para cambiar esto:

La primera es redefiniendo la clase _CSS_ `asteriskField`, que _crispy_ usa para
este tipo de asteríscos. Por ejemplo, el siguiente fragmento de _CSS_ cambia
el color a un tono azul:

```css
.asteriskField {
    color: #2F437E;
}
```

La otra opción es sobreescribir la plantilla `field.html` con tu versión personalizada.


## Cómo hacer que crispy-forms informe de los fallos.

Por defecto, `crispy-forms` no reporta los errores, en caso de fallo, envía
un error usando el sistema de _log_ y continua, si puede. Podemos definir en el
`settings.py` una variable `CRISPY_FAIL_SILENTLY`. Si se pone a `True`, en vez de
simplemente enviar el error al _log_, eleva una excepción. Una forma sugerida de usar
este valor es:

```python
CRISPY_FAIL_SILENTLY = not DEBUG
```




