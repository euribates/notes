---
title: Notas sobre Django Admin
tags:
    - vim
    - django
    - editor
    - database
---


## Cómo hacer que un método booleano se vea bonito en el admin

Esta documentado, pero a menudo resulta complicado de encontrar. Si escribimos
un método de un modelo que devuelve solo `True` o `False`, y lo consultamos en el
admin, este nos muestra texto. Sin embargo, para campos definidos como
booleanos (`BooleanField`) nos muestra un icono. Podemos hacer que utilice esos
mismos iconos si **añadimos un atributo `boolean` al método**.  por ejemplo:

```python
def nacio_en_bisiesto(self):
    year = self.birthday.year
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

nacio_en_bisiesto.boolean = True
```

Fuente:

- [El Ornitorrinco Enmascarado: Recetas Habituales en Django (Que siempre se me olvidan)](http://elornitorrincoenmascarado.blogspot.com/2015/10/recetas-habituales-en-django-que.html)


## Cómo mostrar contenido html en el admin

Para que el _admin_ interprete cualquier texto producido por un método como HTML,
sin escaparlo, debemos **asignar al método el atributo `allow_tag` a `True`**.
Es recomendable que nos escudemos de posibles fallos de seguridad **usando la
función `format_html()`** siempre que incluyamos en la salida texto generado
por el usuario final. Por ejemplo:

```python
def colored_name(self):
    return format_html('<span style="color: #{};">{} {}</span>',
        self.color_code,
        self.first_name,
        self.last_name,
        )

colored_name.allow_tags = True
```

Fuente:

- [El Ornitorrinco Enmascarado: Recetas Habituales en Django (Que siempre se me olvidan)](http://elornitorrincoenmascarado.blogspot.com/2015/10/recetas-habituales-en-django-que.html)




## Cómo personalizar el admin de Django

Podemos personalizar muchas partes del _Admin_, usando diferentes técnicas.
La más sencilla es usar la clase `admin.ModelAdmin` de la que se derivan
nuestras propias clases _Admin_. La clase `ModelAdmin` tiene más de 30
atributos y aproximadamente 50 métodos que podemos usar o reimplementar.

Podemos dividir el _Admin_ en tres áreas principales:

- Índice de _Apps_ (`app index`): Lista los modelos registrados.

- Listas de instancias (`change list`): Se crea una lista para cada
  modelo registrado.

- Formularios de cambios (`change form`): Se crea automáticamente una
  vista de este tipo para cada clase registrada, que nos permite
  editar una instancia.


## Atributos personalizables de la clase `ModelAdmin`

- `list_display`: Especifica las columnas que se montrarán en los
  listados. Es una tupla con los nombres de los campos o métodos
  que queremos para cada columna. También puede referirse a un método
  de la clase derivada de `ModelAdmin`.

- `list_filter`: Si definimos `list_filter` como una tupla de campos, aparecerá
  una nueva sección en el listado, con diferentes opciones que cubren todos los
  posibles valores encontrados en la base de datos.

= `search_fields`: Especifica los campos que serán tenidos en cuenta
  cuando se haga una búsqueda. Por defecto es una lista vacía, así que no
  aparece el cuadro de búsqueda, pero en cuanto pongamos aquí uno o más
  nombres de campos, la búsqueda se activará automáticamente.

  Cuando se efectua la búsqueda, se llama al método `get_search_results()`,
  que devuelve un _queryset_. Se puede afinar la búsqueda redefiniendo
  este método y modificando el
  _queryset_ a nuestra conveniencia.

- `fields`: You can control which fields are included, as well as their order,
  by editing the fields option


- `form`: La clase del Formulario a usar para editar una instancia del modelo.
  Si no lo definimos,
  Se genera automáticamente a partir del modelo.

- [Documentación sobre `ModelAdmin`](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/)

## Métodos de la clase `ModelAdmin`

- `get_form()`: Este método es el responsable de crear el formulario
  para editar na instancia del modelo. Se puede reimplementar este
  método para modificarlo, como en el siguiente ejemplo:

  ```py
  def get_form(self, request, obj=None, **kwargs):
    form = super().get_form(request, obj, **kwargs)
    form.base_fields["name"].label = "Nombre (Solo para humanos):"
    return form
  ```

  O para crear un nuevo formulario desde cero, si es necesario, aunque
  quizá sea más fácil en este caso definir el atributo `form` a la clase
  del formulario que queremos usar.

- `get_search_results()`: Este método realiza las búsquedas, devolviendo un
  _queryset_ con el resultado. Podemos sobreescribir este método y hacer las
  modificaciones que creamos oportunas. Se puede usar, por ejemplo, para
  ampliar el lenguaje de consultas, o para hacer anotaciones o agregados
  sobre el resultado.

Fuentes:

- [Documentación sobre `ModelAdmin`](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/)


## Como añadir acciones al Admin de Django

Lo primero que necesitamos en escribir la función que será llamada
cuando se ejecute la acción. Esta función debe aceptar **tres** parámetros:

- La instancia del `ModelAdmin`.

- El objeto `HttpRequest` de la petición.

- Un `QuerySet` que contiene los objetos seleccionados por el usuario.

El siguiente ejemplo solo cambie el estado de los objetos en el
_queryset_, así que no necesita ninguno de los dos primeros parámetros:


```py
from django.utils import timezone

def make_published(model_admin, request, queryset):
    queryset.update(status='PUB', f_published=timezone.now())
```

Nota: También puede tener sentido definir la acción como un método
del `ModelAdmin`. Es este caso el primer parámetro es el mismo, pero
usaremos la convención de llamarlo `self`.


### registrar la acción para que aparezca en el Admin

Para que aparezca la opción en el _Admin_, tenemos que registrarla. La
forma más sencilla es usando el decorador `@admin.action`, que nos permite
además especificar una descripción para la acción. Una vez marcada como una
acción, podemos añadirla a el o los `modelAdmin` (Puede tener sentido que una
misma `action` se pueda aplicar a varios modelos) en el atributo `actions`:

```py
from django.contrib import admin
from django.utils import timezone

from myapp.models import Article


@admin.action(description="Marcar como publicado")
def make_published(model_admin, request, queryset):
    queryset.update(status='PUB', f_published=timezone.now())


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "status"]
    ordering = ["title"]
    actions = [make_published]


admin.site.register(Article, ArticleAdmin)
```

Si fuera un método, en ves de una función externa, en `actions` tendremos que
usar una cadena de texto para especificarlo, en vez de usar directamente la
función:

```py
class ArticleAdmin(admin.ModelAdmin):
    ...

    actions = ["make_draft"]

    @admin.action(description="Mark selected stories as published")
    def make_draft(self, request, queryset):
        queryset.update(status="DRAFT")
```

### Acciones más complicadas o avanzadas

En otros casos tendremos que pedir datos adicionales: Una confirmación de
la solicitud, por ejemplo, o preguntar más detalles necesarios para la
operación. Eso nos obliga a pasar por una página intermedia.

Para ello, en vez de tener un método/función que no devuelve nada, devolveremos
un objeto de tipo `HttpResponseRedirect` que nos dirige a una página definida
por nosotros, y que acepta el `queryset` original.

```py
from django.http import HttpResponseRedirect


def issue_certificate(modeladmin, request, queryset):
    selected = queryset.values_list("pk", flat=True)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect(
        "/export/?ct=%s&ids=%s"
        % (
            ct.pk,
            ",".join(str(pk) for pk in selected),
        )
```

Esta página puede definir una plantilla que derive de `admin/base.html` para
que se integre bien con el _Admin_.


## Cómo enlazar a una página dentro del admin

La _app_ `admin` proporciona los siguientes patrones de enlace:

| Page                 | URL name               | Parameters                     |
|----------------------|------------------------|--------------------------------|
| Índice               | `index`                |                                |
| _Login_              | `login`                |                                |
| _Logout_             | `logout`               |                                |
| Password change      | `password_change`      |                                | 
| Password change done | `password_change_done` |                                | 
| i18n JavaScript      | `jsi18n`               |                                |
| Lista de _apps_      | `app_list`             | `app_label`                    |
| Redirección          | `view_on_site`         | `content_type_id`, `object_id` |


Cada instancia de `ModelAdmin` proporciona un conjunto adicional de URLs:


| Page       | URL name                              | Parameters  |
|------------|---------------------------------------|-------------|
| Changelist | `<app_label>_<model_name>_changelist` |             |
| Add        | `<app_label>_<model_name>_add`        |             |
| History    | `<app_label>_<model_name>_history`    | `object_id` |
| Delete     | `<app_label>_<model_name>_delete`     | `object_id` |
| Change     | `<app_label>_<model_name>_change`     | `object_id` |

Por ejemplo, para enlazar con la página de edición (*change*) del modelo
`Libro` dentro de la _app_ `biblioteca`, sería:

```
admin:biblioteca_libro_change <object_id>
```

Fuentes:

- [Reversing admin URLs](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#reversing-admin-urls)



## Cómo modificar el queryset usado en el admin para incluir un select_related

No hay que modificar el formulario en si, sino modificar la
clase derivada de `ModelAdmin`. Django incluye un método específico
para esto en la clase madre, `formfield_for_foreignkey`.

De la documentación:

> ModelAdmin.formfield_for_foreignkey(self, db_field, request, \*\*kwargs):
>
> The formfield_for_foreignkey method on a ModelAdmin allows you to
> override the default formfield for a foreign keys field. For example,
> to return a subset of objects for this foreign key field based on the
> user

Veámoslo con un ejemplo:

```python
class MyModelAdmin(admin.ModelAdmin):
    ...
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "car":
            kwargs["queryset"] = Car.objects.filter(
                owner=request.user
            )
        return super(MyModelAdmin, self).formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )
```


## Cómo usar formularios diferentes en el admin para insertar y modificar

Usa el método `get_form` de la clase `ModelAdmin`, y devuelve el formulario que
necesites en cada caso. Puedes discriminar si es un `UPDATE` o un `INSERT`
mirando el parámetro `obj`: Si es `None` se trata de un alta, si no, se trata
de una modificación y `obj` es el modelo modificado.

Un ejemplo:

```python
class AdminBiografia(admin.ModelAdmin):

    ...

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            kwargs['form'] = EditarBiografiaAdminForm
        else:
            kwargs['form'] = NuevaBiografiaAdminForm
        return super().get_form(request, obj, **kwargs)§
```


## Cómo sobreescribir las plantillas del Admin

El orden de carga de las plantillas usado por Django
es usar la primera que se encuentra con un determinado nombre,
buscando las _apps_ en el orden determinado en el fichero `settings.py`.

Como tradicionalmente se pone el `admin` al final,
eso implica que podemos
**sobreescribir las plantillas usadas**
en el admin por las nuestras, incluyendo en nuestras apps
**la misma estructura de directorios y nombres de ficheros**
que el admin.

!!! note "Otra posibilidad es definir `TEMPLATES.DIRS`"

    Podemos crear un directorio solo para los cambios en el admin,
    e incluirlo en lavariable `TEMPLATES`, en el fichero `settings.py`,
    bajo la entrada `DIRS`. Las carpetas que se definan en esta
    variable siempre son buscadas antes que las de las aplicaciones.

Este es el esquema de plantillas usando en el _Admin_:

```
▶ tree admin/
templates/admin/
├── 404.html
├── 500.html
├── actions.html
├── app_index.html
├── app_list.html
├── auth
│   └── user
│       ├── add_form.html
│       └── change_password.html
├── base.html
├── base_site.html
├── change_form.html
├── change_form_object_tools.html
├── change_list.html
├── change_list_object_tools.html
├── change_list_results.html
├── color_theme_toggle.html
├── date_hierarchy.html
├── delete_confirmation.html
├── delete_selected_confirmation.html
├── edit_inline
│   ├── stacked.html
│   └── tabular.html
├── filter.html
├── includes
│   ├── fieldset.html
│   └── object_delete_summary.html
├── index.html
├── invalid_setup.html
├── login.html
├── nav_sidebar.html
├── object_history.html
├── pagination.html
├── popup_response.html
├── prepopulated_fields_js.html
├── search_form.html
├── submit_line.html
└── widgets
    ├── clearable_file_input.html
    ├── date.html
    ├── foreign_key_raw_id.html
    ├── many_to_many_raw_id.html
    ├── radio.html
    ├── related_widget_wrapper.html
    ├── split_datetime.html
    ├── time.html
    └── url.html
```

y el de `registrations`, usado para los cambios de usuario
y las operaciones de _login_ y _logout_:

```
registration/
├── logged_out.html
├── password_change_done.html
├── password_change_form.html
├── password_reset_complete.html
├── password_reset_confirm.html
├── password_reset_done.html
├── password_reset_email.html
└── password_reset_form.html
```

Por ejemplo, si quisiéramos cambiar la página de login, podemos crear una
carpeta `admin` en uno de los directorios `templates` de  nuestras _apps_, y
dentro de ella, el fichero `login.html`. Si quieramos también redefinir
la página que informa de que hemos salido (_logout_), tendríamos que crear
una carpeta `registration` y dentro de esta, una plantilla `logged_out.html`.


