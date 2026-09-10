CAS (*Central Authentication Service*)
========================================================================

.. tags:: web, seguridad, sso


Qué es CAS
------------------------------------------------------------------------

**CAS** es un protocolo de *SSO* (*Single Sign-On*) pensado para la web.
Su propósito es permitir a un usuario acceder a múltiples aplicaciones
teniendo que acreditarse (Como por ejemplo, con su usuario y contraseña)
una única vez. También permite que las aplicaciones web puedan
autenticar al usuario sin tener nunca acceso a su contraseña o
acreditación equivalente.

Qué se entiende por *Single Sign-On*
------------------------------------------------------------------------

El **SSO** (*Single Sign-On*), **inicio de sesión único** o **inicio de
sesión unificado** es un procedimiento de autenticación que habilita a
un usuario determinado para acceder a varios sistemas con una sola
instancia de identificación.

Fuentes:

- `Single Sign-on en Wikipedia`_

- `How does single sign-on work`_


Diferencias entre ``OAuth``, ``OIDC``, ``SAML`` y ``SSO``
------------------------------------------------------------------------

OAuth no autentica; autoriza. Muchas veces usamos un sistema de permisos
para verificar la identidad y nos preguntábamos por qué nuestro sistema
de autenticación tenía lagunas.

La confusión: a menudo se trata a ``OAuth``, ``OIDC``, ``SAML`` y
``SSO`` como cuatro nombres para lo mismo, pero no lo son. Dos gestionan
la **autenticación** (quién eres). Uno gestiona la **autorización** (a
qué puedes acceder). Y uno de ellos **ni siquiera es un protocolo**.

- ``OAuth``: Gestión de permisos, sin identidad. "¿Puede esta aplicación
  acceder a mi *Google Drive*?". Eso es ``OAuth``. Otorga un *token* que
  indica qué acciones tienes permitidas; nunca confirma quién eres.

