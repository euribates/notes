---
title: Notes on Meilisearch
---

## Sobre Meilisearch

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

### Consultas usando la web

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