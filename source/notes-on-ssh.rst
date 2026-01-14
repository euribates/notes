SSH (*Secure Shell*)
========================================================================

.. tags:: unix,python,seguridad,devops


Sobre SSH
------------------------------------------------------------------------

**SSH** (*Secure SHell*) es un protocolo y programa cuya principal
función es el acceso remoto a un servidor por medio de un canal seguro
en el que toda la información está cifrada.

Cómo usar SSH Agent junto con crontan
------------------------------------------------------------------------

Obtener acceso a ssh dentro de una tarea de crontab es a menudo
problemático, ya que las tareas de crontab se ejecutan en un entorno
**diferente** al del usuario normal. No podemos simplemente ejecutar
``ssh-add`` y esperar que los trabajos dentro de crontab tengan acceso
al mismo. Tenemos que realizar una serie de pasos antes:

1) Instalar ``[Keychain](https://linux.die.net/man/1/keychain)``.

2) Añadir la siguiente línea en ``.bashrc`` o similar que se ejecute en
cada *login*. Esto permite que tanto tu crontab como al shell usar
tus claves ssh y obviar la necesidad de tener que teclear la
contraseña cada vez que se necesite usar la clave. Esto funciona
también entre múltiples sesiones y *shells*.

.. code:: shell

    # Use keychain to keep ssh-agent information available in a file
    /usr/bin/keychain "$HOME/.ssh/id_rsa"
    source "$HOME/.keychain/${HOSTNAME}-sh"

3) Finalmente, poner al inicio del fichero crontab la siguiente orden,
que permitirá a los trabajos acceder al keychain:

.. code:: bash

    source "$HOME/.keychain/${HOSTNAME}-sh"

Fuente: `Use Your SSH Agent in a
Crontab <https://gist.github.com/Justintime50/297d0d36da40834b037a65998d2149ca>`__

Cómo usar ``ssh-agent`` y ``ssh-add`` en Unix
------------------------------------------------------------------------

En Unix, **ssh-agent** es un programa que está ejecutándose en segundo
plano, y que gestiona las contraseñas para acceder a las claves. La
orden ``ssh-add`` pregunta al usuario por la contraseña de una clave
privada y la almacena internamente en una lista. Una vez que se ha
añadido la clave privada al ``ssh-agent``, no se te volverá a preguntar
por la contraseña cuando usemos ``ssh``, ``scp`` para conectarnos a
ordenadores que tengan tu clave pública. La parte pública de la clave
debe estar almacenada en el fichero ``~/.ssh/authorized_keys`` del
ordenador al que queremos acceder (Ver ``ssh-copy-id``).

Para usar ``ssh-agent`` y ``ssh-add``, debemos seguir los siguientes
pasos:

En la *shell*, ejecutamos:

.. code:: shell

    eval `ssh-agent`

.. warning:: Hay que tener cuidado de usar las comillas simples
    invertidas (``backquote``) (\`), no las comillas simples
    normales (’).

Con el agente ya ejecutándose en segundo plano, damos la orden:

.. code:: shell

    ssh-add

Que nos preguntará por la contraseña de la clave privada.

Por seguridad, al salir de la sesión, se debería ejecutar:

.. code:: shell

    kill $SSH_AGENT_PID

Para ejecutar esta orden de forma automática cuando nos desconectamos de
la sesión (*log out*), podemos ponerla en el fichero ``.logout`` (Si
estamos usando ``csh`` o ``tcsh``) o en el fichero ``.bash_logout`` si
estamos usando ``bash``.

Fuente: `Indiana University - About ssh-agent and ssh-add in Unix <https://kb.iu.edu/d/aeww>`_


Como verificar si un certificado X.509 sigue siendo válido
------------------------------------------------------------------------

Un `certificado X.509 <https://en.wikipedia.org/wiki/X.509>`__ X.509 es
un estándar para infraestructuras de claves públicas. Especifica, entre
otras cosas, formatos estándares para certificados de claves públicas y
un algoritmo de validación de la ruta de certificación.

Verificar la validez de un fichero de certificado usando openssl
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Podemos usar la opcion ``x509`` de la utilidad ``openssl``:

.. code:: shell

    $ openssl x509 -in secureweb2025.crt -nocert -dates
    notBefore=Feb 25 12:35:39 2025 GMT
    notAfter=Feb 25 12:35:39 2028 GMT

Donde usamos el *flag* ``-in`` para indicar el fichero de entrada, y
``-dates`` para que nos muestre las fechas de inicio y fin de la
validez. El *flag* ``-nocert`` se usa para que no incluya en la salida el
propio certificado en formato ``PEM``

También tenemos el *flag* ``-checkend``, que nos permite saber si el
certificado seguirá siendo válido en algún momento del futuro. Indicamos
ese momento futuro con el número de segundos a partir de la fecha
actual. La respuesta nos dirá si el certificado es valido para ese
momento o no. Esto puede ser útil para verificaciones de tipo “¿Dentro
de tres meses, este certificado seguirá siendo válido?”:

.. code:: shell

    $ openssl x509 -in secureweb2025.crt -checkend 7862400
    Certificate will not expire

    $ openssl x509 -in secureweb2025.crt -checkend 252288000
    Certificate will expire

El valor :math:`7862400` viene de 91 días:

.. math::  91 \times 24 \times 60 \times 60 =  7862400

El significado del número :math:`252288000` se deja como ejercicio para
el lector.


Verificar un fichero usando Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Para verificar las fechas de validez de un certificado x509 tienes que
instalar la librería `cryptography <https://cryptography.io/en/latest/>`_:

.. code:: shell

    pip install cryptography

Y la forma de comprobar los datos del certificado podría ser:

.. code:: python

    from cryptography import x509

    with open('certificate.crt', 'rb') as f_in:
        pem_data = f_in.read()
        cert = x509.load_pem_x509_certificate(pem_data)
        print(f'Serial number: {cert.serial_number}')
        print(f'No valid after: {cert.not_valid_after}')
        print(f'Issuer: {cert.issuer}')


Que son los ficheros PEM
------------------------------------------------------------------------

Muchos estánadares de criptografía usan
`ASN.1 <https://en.wikipedia.org/wiki/Abstract_Syntax_Notation_One>`__
para definir sus estructuras, y
`DER <https://en.wikipedia.org/wiki/X.690#DER_encoding>`__
(*Distinguished Encoding Rules*) para serializar dichas estructuras.
Como la salida de DER es un conjunto de bytes, puede ser un problema a
la hora de transmitir el fichero por determinados sistemas electrónicos,
que solo soportan ASCII.

El formato PEM resuelve este problema codificando los datos binarios
usando base64. También se define un formato de cabecera compuesto de una
única línea, en la forma ``-----BEGIN [label]-----``, y un formato de
pie equivalente, ``-----END [label]-----``. El valor de ``[label]``
determina el tipo de contenido almacenado. Valores habituales son
``CERTIFICATE``, ``CERTIFICATE REQUEST``, ``PRIVATE KEY`` o
``X509 CRL``:

Por Ejemplo:

.. code::

    -----BEGIN PRIVATE KEY-----

    -----END PRIVATE KEY-----

Los ficheros ``PEM``\ ̀ se almacenan habitualmente con el sufijo
``.pem``, ``.cer`` o ``crt`` y, en los casos de claves públicas o
privadas, el sufijo ``key``. La etiqueta de la cabecera es más fiable
del tipo de contenido que el sufijo, ya que se pueden almacenar
diferentes tipos de contenido usando ``.crt``, por ejemplo.
