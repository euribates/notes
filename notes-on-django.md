---
title: Notes on Django
---

## Default error handlers

It's worth reading the documentation of the default error handlers,
`page_not_found`, `server_error`, `permission_denied` and `bad_request`. By
default, they use these templates if they can find them, respectively:
`404.html`, `500.html`, `403.html`, and `400.html`.

So if all you want to do is make pretty error pages, just create those files in
a `TEMPLATE_DIRS` directory, you don't need to edit URLConf at all. [Read the
documentation](https://docs.djangoproject.com/en/4.1/topics/http/views/#customizing-error-views) to see which context variables are available.

In Django 1.10 and later, the default CSRF error view uses the template
`403_csrf.html`.

Note: Don't forget that `DEBUG`` must be set to `False` for these to work,
otherwise, the normal debug handlers will be used.

## How to make a Form dynamically

TL/DR: Add or change fields during initialization of the form using the
`fields` attribute.

Forms are usually defined in a declarative style, with form fields listed as
class fields. However, sometimes we do not know the number or type of these
fields in advance. This calls for the form to be dynamically generated. This
pattern is sometimes called dynamic form or runtime form generation.

Every form instance has an attribute called `fields`, which is a dictionary
that holds all the form fields. This can be modified at runtime. Adding or
changing the fields can be done during form initialization itself.

For example, if we need to add a checkbox to a user-details form only if a
keyword argument named "upgrade" is true upon form initialization, then we can
implement it as follows:

```python
class PersonDetailsForm(forms.Form): 
    name = forms.CharField(max_length=100) 
    age = forms.IntegerField() 

    def __init__(self, *args, **kwargs): 
        upgrade = kwargs.pop("upgrade", False) 
        super().__init__(*args, **kwargs) 

        # Show first class option? 
        if upgrade: 
            self.fields["first_class"] = forms.BooleanField( 
                label="Fly First Class?") 
```

Now, we just need to pass the `PersonDetailsForm(upgrade=True)` keyword argument to
make an additional Boolean input field (a checkbox) appear.

!!! warning
    A newly introduced keyword argument has to be removed or popped before we
    call super to avoid the unexpected keyword error.

!!! warning
    If we use a `FormView` class for this example, then we need to pass the
    keyword argument by overriding the `get_form_kwargs` method of the View
    class.

This pattern can be used to change any attribute of a field at runtime, such as
its widget or help text. It works for model forms as well.

Source: Book [Django Design Patterns and Best
Practice](https://www.packtpub.com/product/django-design-patterns-and-best-practices-second-edition/9781788831345)

## How to Migrate to 3.1.1

- **NullBooleanField** is obsolete, replace it by
  `BooleanField(null=True)`.
- **load staticfiles** and **load admin\_static** are obsoletes since
  Django 2.1, deprecated in Django 3.0.

   Change this references in the templates from:
```django
{% load staticfiles %}
{% load static from staticfiles %}
{% load admin_static %}
```
   to just:
```django
{% load static %}
```

## Set VIM to handle Django template files

Type `:setfiletype htmldjango` from within Vim to select highlighting for
Django HTML templates. If you desire Django template highlighting but not HTML
highlighting, type `:setfiletype django` instead. Items highlighted include
template tags, built-in filters, arguments and comments.

Source: [Syntax highlighting for django templates](https://www.vim.org/scripts/script.php?script_id=1487) 

Tags: vim, django, editor

## What are the possible values of `on_delete` in a model field

This is the behaviour to adopt when the referenced object is deleted. It
is not specific to django, this is an SQL standard.

There are 6 possible actions to take when such event occurs:

- `CASCADE`: When the referenced object is deleted, also delete the
  objects that have references to it (When you remove a blog post for
  instance, you might want to delete comments as well). SQL
  equivalent: CASCADE.

- `PROTECT`: Forbid the deletion of the referenced object. To delete
  it you will have to delete all objects that reference it manually.
  SQL equivalent: RESTRICT.
  
- `SET_NULL`: Set the reference to NULL (requires the field to be
  nullable). For instance, when you delete a User, you might want to
  keep the comments he posted on blog posts, but say it was posted by
  an anonymous (or deleted) user. SQL equivalent: SET NULL.

- `SET_DEFAULT`: Set the default value. SQL equivalent: SET DEFAULT.

- `SET(...)`: Set a given value. This one is not part of the SQL
standard and is entirely handled by Django.

- `DO_NOTHING`: Probably a very bad idea since this would create
  integrity issues in your database (referencing an object that
  actually doesn't exist). SQL equivalent: NO ACTION.

See also the documentation of PostGreSQL for instance.

In most cases, `CASCADE` is the expected behaviour, but for every
`ForeignKey`, you should always ask yourself what is the expected
behaviour in this situation. `PROTECT` and `SET_NULL` are often useful.
Setting `CASCADE` where it should not, can potentially **delete all your
database in cascade**, by simply deleting a single user.

Additional note to clarify cascade direction

It's funny to notice that the direction of the `CASCADE` action is not
clear to many people. Actually, it's funny to notice that only the
`CASCADE` action is not clear. I understand the cascade behavior might
be confusing, however you must think that it is the same direction as
any other action. Thus, if you feel that `CASCADE` direction is not
clear to you, it actually means that `on_delete` behavior is not clear
to you.

In your database, a foreign key is basically represented by an integer
field which value is the primary key of the foreign object. Let's say
you have an entry `comment_A`, which has a foreign key to an entry
`article_B`. If you delete the entry `comment_A`, everything is fine,
`article_B` used to live without `comment_A` and don't bother if it's
deleted. However, if you delete `article_B`, then `comment_A` panics! It
never lived without `article_B` and needs it, it's part of its
attributes (`article=article_B`, but what is *article\_B*?). This is
where `on_delete` steps in, to determine how to resolve this integrity
error, either by saying:

- "No! Please! Don't! I can't live without you!" (which is said
  `PROTECT` in SQL language)

- "Alright, if I'm not yours, then I'm nobody's" (which is said
  `SET_NULL`)

- "Good bye world, I can't live without `article_B`" and commit
  suicide (this is the `CASCADE` behavior).

- "It's OK, I've got spare lover, I'll reference `article_C` from now"
  (`SET_DEFAULT`, or even `SET(...)`).

- "I can't face reality, I'll keep calling your name even if that's
  the only thing left to me!" (`DO_NOTHING`)

I hope it makes cascade direction clearer. :)

Source: [Best practices working with Django models](https://steelkiwi.com/blog/best-practices-working-django-models-python/)

Tags: Databases

## How to make a multiple form, this is, a form across several pages

Use the external app
[django-formtools](https://github.com/django/django-formtools/).

This use to be in the django main distribution, but was split as a
separated app sinde Django 1.8. For this functionality, you'll need the
Form Wizard class, as explained here: [Form wizard](https://django-formtools.readthedocs.io/en/latest/wizard.html).

## Como usar el método `extra` de los queryset para consultas avanzadas

El método `extra` de los queryset nos permite realizar algunas
modificaciones en las sentencias sql que ejecuta. En concreto nos
permite añadir campos a la cláusula `SELECT`, o tablas y joins a la
cláusula `FROM`, o condiciones a la cláusula `ORDER BY`.

Supongamos, por ejemplo, que tenemos una tabla de productos a la venta,
algo como esto:

```python
class Item(Model):
    id = AutoField(primary_key=True)  # Me gusta especificar la clave
    descripcion = CharField(max_length=200)
    pvp = DecimalField(max_digits=12, decimal_places=2)
    alta = DateTimeField(auto_now_add=True)
```

Podemos añadir un campo calculado que nos indique si los precios son
inferiores a 5.0 (quizá queremos marcar estos productos en la página con
un icono de `_low-price_`, por ejemplo). Para ello, podemos añadir un
campo calculado al _select_ de la query usando `extra`, como en el siguiente
ejemplo:

```python
Item.objects.extra(select={'low_price':'pvp < 5.0'}).all()
```

Source: [Best practices working with Django models](https://steelkiwi.com/blog/best-practices-working-django-models-python/)

Lo que estamos haciendo es que la sentencia SQL generada por Django pase
de esto:

```sql
SELECT app_item.*
  FROM app_item;
```

a esto:

```sql
SELECT app_item.*, (pvp < 5.0) AS low_price
  FROM app_item;
```

Podemos pasar varios campos calculados en el diccionario especificado
por el parámetro select, o hacer varias llamadas a extra. Por ejemplo,
si queremos clasificar los precios en tres bandas, (baratos, por debajo
de 5 euros; medios, entre 5 y 100 euros y caros, por encima de 100
euros), podemos hacerlos así:

```sql
Item.objects.extra(select={
    'low_price':'pvp < 5.0',
    'mid_price':'pvp between 5.0 and 100.0',
    'low_price':'pvp > 100.0',
    }).all()
```

O así:

```sql
Item.objects  \
    .extra(select={'low_price':'pvp < 5.0'})  \
    .extra(select={'mid_price':'pvp between 5.0 and 100.0'}) \
    .extra(select={'low_price':'pvp > 100.0'})  \
    .all()
```

El resultado debería ser el mismo en los dos casos.

Es verdad que podemos realizar este calculo de bandas de precios en un simple
método de la clase `Item`, pero en ocasiones puede ser útil o necesario que
determinadas operaciones las haga la base de datos por nosotros.

Obviamente también podemos pasar subconsultas como campo añadido al select, que
nos da aun más posibilidades. Por ejemplo, supongamos que en nuestra aplicación
tiene otro modelo con las puntuaciones que nuestros clientes asignan a nuestros
artículos, algo como esto:

```python
class Score(models.Model):
    id = AutoField(primary_key=True)  # Si, ya lo sé, no hace falta...
    item = ForeignKey(Item)
    rate = SmallIntegerField()
```

Podemos realizar una consulta sobre artículos e incorporar la puntuación
media de cada uno, calculada directamente por el gestor de la base de
datos:

```python
Item.objects.extra(select={
    'mean_rate':'''
        SELECT AVG(app_score.rate)
        FROM app_score
        WHERE app_score.item_id = app_item.id
        '''
    }).all()
```

Si quisiéramos hacerlo desde Django, con un método de la clase `Item`, por
ejemplo, tendríamos que realizar primero una consulta para obtener todas las
puntuaciones de un artículo, y luego calcular la media.

Si lo hacemos para una consulta cuyo resultado final fueran 10 artículos, por
ejemplo, se ejecutan 11 consultas SQL a la base de datos, teniendo además que
hacer el cálculo nosotros, contra una sola consulta, y los cálculos los realiza
el SGBD. La diferencia en rendimiento puede ser considerable a medida que se
incremente el número de artículos.

Estás prácticas también tienen un cierto riesgo: hemos vinculado más nuestro
código al gestor de base de datos que estamos usando, con las dependencias y
peligro que eso conlleva. Si usamos extensiones propietarias de la base de
datos para realizar la consulta, aunque sea algo tan simple como utilizar la
marca de tiempo de la base de datos (Que cada gestor se empeña en definir de
forma diferente, `sysdate` en Oracle, `now()` en postgreSQL,
`current_timestamp` en Microsoft SQL Server, por citar solo unos pocos
ejemplos), ya tenemos un punto de ruptura si pretendemos migrar de gestor.

En cualquier caso, es útil saber que tenemos esta capacidad, ya depende de
nosotros si queremos emplearla o no. Recuerda solo estos tres consejos:

- Explícito mejor que implícito (Tim Peters)

- Los casos especiales no son tan especiales como para romper las
  reglas ... pero lo práctico vence a lo ideal (Tim Peters)

- Un gran poder conlleva también una gran responsabilidad (Stan Lee)

Nota: El uso de extra para modificar las cláusulas `FROM` y `WHERE` está
explicado, junto con muchas otras cosas interesantes, en la
documentación oficial: [Django Query Set API reference - extra](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#extra).

## How to modify the queryset used in the admin forms to get a Foreign Model

You don't need to specify this in a form class, but can do it directly
in the ModelAdmin, as Django already includes this built-in method on
the ModelAdmin. From the docs:

```python
ModelAdmin.formfield_for_foreignkey(self, db_field, request, **kwargs):
'''The formfield_for_foreignkey method on a ModelAdmin allows you to
    override the default formfield for a foreign keys field. For example,
    to return a subset of objects for this foreign key field based on the
    user:'''
```

Lets see an example:

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

## How to use different forms (for update or insert) in admin

Use the `get_form` method from class `ModelAdmin`, and return the form
you need in every case; you can decide if it's an update of an existing
object or the addition of a new one looking at the `obj` parameter. If
`obj` is `None`, then is an `INSERT` on the database, else, `obj` is the
same object being modified.

Look at this example:

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

## How to make a CASE statement using the django ORM

First thing is know to use the conditional expressions. Conditional expressions
let you use `if ... elif ... else` logic within filters, annotations,
aggregations, and updates. A conditional expression **evaluates a series of
conditions for each row of a table and returns the matching result
expression**. Conditional expressions can also be combined and nested like
other expressions.

We'll be using the following model in the subsequent examples:

```python
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
```

A **When** object is used to encapsulate a condition and its result for
use in the conditional expression. Using a `When()` object is similar to
using the `filter()` method. The condition can be specified using field
lookups, `Q` objects, or Expression objects that have an `output_field`
that is a `BooleanField`. The result is provided using the `then`
keyword.

Some examples:

```python
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
```

A **Case** expression use multiples `When()` objects. Each condition in
the provided `When()` objects is evaluated in order, until one evaluates
to a truthful value. The result expression from the matching `When()`
object is returned.

An example:

```python
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
```

the `Case()` class accepts any number of `When()` objects as individual
arguments. Other options are provided using keyword arguments. If none
of the conditions evaluate to `True`, then the expression given with the
`default` keyword argument is returned. If a default argument isn't
provided, `None` is used.

Sources: 

- [Conditional expressions](https://docs.djangoproject.com/en/3.1/ref/models/conditional-expressions/)
- [Best practices working with Django models](https://steelkiwi.com/blog/best-practices-working-django-models-python/)


## Cómo enlazar a una página dentro del admin

When an AdminSite is deployed, the views provided by that site are accessible
using Django's URL reversing system.

The AdminSite provides the following named URL patterns:

| Page                      | URL name | Parameters                 |
|---------------------------|----------|----------------------------|
| Index                     | `index`  |                            |
| Login                     | `login`  |                            |
| Logout                    | `logout` |                            |
| Password change           | `password_change` |                   | 
| Password change done      | `password_change_done` |              | 
| i18n JavaScript           | `jsi18n` |                            |
| Application index page    | `app_list` | `app_label`             |
| Redirect to object's page | `view_on_site` | `content_type_id`, `object_id` |

Each ModelAdmin instance provides an additional set of named URLs:

| Page       | URL name                              | Parameters  |
|------------|---------------------------------------|-------------|
| Changelist | `<app_label>_<model_name>_changelist` |             |
| Add        | `<app_label>_<model_name>_add`        |             |
| History    | `<app_label>_<model_name>_history`    | `object_id` |
| Delete     | `<app_label>_<model_name>_delete`     | `object_id` |
| Change     | `<app_label>_<model_name>_change`     | `object_id` |

Por ejemplo, para enlazar con la página de edición (*change*) del modelo
`Libro` dentro de la app `biblioteca`, sería:

```
admin:biblioteca_libro_change
```

- Source: [Reversing admin URLs](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#reversing-admin-urls)

## Correct Model Naming

It is generally recommended to use **singular nouns** for model naming, for
example: `User`, `Post`, `Article`. That is, the last component of the name
should be a noun, e.g.: Some New Shiny Item. It is correct to use singular
numbers when one unit of a model does not contain information about several
objects.

## Relationship Field Naming

For relationships such as `ForeignKey`, `OneToOneKey`, `ManyToMany` it is
sometimes better to specify a name. Imagine there is a model called `Article`,
- in which one of the relationships is `ForeignKey` for model `User`. If this
field contains information about the author of the article, then `author` will
be a more appropriate name than user.

## Correct Related-Name

It is reasonable to indicate a related-name in plural as related-name
addressing returns queryset. Please, do set adequate related-names. In
the majority of cases, the **name of the model in plural** will be just
right. For example:

```python
class Owner(models.Model):
    pass

class Item(models.Model):
    owner = models.ForeignKey(Owner, related_name='items')
```

## Do not use ForeignKey with unique=True

There is no point in using ForeignKey with unique=Trueas there exists
`OneToOneField` for such cases.


## Attributes and Methods Order in a Model

Preferable attributes and methods order in a model (an empty string
between the points).

1)  `meta`

2)  constants (for choices and other)

3)  fields of the model

4)  custom manager indication

5)  `__unicode__` (python 2) or `__str__` (python 3)

6)  other special methods

7)  def `clean`

8)  def `save`

9)  def `get_absolut_url`

10) other methods


## Denormalisations

You should not allow thoughtless use of denormalization in relational
databases. Always try to avoid it, except for the cases when you denormalise
data consciously for whatever the reason may be (e.g.  productivity). If at the
stage of database designing you understand that you need to denormalise much of
the data, a good option could be the use of NoSQL. However, if most of data
does not require denormalisation, which cannot be avoided, think about a
relational base with JsonField to store some data.


## BooleanField

Do not use `null=True` or `blank=True` for `BooleanField`. It should
also be pointed out that it is better to specify default values for such
fields. If you realise that the field can remain empty, you need
`NullBooleanField`.


## Use of choices

While using choices, it is recommended to:

- keep strings instead of numbers in the database (although this is not the
  best option from the point of optional database use, it is more convenient in
  practise as strings are more demonstrable, which allows the use of clear
  filters with get options from the box in REST frameworks).

- Variables for variants storage are constants. That is why they must
  be indicated in uppercase.

- Indicate the variants before the fields lists.

- If it is a list of the statuses, indicate it in chronological order
  (e.g. `new`, `in_progress`, `completed`).

you can use `Choices` from the `model_utils` library. Take model
`Article`, for instance:

```python
from model_utils import Choices

class Article(models.Model):
    STATUSES = Choices(
        (0, 'draft', _('draft')),
        (1, 'published', _('published'))   )
    status = models.IntegerField(choices=STATUSES, default=STATUSES.draft)
```

## Many flags in a model?

If it is justified, replace several `BooleanFields` with one field,
status-like:

```python
class Article(models.Model):`
    is_published = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
```

Assume the logic of our application presupposes that the article is not
published and checked initially, then it is checked and marked as verified and
then it is published. You can notice that article cannot be published without
being checked. So there are 3 conditions in total, but with 2 boolean fields we
do not have **4 possible variants**, and you should make sure there are no articles
with wrong boolean fields conditions combinations (You can have wrong states).
That is why using one status field instead of two boolean fields is a better
option:

```python
class Article(models.Model):

    STATUSES = Choices('new', 'verified', 'published')

    status = models.IntegerField(choices=STATUSES, default=STATUSES.draft)
```

## Do not add redundant model name in a field name

Do not add model names to fields if there is no need to do so, e.g. if table
`User` has a field `user_status` - you should rename the field into `status`,
as long as there are no other statuses in this model.


## Dirty data should not be found in a base

Always use `PositiveIntegerField` instead of `IntegerField` if it
is not senseless, because **bad data must not go to the database**.  For the
same reason you should always use `unique` for logically unique data and never
use `required=False` in every field.


## Getting the earliest/latest object

You can use `ModelName.objects.earliest('created'/'earliest')` instead
of `order_by('created')[0]` and you can also put `get_latest_by` in Meta
model. You should keep in mind that `latest/earliest`, as well as `get`,
can cause an exception `DoesNotExist`. Therefore,
`order_by('created').first()` is the most useful variant.


## Never make len(queryset)

Do not use `len` to get queryset's objects amount. The `count` method can be
used for this purpose. Reason is: if you made `len(ModelName.objects.all())`,
firstly the query for selecting all data from the table will be carried out,
then this data will be transformed into a Python object, and the length of this
object will be found with the help of `len`.

It is highly recommended not to use this method as `count` will address to a
corresponding SQL function `COUNT()`.  With `count`, an easier query will be
carried out in that database and fewer resources will be required for python
code performance.


## Do not use `if queryset`, is a bad idea

Never use a `queryset` as a boolean value: instead of `if queryset:` do
something like `if queryset.exists():`. Remember querysets are lazy, and
if you use `queryset` as a boolean value, an inappropriate query to a
database will be carried out.


## Please use `help_text` as documentation

Using model `help_text` in fields as a part of documentation will
definitely facilitate the understanding of the data structure by you,
your colleagues, and admin users.


## Use `DecimalField` for Money Information Storage

**Never use `FloatField` to store information about a quantity of money**.
Instead, use `DecimalField` . Other common option in to keep this information
in cents, pence, etc.


## Don't use `null=true` if you don't need it

- `null=True` Allows column to keep null value.

- `blank=True` Will be used only if Forms for validation and **is not
  related to the database**.

In text-based fields, it's better to keep default value. `''`, this way
you'll get only one possible value for columns without data.


## Leer los valores pasados como parámetros en una URL

Se usa el pseudo-diccionario `GET`. Por ejemplo, si la url era
`/search/?q=haha`, entonces se puede obtener el valor con:

```python
request.GET.get('q', '')
```

## Transparent fields list

Do not use `Meta.exclude` for a model's fields list description in
`ModelForm`. It is better to use `Meta.fields` for this as it makes the
fields list transparent. Do not use `Meta.fields="__all__"` for the
same reason.


## Do not heap all files loaded by user in the same folder

Sometimes even a separate folder for each FileField will not be enough
if a large amount of downloaded files is expected. Storing many files in
one folder means the file system will search for the needed file more
slowly. To avoid such problems, you can do the following:

```python
def get_upload_path(instance, filename):
    _now = now().date().strftime("%Y/%m/%d")
    return os.path.join('account/avatars/', _now, filename)

class User(AbstractUser):
    avatar = models.ImageField(blank=True, upload_to=get_upload_path)
```

## Use custom Manager and QuerySet

The bigger project you work on, the more you repeat the same code in
different places. To keep your code DRY and allocate business logic in
models, you can use custom Managers and Queryset.

For example. If you need to get comments count for posts, from the
example above:

```python
class CustomManager(models.Manager):

    def with_comments_counter(self):
        return self.get_queryset().annotate(comments_count=Count('comment_set'))
```

Now you can use:

```python
posts = Post.objects.with_comments_counter()
posts[0].comments_count
```

You can use this in chain with others `queryset` methods:

```python
posts = Post.objects.with_comments_counter().filter()
posts[0].comments_count 
```

Source:
<https://steelkiwi.com/blog/best-practices-working-django-models-python/>

### Writing a custom storage system¶

Source:
[https://docs.djangoproject.com/en/3.2/howto/custom-file-storage/](https://docs.djangoproject.com/en/3.2/howto/custom-file-storage/)

If you need to provide custom file storage – a common example is storing files on some
remote system – you can do so by defining a custom storage class. You’ll need to follow
these steps:

Your custom storage system must be a subclass of django.core.files.storage.Storage:

from django.core.files.storage import Storage

class MyStorage(Storage):
    ...
Django must be able to instantiate your storage system without any arguments. This means that any settings should be taken from django.conf.settings:

from django.conf import settings
from django.core.files.storage import Storage

class MyStorage(Storage):
    def __init__(self, option=None):
        if not option:
            option = settings.CUSTOM_STORAGE_OPTIONS
        ...
Your storage class must implement the _open() and _save() methods, along with any other methods appropriate to your storage class. See below for more on these methods.

In addition, if your class provides local file storage, it must override the path() method.

Your storage class must be deconstructible so it can be serialized when it’s used on a field in a migration. As long as your field has arguments that are themselves serializable, you can use the django.utils.deconstruct.deconstructible class decorator for this (that’s what Django uses on FileSystemStorage).

By default, the following methods raise NotImplementedError and will typically have to be overridden:

Storage.delete()
Storage.exists()
Storage.listdir()
Storage.size()
Storage.url()
Note however that not all these methods are required and may be deliberately omitted. As it happens, it is possible to leave each method unimplemented and still have a working Storage.

By way of example, if listing the contents of certain storage backends turns out to be expensive, you might decide not to implement Storage.listdir().

Another example would be a backend that only handles writing to files. In this case, you would not need to implement any of the above methods.

Ultimately, which of these methods are implemented is up to you. Leaving some methods unimplemented will result in a partial (possibly broken) interface.

You’ll also usually want to use hooks specifically designed for custom storage objects. These are:

_open(name, mode='rb')¶
Required.

Called by Storage.open(), this is the actual mechanism the storage class uses to open the file. This must return a File object, though in most cases, you’ll want to return some subclass here that implements logic specific to the backend storage system.

_save(name, content)¶
Called by Storage.save(). The name will already have gone through get_valid_name() and get_available_name(), and the content will be a File object itself.

Should return the actual name of name of the file saved (usually the name passed in, but if the storage needs to change the file name return the new name instead).

get_valid_name(name)¶
Returns a filename suitable for use with the underlying storage system. The name argument passed to this method is either the original filename sent to the server or, if upload_to is a callable, the filename returned by that method after any path information is removed. Override this to customize how non-standard characters are converted to safe filenames.

The code provided on Storage retains only alpha-numeric characters, periods and underscores from the original filename, removing everything else.

get_alternative_name(file_root, file_ext)¶
Returns an alternative filename based on the file_root and file_ext parameters. By default, an underscore plus a random 7 character alphanumeric string is appended to the filename before the extension.

get_available_name(name, max_length=None)¶
Returns a filename that is available in the storage mechanism, possibly taking the provided filename into account. The name argument passed to this method will have already cleaned to a filename valid for the storage system, according to the get_valid_name() method described above.

The length of the filename will not exceed max_length, if provided. If a free unique filename cannot be found, a SuspiciousFileOperation exception is raised.

If a file with name already exists, get_alternative_name() is called to obtain an alternative name.

## Como hacer migraciones propias

Crteamos una migracion vacia (_empty_):

```shell
./manage.py makemigrations --empty --name nombre_que_quieras_para_la_migracion <app>
```

Esto creara un fichero de migración vacio, con un contenido similar a este:

```python
# Generated by Django 3.2.12 on 2022-03-22 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0003_asunto_bop_cargo_claseiniciativa_composicion_diputado_diputadogrupo_ds_dsc_dsdp_fotodiputado_grupopa'),
    ]

    operations = [
    ]
