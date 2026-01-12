Matomo
========================================================================

Sobre Matomo
------------

**Matomo** es una aplicación web libre y de código abierto, escrita por
un equipo internacional de diseñadores que corre sobre un servidor web
PHP/MySQL. Rastrea en tiempo real páginas vistas y visitas de un sitio
web y muestra reportes de estos datos para su análisis.

Formatos en que se puede obtener la información de Matomo
-----------------------------------------------------------------------

Matomo puede proporcionar la información de todas sus APIS en cualquiera
de los siguientes formatos (Usando el parámetro ``format``):

- CSV o TSV (Separado por tabuladores)
- JSON
- XML
- HTML
- RSS

Por defecto devuelve los resultados en XML.


Parámetros comunes a todas las APIs de Matomo
-----------------------------------------------------------------------

- **``IdSite``**: El identificador (numérico) del *site*. También se
  puede especificar una lista de *ids* seprandolos con comas.

- **``period``**: El periodo de tiempo que engloba las estadísticas
  solicitadas. Puede tener uno de los siguientes valores: ``day``,
  ``week``, ``month``, ``year`` o ``range``.

- ``day`` devuelve datos para un día determinado.

- ``week`` devuelve los datos de la semana que contenga la fecha
  especificada en ``date``.

- ``month`` devuelve los datos del mes que contenga la fecha
  especificada en ``date``.

- ``year``: devuelve los datos del año que contenga la fecha
  especificada en ‘date’

- ``range``: Devuelve los datos incluidos entre las fechas
  especificadas en el campo ``date``, que para este caso no será solo
  una fecha, sino dos fechas separadas por coma. POr ejemplo
  ``date=2011-01-01,2011-02-15``

- **``date``**: Fecha de referencia, especificada en formato
  ``YYYY-MM-DD``. Acepta también ciertos valores especiales que son:
  ``today``, ``yesterday``, ``lastWeek``, ``lastMonth`` o
  ``lastYear``.


Cómo autenticarse en la API de Matomo con el parámetro token_auth
-----------------------------------------------------------------------

Por defecto, las estadísticas de Matomo son privadas. Si no se puede
o no se quieren hacer públicas hay que usar autenticación. Para ello
se incluye en la URL un parámetro llamado ``token_auth``. 

Para  crear tokes de autenticación, hay que ir  a
Administration => Personal => Security => Auth tokens.

Con ese valor, solo tenemos que añadir ``&token_auth=YOUR_TOKEN``
al final de la URL de cada API.  Como es un valor secreto, no debemos
publicar en ningún sitio estas URLs.


La API de acciones de Matomo
-----------------------------------------------------------------------

The Actions API lets you request reports for all your Visitor Actions:
Page URLs, Page titles, Events, Content Tracking, File Downloads and
Clicks on external websites.
