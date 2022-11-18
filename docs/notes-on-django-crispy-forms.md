## Notes on django-crispy-forms

### Form Helpers

Let’s see how helpers works step by step, with some examples explained. First you will need to import FormHelper:

```python
from crispy_forms.helper import FormHelper
```

Your helper can be a class level variable or an instance level variable, if you don’t know what this means you might want to read the article “Be careful how you use static variables in forms”. As a rule of thumb, if you are not going to manipulate a FormHelper in your code, like in a view, you should be using a static helper, otherwise you should be using an instance level helper.

let's create an instance variable:
```python
from crispy_forms.helper import FormHelper

class ExampleForm(forms.Form):
    [...]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
```

We’ve also done some helper magic. FormHelper has a list of attributes that can
be set, that affect mainly form attributes. Our form will have as DOM `id
id-exampleForm`, it will have as DOM CSS class `blueForms`, it will use http
`POST` to send information and its action will be set to
`reverse(submit_survey)`.

Let’s see how to render the form in a template. Supposing we have the form in the template context as `example_form`, we would render it doing:

```python
{% load crispy_forms_tags %}
{% crispy example_form example_form.helper %}
```

Notice that the `{% crispy %}` tags expects **two parameters**: first **the form** variable and then the **helper**. If you name your `FormHelper` attribute `helper` you will only need to do:

```python
{% crispy form %}
```



