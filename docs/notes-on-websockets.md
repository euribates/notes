---
title: Notas sobre websockets
tags:
    - web
    - async
    - django
    - vue.js
---

## Notas sobre websockets

**Websockets** es un protocolo de comunicaciones como HTTP, pero con la
direrencia de ser _full_duplex_, lo que permite comunicaciones bidireccionales
entre el servidor y el navegador web. Se usa en su mayoría para aplicaciones de
chat, juegos y aplicaciones de IoT. LA funcionalidad más usada es notificar al
front-end cuando se ha producido un cambio en el backend.

Antes de _websockets_, los clientes web usaban una tecnica llamada _[pooling](https://es.wikipedia.org/wiki/Polling)_,
que consiste en realizar llamadas periodícas para interrogar el estado del
servidor. Esto resulta muy ineficiente, ya que muchas de las llamadas son
superfluas, al no haber cambios en el servidor.

## Websockets con Django

Desde la version 2.0 de [Django](notes-on-django.md)  se dispone de soporte
asíncrono y de _websockets_, usando la funcionalidad de
[django-channels](https://channels.readthedocs.io/en/latest/). Esto abre las
posibilidaders de trabajar no solo con _websockets_, también con otros
protocolos que impliquen conexiones de larga duración como MQTT, por ejemplo.




