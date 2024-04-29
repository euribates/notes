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



