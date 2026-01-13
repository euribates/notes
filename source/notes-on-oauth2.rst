OAuth2
========================================================================

Qué es :index:`OAuth`
-----------------------------------------------------------------------

**OAuth** es una especificación que permite a los usuarios delegar el
acceso a sus datos sin tener que compartir ni el *username* ni las
contraseñas.

Por ejemplo, supongamos que una aplicación quiere acceder a los datos de
la cuenta de twetter de un usuario. La forma más fácil sería darle a la
aplicación acceso total con el identificador del usuario y su contraseña,
pero es una muy mala idea por una serie de razones:

1) El usuario debe confiar **muchisimo** en la aplicación para conceder
este tipo de acceso.

2) Si el usuario cambia de contraseña, todo el sistema se rompe, hay que
preguntarsela de nuevo al usuario.

3) No hay ajuste fino de seguridad, la aplicación podrá hacer todo lo que el
usuario puede hacer. Es un enfoque de todo o nada.

Evidentemente, cada empresa tenia su propio sistema de delegacin de
acceso, OAuth intenta ser el estándar.

OAuth Versión 1
-----------------------------------------------------------------------

Con esta idea se crea OAuth1. Esta primera versin ya proporcionaba una
serie de beneficios importantes:

- Una implementación más sencilla y con una curva de aprendizaje más
  suave. Además, solo tenias que aprendértela una vez, y luego usarla en
  varios servicios.

- Más segura, ya que es un estándar público y avalado por la comunidad.

- Como el protocolo ya se ha fijado, ya se pueden **hacer libreras**.


OAuth Version 2
-----------------------------------------------------------------------

La versión 2 no es demasiado diferente de la 1, hay muchos cambios menores
pero hay dos cambios que
que merece la pena destacar.

- OAuth 1 estaba diseñada para aplicaciones de tipo cliente-servidor
  típicas de la web, pero prensentaba ciertos problemas con aplicaciones
  como páginas web de página única (*Single page*), dispositos :ref:`IoT`.
  OAuth 2 intenta ser más flexible para estos escenarios. Incorpora el
  concepto de *perfiles de cliente*.

- OAuth 1 requiere *tokens* firmados, en OAuth2 podemos usar *tokens*
  sin firmar.