```

Como vemos, solo se define el campo de dependencias, las operaciones a realizar
en esta migracion estam vacias. Vamos a incluir codigo SQL para crear la
sequencia:

```sql
CREATE SEQUENCE Agora.seq_foto_diputado START WITH 1 INCREMENT BY 1;
```

Para ello haremos uso de la clase [migration.RunSQL](https://docs.djangoproject.com/en/1.10/ref/migration-operations/#runsql), que nos permite definir la migración tante en una dirección como en otra, es decir, crearemos
este objeto con dos sentencias SQL, una para definir como aplicar la migración, y otra para desacerla. En nuestro caso, quedaria asi:

```python
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


## Como condensar /simplificar (_squash_) las migraciones en Django

Existe una opción en el `manage.py` llamada `squashmigrations` que nos
permite condensar todas las migraciones aplicadas (o un subconjunto de ellas)
de forma que se sustituyan por una única migración. Además, intenta optimizar
las migraciones al mezclarlas, de forma que se eliminan los cambios que son
sobrescritos por migraciones posteriores.

Por ejemplo, si tenemos una accion de tipo `CreateModel()` y más tarde aparece
otra de tipo `DeleteModel()` para el mismo modelo, se pueden eliminar no solo
las dos acciones indicadas, sino también cualquier acción intermedia que
modificar al modelo.