- ``OIDC``: Identidad construida sobre ``OAuth``. Es la pieza que le
  faltaba a ``OAuth``. Devuelve un *token* de identidad (:term':`JWT`) que
  realmente indica quién es el usuario: nombre, correo electrónico,
  roles. ``OIDC`` existe porque todo el mundo usaba ``OAuth``
  incorrectamente para la autenticación. En lugar de luchar contra el
  uso indebido, la industria creó una solución adecuada sobre él. Si tu
  aplicación necesita saber quién es alguien Y a qué puede acceder,
  ``OIDC`` te proporciona ambas cosas.

- ``SAML``: Para empresas y sistemas heredados (*legacy*). Sigue
  funcionando en la mayoría de las grandes organizaciones. Cuando
  inicias sesión en las herramientas internas de tu empresa a través de
  Okta o ADFS, probablemente haya ``SAML`` de fondo. Realiza la misma
  función que ``OIDC`` —demostrar la identidad—, pero utilizando
  aserciones XML en lugar de tokens JSON. No es tan amigable para los
  desarrolladores.

• ``SSO``: No es un protocolo, sino una **experiencia**. Inicias sesión
una vez y accedes a múltiples aplicaciones sin tener que volver a
autenticarte. El ``SSO`` es el resultado; ``OIDC``, ``SAML`` (o ambos) son los
mecanismos que lo hacen posible.

La decisión en la práctica:

- Necesitas saber a qué puede acceder un usuario: ``OAuth`` 2.0.

- Necesitas saber quién es un usuario (aplicación moderna): ``OIDC``.

- Necesitas saber quién es un usuario (entorno empresarial o sistemas
  heredados): ``SAML``.

- Necesitas un único inicio de sesión para varias aplicaciones: ``SSO``,
  impulsado por ``OIDC`` o ``SAML``.

- Necesitas identidad Y autorización: ``OIDC`` (que incluye ``OAuth`` en
  su base).



Cómo funciona CAS
------------------------------------------------------------------------

El protocolo de CAS implica a, al menos, tras participantes: El
navegador web, la aplicación web en la que se quiere identificar el
usuario, y el servidor CAS. Puede –y es muy probable que así sea– que el
servidor CAS use otros componentes, como una base de datos, con los que
se comunicará probablemente usando canales de comunicación privados.

Cuando el cliente accede a la aplicación, y necesita identificarse, la
aplicación le redirige hacia el CAS. Este valida la identidad del
usuario, normalmente validando su combinación de usuario y contraseña
contra una base de datos como Kerberos, LDAP o un directorio activo.

Si el proceso de identificación tiene éxito, CAS retorna el cliente a la
aplicación, junto con un **ticket de servicio** (*service ticket*). La
aplicación debe ahora validar el *ticket* conectado con el CAS, usando
una conexión segura, y proporcionando su propio identificador de la
aplicación junto con el ticket. CAS entonces proporciona a la aplicación
informaciøn adicional y confiable acerca del usuario en particular, que
de esta manera ya se ha identificado correctamente.

Librerías para usar CAS
------------------------------------------------------------------------

En Django tenemos:

-  **Cliente Django CAS**: `django-cas-ng <https://djangocas.dev/>`__

**Django-CAS-NG** es un cliente CAS 1.0/2.0/3.0 que permite usar SSO
(*Single Sign On*) y *Single Sign Out*.

Repo: https://github.com/django-cas-ng

-  **Django CAS Server**:
`django-mama-cas <https://github.com/jbittel/django-mama-cas>`__

**Django-MamaCAS** es un servidor Django CAS. Implementa los
protocolos CAS 1.0, 2.0 y 3.0, incluyendo ciertas funcionalidades
adicionales.

Repo: https://github.com/jbittel/django-mama-cas

Las versiones de CAS
------------------------------------------------------------------------

CAS 1.0 es un protocolo en texto plano que devuelve un simple "yes" o
"no", para indicar si un *ticket* de validación es correcto o no.

CAS 2.0 devuelve fragmentos XML para la validación de las respuestas y
permite el uso de *proxy*.

La versión 3.0 expande el protocolo con nuevos parámetros y la respuesta
ahora viene en formato
`SAML <https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language>`__.

Qué es el formato SAML
------------------------------------------------------------------------

**SAML** es un estándar abierto que define un esquema XML para el
intercambio de datos de autenticación y autorización. Es utilizado como
elemento clave en sistemas centralizados de autenticación y
autorización(*Single Sign-On*).

Usualmente las partes que intervienen en el intercambio son un proveedor
de identidad (entidad que dispone de la infraestructura necesaria para
la autenticación de los usuarios) y un proveedor de servicio (entidad
que concede a un usuario el acceso o no a un recurso).

Notas sobre la especificación del protocolo CAS 3.0
------------------------------------------------------------------------

CAS es un protocolo que funciona sobre HTTP, y que requiere que sus
componentes sean accesibles a través de unas URL específicas:

======================= =========================================
URI                     Descripción
======================= =========================================
``/login``              credential requestor / acceptor
``/logout``             destroy CAS session (logout)
``/validate``           service ticket validation
``/serviceValidate``    service ticket validation [CAS 2.0]
``/proxyValidate``      service/proxy ticket validation [CAS 2.0]
``/proxy``              proxy ticket service [CAS 2.0]
``/p3/serviceValidate`` service ticket validation [CAS 3.0]
``/p3/proxyValidate``   service/proxy ticket validation [CAS 3.0]
======================= =========================================

La URI /login
------------------------------------------------------------------------

La URI ``/login`` realiza **dos papeles diferentes**: Es la URI que se
usa para solicitar una credencial, y también actúa como receptor de
dicha credencial. Dependiendo de si se le añade la credencial, actual en
un papel u otro.

Si el cliente ya ha establecido una sesión de identificación con CAS, el
navegador web enviará una *cookie* segura, que contendrá el
identificador del *ticket* autorizado (*ticket-granting*) que obtuvo en
dicha sesión. Esta *cookie* se conoce como *ticket-granting cookie*. Si
el identificador se refiere a un *ticket* válido, CAS puede suministrar
un *ticket de servicio*.

Los parámetros que se pueden pasar ``/login``, cuando actúa como un
solicitante de identificación son:

- ``service`` [OPCIONAL] - Es el identificador de la aplicación a la que
  el cliente está intentando acceder. Casi siempre consistirá en una URL
  a la aplicación. Debe estar codificada como cualquier otro parámetro
  HTTP, tal y como se describe en la sección 2.2 del `RFC 3986
  <https://www.rfc-editor.org/info/rfc3986>`_.

  Si no se especifica el servicio, y no **existe** una sesión previa,
  CAS **debe** iniciar el proceso para iniciar una sesión de
  identificación. Si no se especifica el servicio, pero existe una
  sesión prevía, CAS **debería** mostrar un mensaje al cliente
  informándole de que ya se ha identificado.

.. note::

    Se **recomienda encarecidamente** que todas las URL de los
    servicios estén previamente registradas, de forma que solo se
    autorizan estas.

- ``method`` [OPCIONAL, CAS 3.0] - El método que se debe usar para
  enviar datos. Aunque el método por defecto es utilizar el verbo
  ``GET``, las aplicaciones que prefieran recibir los datos vía ``POST``
  pueden usar este parámetro para indicar dicha preferencia. A pesar de
  eso, el CAS puede determinar si se soportan las peticiones ``POST``

Otros parámetros no comentados aquí:

    The method to be used when sending
    responses. While native HTTP redirects (GET) may be utilized as the
    default method, applications that require a POST response can use this
    parameter to indicate the method type. It is up to the CAS server
    implementation to determine whether or not POST responses are
    supported.
    
    2.1.2. URL examples of /login Simple login example:
    
Fuente: https://cas.example.org/cas/login?service=http%3A%2F%2Fwww.example.org%2Fservice

.. _Single Sign-on en Wikipedia: https://es.wikipedia.org/wiki/Single_Sign-On
.. _How does single sign-on work: https://www.onelogin.com/learn/how-single-sign-on-works
