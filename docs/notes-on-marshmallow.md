---
title: Notas sobre marshmallow
---

## Sobre marshmallow

marshmallow is an ORM/ODM/framework-agnostic library for converting complex
datatypes, such as objects, to and from native Python datatypes.

Lets see an example:

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

## Create a Schema

Let’s start with a basic user model:

```python
import datetime

class User:

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return f"User(name={self.name!r}, email={self.email!r})")
```

Create a schema by defining a class with variables mapping attribute names to Field objects:

```python
from marshmallow import Schema, fields

class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()
```

Note: You can create a schema from a dictionary of fields using the `from_dict` method.
