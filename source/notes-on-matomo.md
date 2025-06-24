---
title: Notas sobre matomo
---

## Sobre Matomo

## Formatos en que se puede obtener la información de Matomo

Matomo puede proporcionar la informacion de todas sus APIS en cualquiera de los
siguientes formatos:

- CSV o TSV (Separado por tabuladores)
- JSON
- XML
- HTML
- RSS

Por defecto devuelve los resultados en XML.

Usando el parámetro `format`.

## Parámetros comunes a todas las APIs de Matomo

- **`IdSite`**: El identificador (numérico) del _site_. También se puede especificar
  una lista de _ids_ seprandolos con comas.

- **`period`**: El periodo de tiempo que engloba las estadísticas solicitadas. Puede
  tener uno de los siguientes valores:
`day`, `week`, `month`, `year` o `range`.

  - `day` devuelve datos para un día determinado.

  - `week` devuelve los datos de la semana que contenga la fecha especificada en
    `date`.

  - `month` devuelve los datos del mes que contenga la fecha especificada en
    `date`.

  - `year`: devuelve los datos del año que contenga la fecha especificada en 'date'

  - `range`: Devuelve los datos incluidos entre las fechas especificadas en el
    campo `date`, que para este caso no será solo una fecha, sino dos fechas
    separadas por coma. POr ejemplo `date=2011-01-01,2011-02-15`

- **`date`**: Fecha de referencia, especificada en formato 
    `YYYY-MM-DD`. Acepta también ciertos valores especiales
    que son: `today`, `yesterday`, `lastWeek`, `lastMonth` o `lastYear`.

## Authenticate to the API via token_auth parameter

In the example above, the request works because the statistics are public (the
anonymous user has a view access to the website). By default, in Matomo your
statistics are private. In the case that you cannot have your statistics to be
public:

when you access your Matomo installation you are requested to log in when you
call the API over http you need to authenticate yourself. This is done by adding
a secret parameter called `token_auth` in the URL. This parameter is as secret
as your login and password!

You can create authentication tokens in the Administration area under
Administration => Personal => Security => Auth tokens.

Then you simply have to add the parameter &token_auth=YOUR_TOKEN at the end of
your API call URL.

You should never share a URL that includes a token_auth with another person as
this person could use this same token to fetch and change data in Matomo.


## Actions

The Actions API lets you request reports for all your Visitor Actions: Page
URLs, Page titles, Events, Content Tracking, File Downloads and Clicks on
external websites.
