Websockets
========================================================================

.. tags:: development, html, django, python


Notas sobre :index:`websockets`
-----------------------------------------------------------------------

**Websockets** es un protocolo de comunicaciones como HTTP, pero con la
direrencia de ser *full_duplex*, lo que permite comunicaciones
bidireccionales entre el servidor y el navegador web. Se usa en su
mayoría para aplicaciones de *chat*, juegos y aplicaciones de IoT. LA
funcionalidad más usada es notificar al *front-end* cuando se ha
producido un cambio en el *back-end*.

Antes de *websockets*, los clientes web usaban una técnica llamada
`pooling <https://es.wikipedia.org/wiki/Polling>`__, que consiste en
realizar llamadas periódicas para interrogar el estado del servidor.
Esto resulta ineficiente, ya que muchas de las llamadas son superfluas,
al no haber cambios en el servidor.

Websockets con Django
----------------------------------------------------------------------

Desde la version 2.0 de :doc:`notes-on-django` se dispone de soporte
asíncrono y de *websockets*, usando la funcionalidad de
`django-channels`_. Esto abre la posibilidad de trabajar no solo con
*websockets*, también con otros protocolos que impliquen conexiones de
larga duración como MQTT, por ejemplo.

.. _django-channels: https://channels.readthedocs.io/en/latest/
