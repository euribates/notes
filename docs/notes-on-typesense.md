---
title: Notas sobre Typesense
tags:
  - systemd
  - linux
  - docker
---

## Sobre Typesense

Es un motor de búsqueda libre, escrito en C++. Muy rápido y tolerante a fallos.

- Repositorio: [Github typesense](https://github.com/typesense/typesense)

Principales características:

- Tolerante ante faltas de ortografía
- Rápido
- Fácil de instalar (En Linux por lo menos)
- _Clustering_ de serie, si hace falta
- Búsqueda a la vez que tecleas. Chorrada, pero mola.
- Segmentación de búsqueda (_Faceted search_)
- Filtrado por campos

## Instalar Typesense

En linux:

```shell
curl -O https://dl.typesense.org/releases/0.23.1/typesense-server-0.23.1-amd64.deb
sudo apt install ./typesense-server-0.23.1-amd64.deb
```

Para ver que está instalado y funcionando:

```shell
sudo systemctl status typesense-server.service
```

## Cómo conectar con el cliente Python al servidor Typesense

Usaremos la api para crear un objeto de la clase `Client`:

```python
import typesense

client = typesense.Client({
    'api_key': 'abcd',  # La clave definida en la configuracion
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'connection_timeout_seconds': 6
})
```

## Cómo crear Colecciones en Typesense

En `typesense`, los documentos que indexamos se almacenan en **colecciones**.

Antes de poder añadir documentos debemos crear una colección. Para
ello usamos la llamada `client.collections.create(schema)`.

Podemos dejar que
`typesense` descubra la estructura de los documentos por si mismo, pero es
preferible darle esta información ya procesada, y esto se hace con el parámetro
`schema`, que es un diccionario con los parámetros que tendrá la
colección/índice. De esta forma tenemos un control más detallado.


Vemos un ejemplo:

```python
create_response = client.collections.create({
    "name": "tareas",
    "fields": [
        {"name": "id", "type": "int64"},
        {"name": "url", "type": "string"},
        {"name": "titulo", "type": "string"},
        {"name": "descripcion", "type": "string"},
        {"name": "estado", "type": "string"},
        {"name": "prioridad", "type": "int32"},
        {"name": "f_creacion", "type": "float"},
        {"name": 'notas', 'type': "string[]"},
        {"name": 'clasificadors', 'type': "string[]"},
    ],
    "default_sorting_field": "f_creacion"
})
```

## Como listar las colecciones disponibles en el servidor

Para poder ver los colecciones disponibles en el servidor, podemos llamar
a `client.collections.retrieve()`. Si acabamos de instalar el servidor, lo
normal sera que no tengamos ninguna colección disponible:

```python
>>> print(client.collections.retrieve())
[]
```

### Cómo acceder a una colección sabiendo su nombre:

Si suponemos que el nombre es `tareas`:

```python
client.collections['tareas'].retrieve()
```


## Cómo indexar un documento

Si hemos definido un esquema para la colección, los documentos deben
ser conformes al esquema.

Si existe un campo `id`, de tipo `string`, `typesense`
usará el valor de este campo como clave primaria. **No se puede especificar otro
nombre**.

## Cómo buscar en Typesense

Las búsquedas se realizan mediante una **`query`** o texto de consulta, que
se buscará en una serie de campos de tipo `string`. Los campos de otros tipos se
pueden usar para filtrar, segmentar u ordenar los resultados.

El orden de búsqueda de los campos `string` en los que se buscará el
texto de la consulta se especifica con **`query_by`**, y es una lista de nombres
de campos separados por comas. El orden importa, de forma que para una palabra
encontrada en un campo, esa coincidencia tiene un peso o rango superior
al de una aparición en otro campo listado después.

Por ejemplo, si tenemos los campos de texto `title` y `body`, y
`query_by` está definido como `title, body`, las palabras encontradas
en el título tienen mayor peso e importancia
que las encontradas en el cuerpo.

El filtrado se realiza usando el parámetro **`filter_by`**. 

- **Búsquedas exactas**: Podemos filtrar
  usando el operador `:=`
  para señalar coincidencias exactas.
  Por ejemplo, si tenemos un campo entero `priority`,
  podemos hacer `priority:=7`. También podemos filtrar
  con un conjunto de valores: `priority:=[7,8,9]`. Si es un campo
  de texto, tenemos que incluir el texto completo tal y como
  esté en el campo del documento para que lo encuentre.

- **Búsquedas parciales**: Si usamos el operador `:`, entonces
  se realiza una comparación parcial,
  a partir del inicio de la palabra.
  Por ejemplo, `title:shoe` encontrará y filtrará
  los documentos que contengan en su título las palabras
  `shoe`, `shoes`, `shoemaker`, etc. 

  Igual que con el operador `:=`, también podemos buscar por un conjunto,
  por ejemplo `title:[shoe, boots, footwear, sandals]`.

- **Búsqueda por rango**: Para los valores numéricos
  podemos usar el operador de rango `..`. Por ejemplo:
  `priority:[1..5]`. También tenemos los operadores `:<`,
  `:<=`, `:>`, `:>=` y `:!=`.

Si queremos usar más de un filtro, podemos hacerlo con el operador `&&`.
Por ejemplo `title:show && priority :< 6`.
