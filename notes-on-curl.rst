Sobre cURL
----------

**cURL** es una biblioteca (``libcurl``) y un intérprete de comandos
(``curl``) orientado a la transferencia de archivos. Soporta los
protocolos FTP, FTPS, HTTP, HTTPS, TFTP, SCP, SFTP, Telnet, DICT, FILE y
LDAP, entre otros.

Fuente: `cURL - Wikipedia <https://es.wikipedia.org/wiki/CURL>`__

Como mostrar las cabeceras de petición y respuesta
--------------------------------------------------

Usa la opción ``-v`` o ``--verbose``. En el resultado, las líneas que
empiezan por ``>`` son de la cabecera de petición, mientras que las que
empiezan por ``<`` son la cabecera de respuesta.

Para mostrar **solo** las cabeceras:

Ademas de ``-v``, hay que usar el flag ``--head`` o ``-I`` para que no
muestre el cuerpo:

.. code:: shell

   curl --head --verbose http://www.parcan.es/

Fuente: `cURL - Display reuqest headers and response
headers <https://mkyong.com/web/curl-display-request-headers-and-response-headers/>`__
