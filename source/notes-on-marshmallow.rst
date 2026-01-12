marshmallow
========================================================================

.. tags: python

Sobre marshmallow
-----------------------------------------------------------------------

**Marshmallow** es una libraría para convertir tipos de datos complejos,
como o objetos, desde y hacia variables Pyton nativas.

Documentación: https://marshmallow.readthedocs.io/en/latest/

Veamos un ejemplo:

.. code:: python

    import datetime

    from marshmallow import Schema, fields

    class ArtistSchema(Schema):
        name = fields.Str()

    class AlbumSchema(Schema):
        title = fields.Str()
        release_date = fields.Date()
        artist = fields.Nested(ArtistSchema())

    bowie = dict(name="David Bowie")
    album = dict(
        artist=bowie,
        title="Hunky Dory",
        release_date=datetime.date(1971, 12, 17),
        )

    schema = AlbumSchema()
    result = schema.dump(album)
    print(result)


Crear un esquema (*Schema*)
-----------------------------------------------------------------------

Supongamos un modelo básico de usuario:

.. code:: python

    import datetime

    class User:

        def __init__(self, name, email):
            self.name = name
            self.email = email
            self.created_at = datetime.datetime.now()

        def __repr__(self):
            return f"User(name={self.name!r}, email={self.email!r})")

Creamos un esquema definiendo una clase con variables que mapean los
nombres de los atributos a objetos de tipo ```Field``:

.. code:: python

    from marshmallow import Schema, fields

    class UserSchema(Schema):
        name = fields.Str()
        email = fields.Email()
        created_at = fields.DateTime()


.. note:: Tamnbién se puede crear un squema a parti de un diccionario
   usando el método ``from_dict``.
