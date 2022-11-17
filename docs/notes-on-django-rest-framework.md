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
