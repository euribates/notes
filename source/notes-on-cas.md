---
title: Notas sobre CAS (Central Authentication Service)
tags:
    - web
    - seguridad
    - sso
---

## Notas sobre CAS  (Central Authentication Service)

### ¿Qué es CAS?

**CAS** es un protocolo de _SSO_ (_Single Sign-On_) pensado para la web.
Su propósito es permitir a un usuario acceder a múltiples aplicaciones
teniendo que acreditarse (Como por ejemplo, con su usuario y contraseña)
una única vez. También permite que las aplicaciones web puedan
autenticar al usuario sin tener nunca acceso a su contraseña o
acreditación equivalente.

### ¿Qué se entiende por _Single Sign-On_?

El **SSO** (_Single Sign-On_), **inicio de sesión único** o **inicio de sesión
unificado** es un procedimiento de autenticación que habilita a un usuario
determinado para acceder a varios sistemas con una sola instancia de
identificación.

- [_Single Sign-on_ en Wikipedia](https://es.wikipedia.org/wiki/Single_Sign-On)
- [_How does single sign-on work?_](https://www.onelogin.com/learn/how-single-sign-on-works)


### ¿Cómo funciona CAS?

El protocolo de CAS implica a, al menos, tras participantes: El
navegador web, la aplicación web en la que se quiere identificar el
usuario, y el servidor CAS. Puede --y es muy probable que así sea-- que
el servidor CAS use otros componentes, como una base de datos, con los
que se comunicará probablemente usando canales de comunicación privados.

Cuando el cliente accede a la aplicación, y necesita identificarse, la
aplicación le redirige hacia el CAS. Este valida la identidad del
usuario, normalmente validando su combinación de usuario y contraseña
contra una base de datos como Kerberos, LDAP o un directorio activo.

Si el proceso de identificación tiene éxito, CAS retorna el cliente a la
aplicación, junto con un **ticket de servicio** (_service ticket_). La
aplicación debe ahora validar el ticket conectado con el CAS, usando una
conexión segura, y proporcionando su propio identificador de la
aplicación junto con el ticket. CAS entonces proporciona a la aplicación
informaciøn adicional y confiable acerca del usuario en particular, que
de esta manera ya se ha identificado correctamente.


### Librerías para usar CAS

En Django tenemos:

- **Cliente Django CAS**: [django-cas-ng](https://djangocas.dev/)
  
  **Django-CAS-NG** es un cliente CAS 1.0/2.0/3.0 que permite usar SSO (_Single
  Sign On_) y _Single Sign Out_. 

  Repo: [https://github.com/django-cas-ng](https://github.com/django-cas-ng)

- **Django CAS Server**: [django-mama-cas](https://github.com/jbittel/django-mama-cas)

  **Django-MamaCAS** es un servidor Django CAS. Implementa los protocolos CAS
  1.0, 2.0 y 3.0, incluyendo ciertas funcionalidades adicionales.

  Repo: [https://github.com/jbittel/django-mama-cas](https://github.com/jbittel/django-mama-cas)

### Notas sobre la especificación del protocolo CAS 3.0

CAS es un protocolo que funciona sobre HTTP, y que requiere que sus
componentes sean accesibles a través de unas URL específicas:

| URI                   | Descripción                               |
|-----------------------|-------------------------------------------|
| `/login`              | credential requestor / acceptor           |
| `/logout`             | destroy CAS session (logout)              |
| `/validate`           | service ticket validation                 |
| `/serviceValidate`    | service ticket validation [CAS 2.0]       |
| `/proxyValidate`      | service/proxy ticket validation [CAS 2.0] |
| `/proxy`              | proxy ticket service [CAS 2.0]            |
| `/p3/serviceValidate` | service ticket validation [CAS 3.0]       |
| `/p3/proxyValidate`   | service/proxy ticket validation [CAS 3.0] |


### La URI /login

La URI `/login` realiza dos papeles diferentes: Es la URI que se usa
para solicitar una credencial, y también actua como un receptor de dicha
credencial. Dependiendo de si se le añade la credencial, actual en uno
papel u otro.

Si el cliente ya ha establecido una sesión de indetificación con CAS, el
navegador web enviará una _cookie_ segura, que contendrá el
identificador del _ticket_ autorizador (_ticket-granting_) que obtuvo
en dicha sesión. Esta _cookie_ se conoce como _ticket-granting cookie_.
Si el identificador se refiere a un ticket válido, CAS puede suministrar
un *ticket de servicio**.

Los parámetros que se pueden pasar `/login`, cuando actúa como un
solicitante de identificación son:

- `service` [OPCIONAL] - Es el identificador de la aplicación a la que el
  cliente está intentando acceder. Casi siempre consistirá en una URL a
  la aplicación. Debe estar codificada como cualquier otro parámetro
  HTTP, tal y como se describe en la sección 2.2 del
  [RFC 3986](https://www.rfc-editor.org/info/rfc3986).

  Si no se especifica el servicio, y no **existe** una sesión previa,
  CAS **debe** iniciar el proceso para iniciar una sesión de
  identificación. Si no se especifica el servicio, pero existe una
  sesión prevía, CADA **debería** mostrar un mensaje al cliente
  informándole de que ya se ha identificado.

  Nota: Se **recomienda encarecidamente** que todas las URL de los servicios
  estén previamente registradas, de forma que solo se autorizan estas.

- `method` [OPCIONAL, CAS 3.0] - El método que se debe usar
  para enviar datos. Aunque el método por defecto es utilizar
  el verbo `GET`, las aplicaciones que prefieran recibir los
  datos vía `POST` pueden usar este parámetro para indicar
  dicha preferencia. A pesar de eso, el CAS puede determinar si
  se soportan las peticiones `POST`


Otros paræmetros no comentados aquí: 
  The method to be used when sending
  responses. While native HTTP redirects (GET) may be utilized as the
  default method, applications that require a POST response can use this
  parameter to indicate the method type. It is up to the CAS server
  implementation to determine whether or not POST responses are
  supported.


2.1.2. URL examples of /login
Simple login example:

https://cas.example.org/cas/login?service=http%3A%2F%2Fwww.example.org%2Fservice
