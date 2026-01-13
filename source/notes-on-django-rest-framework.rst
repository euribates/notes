Django Rest Framework
========================================================================


Serializares
-----------------------------------------------------------------------

Una clase ``serializer`` es muy similar a una clase formulario de Django,
e incluye reglas de validación similares para los diferentes campos, como
``required``, ``max_length`` o ``default``.

El cuerpo de la clase define los campos pertinentes, mientras que los
métodos ``create()`` y ``update()`` determinan de que manera se crean o
actualizan las instancias correspondientes, cuando se llama al método
``save()``.

El propósito es tener una forma centralizada de convertir instancias en
versiones serializadas en JSON, y viceversa:

.. code::

    Model instance -> Serializer -> Dict json-ready -> JSONRenderer -> json

    json -> JSONParser -> Dict -> Serializer -> Model Instance

Además de instancias, también permite serializar *querysets*. Para ello
solo hay que añadir el parámetro ``many=True`` el crear el *serializar*:

.. code:: python

    serializer = SnippetSerializer(Snippet.objects.all(), many=True)


Cómo usar ModelSerializers
-----------------------------------------------------------------------

Igual que Djnago incorpora clases Formularios base y Formularios basados en
objetos, *REST Framework* también define dos tipos de serializadores con
la misma idea, ``Serializer`` y ``ModelSerializer``.

La clase ``ModelSerializer`` no hace nada especialmente mágico, solo es
una forma simplificada de crear un serializador.

- Determina de forma automática los campos
- Incluye una implementación por defecto de los métodos ``create()`` y ``update()``.


Objetos tipo *Request*
-----------------------------------------------------------------------

Django Rest Framework incluye una clase ``Request`` que extiende la clase
``HttpRequest``, que es la usada normalmente en Django. El componente
principal de esta clase es el atributo ``data``, que es similar al
atributo ``request.POST``, pero más orientado al uso para APIs.

- ``request.POST``: Solo funciona con datos de formularios, enviado con
  ``POST``.

- ``request.data``: maneja datos arbitrarios. Funciona con los verbos
  ``POST``, ``PUT`` y ``PATCH``.

Cómo cambiar el nombre de un campo en Django Rest Framework
-----------------------------------------------------------------------

Al definir el campo, podemos usar el parámetro ``source`` para especificar
la fuente desde la que se obtiene el dato.
Por ejemplo, si el campo es de tipo texto, usaríamos un ``serializers.CharField``
con el parámetro ``source``:

.. code:: python

    class ParkSerializer(serializers.ModelSerializer):
        location = serializers.CharField(source='alternate_name')

Si lo que queremos es incluir es el reseultado de un método, usaremos
``SerializerMethodField``, en este caso especificando el parámetro
``method_name``. Si lo preferimos, podemos dejar este valor sin declarar,
definiendo un método en la clase ``Serializar`` que se llame igual que el
campo, pero con el prefijo ``get_`` (Ver la signatura de la función en el
siguiente párrafo). El campo resultante será de solo lectura. Obtiene sus
valores llamando al método indicado de la clase ``Serializar``.

.. code:: python

    class ParkSerializer(serializers.ModelSerializer):
        signature: serializers.SerializerMethodField(method_name=None)

        def get_signature(self):
            '''Obtener la signatura.
            '''
            ...

Si queremos especificar el nombre del método:

.. code:: python

    class ParkSerializer(serializers.ModelSerializer):
        signature: serializers.SerializerMethodField(
            method_name='calculate_signature'
            )

        def calculate_signature(self):
            '''Obtener la signatura.
            '''
            ...


El parámetro ``method_name`` de ``SerializerMethodField`` permite por
tanto especificar el nombre del método del serializador que se usará para
obtener el dato. Si no se especifica, el valor por defecto que se tomara
es `get_<field_name>`.

Vamos un ejemplo:

.. code:: python

    from django.contrib.auth.models import User
    from django.utils.timezone import now
    from rest_framework import serializers

    class UserSerializer(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = '__all__'
        
        days_since_joined = serializers.SerializerMethodField()


    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days
