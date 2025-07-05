---
title: Notas sobre Django REST Framework
---


## Serializares

A serializer class is very similar to a Django Form class, and includes
similar validation flags on the various fields, such as `required`,
`max_length` and `default`.

The first part of the serializer class defines the fields that get
serialized/deserialized. The create() and update() methods define how
fully fledged instances are created or modified when calling
serializer.save()

```
Model instance -> Serializer -> Dict json-ready -> JSONRenderer ->
json

json -> JSONParser -> Dict -> Serializer -> Model Instance
```

Notice how similar the API is to working with forms.


We can also serialize querysets instead of model instances. To do so we
simply add a many=True flag to the serializer arguments:

```python
    serializer = SnippetSerializer(Snippet.objects.all(), many=True)
    serializer.data
    # [OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
```

## Using ModelSerializers

In the same way that Django provides both Form classes and ModelForm
classes, REST framework includes both Serializer classes, and
ModelSerializer classes.

ModelSerializer classes don\'t do anything particularly magical, they
are simply a shortcut for creating serializer classes:

- An automatically determined set of fields.
- Simple default implementations for the create() and update()
    methods.


## Request objects

REST framework introduces a `Request` object that extends the regular
`HttpRequest`, and provides more flexible request parsing. The core
functionality of the Request object is the `data` attribute, which is
similar to `request.POST`, but more useful for working with Web APIs.

- `request.POST`: Only handles form data. Only works for \'POST\'
    method.
- `request.data`: Handles arbitrary data. Works for \'POST\', \'PUT\'
    and \'PATCH\' methods.


## Cómo cambiar el nombre de un campo en Django Rest Framework

Usando un _serializer`, podemos usar `source` donde podemos especificar la
fuente de la cual se obtiene campo en concreto. Por ejemplo, si el campo es de
tipo texto, usaríamos un `serializers.CharField` con el parámetro `source`:

```python
class ParkSerializer(serializers.ModelSerializer):
    location = serializers.CharField(source='alternate_name')
```

Si lo que queremos incluir es el resultado de un método, usaremos
`SerializerMethodField`, en este caso especificando el parámetro `method_name`.
Si lo preferimos, podemos dejar este valor sin declarar, definiendo un método en
la clase serializar que se llame igual que el campo, pero con el prefijo `get_`
(Ver la signatura de la función en el siguiente párrafo). El campo resultante
será de solo lectura. Obtiene sus valores llamando al método indicado de la
clase Serializar. 

```python
Signature: SerializerMethodField(method_name=None)

    method_name - El nombre del método del serializador que usará para
                  obtener el dato. Si no se especifica, el valor por defecto
                  que se tomara es `get_<field_name>`.
```

Vamos un ejemplo:

```
from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days
```

