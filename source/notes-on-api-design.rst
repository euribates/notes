Diseño de API
========================================================================


Invariantes
------------------------------------------------------------------------

Some invariantes we must be confident we will find in all the API
answers:

-  All responses consists in one dictionary

-  All responses includes one key ``timestamp`` whit the date and time
of the response (Useful for traceability and debugging) as determined
by the server, in UTC. As JSON don’t have a format for dates neither
datetimes, I suggest to use a string in ISO 8601. Like:
``2018-11-03T14:30:07Z``

-  All responses includes one key ``status``

-  If status is equal to ‘ok’, then:

-  The key ``result`` is also include in the dictionary

-  This is the real response of the API and can be any type of
json-serializable object

-  If status is equal to ‘error’, then:

-  The key ``result`` **IS NOT** included in the dictionary

-  The key ``message`` is included in the dictionary. It contains
a string with a plain english description of the problem.
