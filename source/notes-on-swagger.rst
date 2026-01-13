Swagger
========================================================================


Sobre swagger
------------------------------------------------------------------------

Current version: 3.02

Definitions
------------------------------------------------------------------------

**Path Templating**: refers to the usage of curly braces ({}) to mark a
section of a URL path as replaceable using path parameters.

Format
------------------------------------------------------------------------

An OpenAPI document that conforms to the OpenAPI Specification is itself
a JSON object, which may be represented either in JSON or YAML format.
For example, if a field has an array value, the JSON array
representation will be used:

.. code:: json

    {
        "field": [ 1, 2, 3 ]
    }

In order to preserve the ability to round-trip between YAML and JSON
formats, YAML version 1.2 is RECOMMENDED along with some additional
constraints:

- Tags **must be limited to those allowed by the JSON Schema** ruleset.

- Keys used in YAML maps **must be limited to a scalar string**, as
  defined by the YAML Failsafe schema ruleset.