Igualmente, acciones como `AlterField()` o `AddField()` son transladadas a la
versión final de la acción `CreateModel`.

La versión final condensada también mantiene referencias al conjuto de
migraciones que reemplaza. De esa forma Django puede saber si tiene que
mirgaciones tiene que usar para entender cosas como el histórico de grabaciones
o las dependencias entre migraciones.

Django enumera de forma automática los ficheros de migraciones, partiendo de
`0001_initial.py`. De esa forma puede determinar el orden de aplicación de las
migraciones, y nosotros podemos usarlo para indicar el conjunto de las
migraciones que queremos condensar, en forma de rango.

Por ejemplo, supongamos que tenemos la siguiente lista de migraciones:

```
./foo
    ./migrations
        0001_initial.py
        0002_userprofile.py
        0003_article_user.py
        0004_auto_20190101_0123.py
```

En la mayoría de los casos estarémos interesados en condensarlas todas en un
único fichero. Para ello, ejecutamos la siguiente orden:

```shell
python manage.py squashmigrations foo 0004
```

El resultado será condensar todas las migraciones, desde la 1 hasta la 4,
generando una nueva migración con el nombre:
`0001_squashed_0004_auto_<timestamp>.py`

Si examinamos este fichero, descubriremos dos cosas interesantes:

- La nueva migración está marcada como `initial=True`, lo que significa que
  sera la nueva migración inicial de esta aplicación. Si se aplicara en una
  nueva base de datos, las migraciones anteriores se ignorarían.

- Se ha añadido un nuevo atributo, `replaces`, que es una lista de las
  migraciones que son reemplazadas por esta.

Fuentes:

 - [How to Squash and Merge Django Migrations &middot; Coderbook](https://coderbook.com/@marcus/how-to-squash-and-merge-django-migrations/)

