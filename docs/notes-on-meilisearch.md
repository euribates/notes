---
title: Notes on Meilisearch
tags:
  - Python
  - Web
---

## Sobre Meilisearch

## Instalar Meilisearch un Ubuntu

Bajamos el script de instalación:

```shell
sudo wget -qO /usr/local/bin/meilisearch https://github.com/meilisearch/meilisearch/releases/latest/download/meilisearch-linux-amd64
sudo chmod a+x /usr/local/bin/meilisearch
```

Comprobemos la versión con:

```
meilisearch --version
```

debería producir:

```
meilisearch-http 0.30.0
```

Ver ahora [Como pasar Meilisearch a producción](#como-pasar-meilisearch-a-produccion)



## Primeros pasos

### Crear un índice y actualizar documentos

Si el servidor est ejecutandose, suponemos en el host local y en el puerto
estándar, $7700$, podemos crear un indice y alimentarlo con datos usando `curl`.
Vamos a usar la base de datos de películas que se puede descargar
desde aquí: [The movie
database](https://www.notion.so/meilisearch/A-movies-dataset-to-test-Meili-1cbf7c9cfa4247249c40edfa22d7ca87#b5ae399b81834705ba5420ac70358a65). descargemos la base de datos en formato json al fichero `movies.json`.

```shell
curl -L https://docs.meilisearch.com/movies.json -o movies.json
```

AHora, para crear el índice y alimentarlo:

```shell
curl -i -X POST 'http://127.0.0.1:7700/indexes/movies/documents' \
  --header 'content-type: application/json' \
  --data-binary @movies.json
```

## Consultas usando la web

Se puede usar directamente la API web para realizar consultas, usado curl (y `jq` en el ejmplo para mejorar la presentacion del json generado:

```shell
curl 'http://127.0.0.1:7700/indexes/movies/search?q=botman+robin&limit=2' | jq
```

Produciría algo como:

```js
{
  "hits": [
    {
      "id": "415",
      "title": "Batman & Robin",
      "poster": "https://image.tmdb.org/t/p/w1280/79AYCcxw3kSKbhGpx1LiqaCAbwo.jpg",
      "overview": "Along with crime-fighting partner Robin and new recruit Batgirl, Batman battles the dual threat of frosty genius Mr. Freeze and homicidal horticulturalist Poison Ivy. Freeze plans to put Gotham City on ice, while Ivy tries to drive a wedge between the dynamic duo.",
      "release_date": 866768400
    },
    {
      "id": "411736",
      "title": "Batman: Return of the Caped Crusaders",
      "poster": "https://image.tmdb.org/t/p/w1280/GW3IyMW5Xgl0cgCN8wu96IlNpD.jpg",
      "overview": "Adam West and Burt Ward returns to their iconic roles of Batman and Robin. Featuring the voices of Adam West, Burt Ward, and Julie Newmar, the film sees the superheroes going up against classic villains like The Joker, The Riddler, The Penguin and Catwoman, both in Gotham City… and in space.",
      "release_date": 1475888400
    }
  ],
  "nbHits": 8,
  "exhaustiveNbHits": false,
  "query": "botman robin",
  "limit": 2,
  "offset": 0,
  "processingTimeMs": 2
}
```

## Crear un índice con Python

Para crear un índice en Meilisearch, hay que asignarle un nombre y decirle el
atributo que debe usar como clave primaria. Por ejemplo:

```
import meilisearch

client = meilisearch.Client('http://127.0.0.1:7700', 'masterKey')
client.create_index('notes', {'primaryKey': 'id'})
```


## Consultar un índice con Python

Primero, tenemos que instalar el cliente para meilisearch, si no estuviera ya
instalado:

```shell
pip install meilisearch
```

El siguente ejemplo muestra una consulta sencilla:

```python
import datetime
import meilisearch

client = meilisearch.Client('http://127.0.0.1:7700')
index = client.index('movies')
for movie in index.search('spiderman')['hits']:
     release_date = datetime.datetime.utcfromtimestamp(movie['release_date'])
     print(movie['title'], release_date.year)
```
Debería producir un resultado similar a este:

```
Spider-Man: Into the Spider-Verse 2018
Spider-Man: Homecoming 2017
Spider-Man 2002
Spider-Man 3 2007
Spider-Man: Far from Home 2019
Spider-Man 2 2004
The Amazing Spider-Man 2 2014
The Amazing Spider-Man 2012
The Amazing Spider-Man 1978
LEGO Marvel Super Heroes: Maximum Overload 2013
LEGO Marvel Super Heroes: Avengers Reassembled! 2015
```


## Como saber la version de Meilisearch instalada

Se puede hacer desde la línea de comandos:

```shell
$ meilisearch --version
meilisearch-http 0.28.1
```

O desde la API web, si el servidor se está ejecutando, por ejemplo en:

    http://127.0.0.1:7700/version/

Nos daría la respuesta:

```js
{
    "commitSha":"22aa349e31bc7662a065f4dc3229a93abd1f1f33",
    "commitDate":"2022-07-21T11:08:37Z",
    "pkgVersion":"0.28.1"
}
```

## Como pasar Meilisearch a producción

Necesitamos una version de Linux moderna y un par de claves ssh.

1) Instalar Meilisearh

```
curl -L https://install.meilisearch.com | sh
sudo mv ./meilisearch /usr/bin
sudo chmod a+x /usr/bin/meilisearch
```

Y ver que funciona:

```
$ meilisearch --version
meilisearch-http 0.29.2
```

2) Convertir meilisearh en un servicio

Usaremos systemd. Los servicios de `systemd` están definidos como ficheros de
texto en `/etc/systemd/system`. Para ejecutar Meilisearch en modo servidor
hay que usar la opción `--env`. Para definir la clave maestra se usa
`--masterkey`.

Cuando se ejecuta por primera vez, Meilisearch crea dos
claves API: `Default Admin API Key` y `Default Search API Key`. Usaremos la
primera para operaciones de mantenimiento como crear nuevos documentos,
índices, o cambios en la configuración, mientras que ls segunda se usará para
las busquedas.

Ahora el fichero service en `/etc/systemd/system/meilisearch.service` podría
ser algo como esto:

```
[Unit]
Description=Meilisearch
After=systemd-user-sessions.service

[Service]
Type=simple
ExecStart=/usr/local/bin/meilisearch --http-addr 127.0.0.1:7700 --env production --master-key Y0urVery-S3cureAp1K3y

[Install]
WantedBy=default.target
```

En esta configuración 
el servidor esta viculado a la direccion `127.0.0.1` lo que significa que solo
aceptará conexiones desde la máquina local. En producción habría que ponerla en
la IP `0.0.0.0`.

Ahora arrancamos el servicio:

```bash
$ sudo systemctl enable meilisearch.service
$ sudo systemctl start meilisearch.service
```

Y comprobamos que esta funcionando:

```bash
$ sudo systemctl status meilisearch.service
```

Debería producir al final:

```bash
● meilisearch.service - Meilisearch
     Loaded: loaded (/etc/systemd/system/meilisearch.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2022-11-23 11:30:09 WET; 1s ago
   Main PID: 30162 (meilisearch)
      Tasks: 10 (limit: 9256)
     Memory: 7.4M
        CPU: 47ms
     CGroup: /system.slice/meilisearch.service
             └─30162 /usr/bin/meilisearch --http-addr 127.0.0.1:7700 --env production --master-key Y0urVery>

Nov 23 11:30:10 nova meilisearch[30162]: Thank you for using Meilisearch!
Nov 23 11:30:10 nova meilisearch[30162]: We collect anonymized analytics to improve our product and your ex>
Nov 23 11:30:10 nova meilisearch[30162]: Anonymous telemetry:        "Enabled"
Nov 23 11:30:10 nova meilisearch[30162]: Instance UID:                "1d6ead4c-3d21-42d9-ba0b-b91b031c9bd5"
Nov 23 11:30:10 nova meilisearch[30162]: A Master Key has been set. Requests to Meilisearch won't be author>
Nov 23 11:30:10 nova meilisearch[30162]: Documentation:                https://docs.meilisearch.com
Nov 23 11:30:10 nova meilisearch[30162]: Source code:                https://github.com/meilisearch/meilise>
Nov 23 11:30:10 nova meilisearch[30162]: Contact:                https://docs.meilisearch.com/resources/con>
Nov 23 11:30:10 nova meilisearch[30162]: [2022-11-23T11:30:10Z INFO  actix_server::builder] Starting 4 work>
Nov 23 11:30:10 nova meilisearch[30162]: [2022-11-23T11:30:10Z INFO  actix_server::server] Actix runtime fo>
...
```

En este momento el sistema esta funcionando y preparado para posibles caidas,
reinicios del sistema, etc.

3) Usar el sistema desde `nginx`

Si queremos dar acceso al sistema enel puerto 7000, probablemente tendremos que definir 
una entrada especifica en `nginx`.

