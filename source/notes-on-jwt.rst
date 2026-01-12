JWT (*JSON Web Token*)
========================================================================


Sobre :index:`JWT` (*JSON Web Token*)
-----------------------------------------------------------------------

Un **token** es un dato que no tiene significado ni utilidad por sí
solo, pero que, combinado con el sistema de tokenización adecuado, se
convierte en un elemento vital para la seguridad de su aplicación.

La autenticación basada en tokens funciona garantizando que cada
solicitud a un servidor vaya acompañada de un token firmado, cuya
autenticidad verifica el servidor y solo entonces responde a la
solicitud.

*JSON Web Token* (JWT) es un estándar abierto (`RFC 7519`_) que define
un método compacto y autónomo para la transmisión segura de información
entre partes, codificada como un objeto JSON. JWT ha ganado gran
popularidad gracias a su tamaño compacto, que permite la fácil
transmisión de tokens mediante cadenas de consulta, atributos de
encabezado y dentro del cuerpo de una solicitud POST.


.. _RFC 7519: https://www.rfc-editor.org/info/rfc7519
