---
title: Notas sobre pyinfra
tags:
    - python
    - sysadmin
    - devops
---

## Notas sobre pyintra

**[Pyinfra](https://pyinfra.com/)** es un software para automatizar infraestructura
implementado en Python. Es rápido y escalable hasta miles de servidores. Los usos
más habituales son ejecución remote de ordenes, despliegue de servicios y gestión
de configuración, entre otros.

Podemos instalarlo sin problemas con `pip`:

```shell
$ python3 -m pip install pyinfra
```

## Para empezar con pyinfra

Para empezar con pyinfra se necesitan dos cosas:

- El **Inventario**: Aquí definimos los ordenadores o _hosts_, grupos y datos.
  Los _hosts_ son los objetivos sobre los que se ejecutan los comandos o los
  cambios de estado de pyinfra. Los _hosts_ pueden ser organizados en
  **grupos**, y les elementos de datos se pueden asignar indistintamente a
  _hosts_ o a grupos. Por defecto, se asume que los _hosts_ se pueden acceder
  usando _SSH_, pero existen conectores para otros sistemas, como por ejemplo, el
  usado para conectar con contenedores _Docker_.

- Las **Operaciones**: Ordenes o nuevos estados que hay que aplicar a uno o más
  _hosts_, ya sea directamente o usando grupos. Estas ordenes pueden ser simples
  comandos de shell como "Ejecuta el comando `uptime`" o cambios de estado como
  "Asegurate de que el paquete `apt` `iftop` esté instalado".

Podemos ejecutar una orden remota, si ya tenemos pyinfra instalado. El cliente
de línea de comandos siempre espera los argumentos en orden, primero el
inventario y luego la orden a ejecutar. Podemos indicar un servidor con ssh, la
máquina local o una instancia de docker:

```shell
# Execute over SSH
pyinfra my-server.net exec -- echo "hello world"

# Execute within a new docker container
pyinfra @docker/ubuntu:18.04 exec -- echo "hello world"

# Execute on the local machine (MacOS/Linux only - for now)
pyinfra @local exec -- echo "hello world"
```

## Cómo definir el inventario en pyinfra

Por defecto, pyinfra asume que los _hosts_ son servidores con acceso por _ssh_, y
se usa simplemente el nombre del host para identificarlo. Si no queremos usar el
conector _ssh_ usado por defecto, podemos prefijar, con `@<nombre del
conector>`. El siguiente ejemplo usa el conector para _Docker_:

```
pyinfra @docker/ubuntu:18.04 exec -- echo "hello world"
```

Un **inventario** es simplemente un fichero `.py`. Los **grupos** se definen
simplemente como listas. El siguiente Ejemplo crea dos grupos, uno para servidores
web y otro para servidores de base de datos:

```PY
web_servers = [
    "atenea",
    "minerva"
    ]

db_servers = [
    "postgres",
    "oracle",
    ]
```

si guardamos este fichero como `inventario.py`, se puede usar cuando ejecutemos
los comandos de pyinfra:

```shell
pyinfra inventario.py OPERATIONS...
```

Además de los grupos definidos internamente en el fichero, todos los _hosts_
mencionados en el fichero de inventario se añaden automáticamente a un grupo con
el mismo nombre que el fichero, sin la extensión `.py`. Es este caso,
`inventario`.

Es posible seleccionar un subconjunto de los _hosts_ definidos en el inventario,
usando el parámetro `--limit`. Si se especifica, solo se ejecutarán las
operaciones indicadas en los _hosts_ que cumplan la condición especificada. Se
pueden especificar varias veces, y se pueden usar el nombre completo de un
grupo o un patrón usando el asterísco `*` como comodín. Algunos ejemplos:

```
# Solo en local
pyinfra inventory.py deploy.py --limit @local

# Solo en los servidor dentro del grupo web_servers
pyinfra inventory.py deploy.py --limit web_servers

# Solo en los servidores dentro de grupos cuyo nombre case con *_servers
pyinfra inventory.py deploy.py --limit "*_servers"

# Usando varios límites
pyinfra inventory.py deploy.py --limit web_servers --limit postgres
```

## Asignar datos a hosts

Se pueden asignar datos a _hosts_ individuales, usando una tupla `(hostname, data_dict)`:

```
minerva = [
    ("srv-minerva", {"ssh_user": 'informatica'}),
    ("srv-minerva-dev", {"ssh_user": 'informatica'}),
]
```

Estos datos pueden ser recuperados en fichero de operaciones:

```py
from pyinfra import host

if host.data.get("install_postgres"):
    apt.packages(
        packages=["postgresql-server"],
    )
```

## Asignar datos a grupos

Para asignar catos a grupos, debemos crear ficheros `.py`, con el mismo nombre que los
grupos, **dentro del directorio `group_data`** (Aunque se puede usar otro
directorio si especificamos el parámetro `--group-data`). Todos los _hosts_ 
del grupo reciben las varibales y valores definidos así.


## Definición de estados en pyinfra

Podemos usar operaciones para definir determinados estados en los que queremos
que estén nuestro _hosts_. Siempre que sea posible, se intenta usar el estado
para determinar qué cambios habría que efectuar, si es que hay que hacerlos,
para llevar a la máquina al estado deseado.

Esto significa que los cambios de estado son
[idempotentes](https://es.wikipedia.org/wiki/Idempotencia); si ejecutamos el
cambio de estado dos veces, el segundo no hará nada, porque ya estamos en el
estado deseado.

## Como definir y usar operaciones en pyinfra

Las **operaciones** le dicen a pyinfra que cosas deben ser hechas en los objetivos
o _targets_. Existen varios tipos de operaciones, por ejemplo, las operaciones
`server.shell` ejecutan un comando usando la shell del _host_.

La mayoría de las operaciones definen **estados**, más que acciones. A modo de
ejemplo, en vez de pensar en operaciones: "Arrancar este servicio", debemos
pensar en estados: "Este servicio debería estar arrancado". De esta forma,
las ordenes se ejecutarán solo si fuera necesario.

El siguiente ejemplo verifica que el usuario `pyinfra` existe, que su
directorio principal es `/home/pyinfra`, y también que el fichero `/var/log/pyinfra.log`
existe, que es propiedad del usuario `pyinfra`, y que tienes como _bits_ de permisos
el valor `644`.

```python3
# Import pyinfra modules, each containing operations to use

from pyinfra.operations import server, files

server.user(
    name="Create pyinfra user",
    user="pyinfra",
    home="/home/pyinfra",
)

files.file(
    name="Create pyinfra log file",
    path="/var/log/pyinfra.log",
    user="pyinfra",
    group="pyinfra",
    mode="644",
    _sudo=True,
)
```

Esta operación usa operaciones de los tipos `server` y `files`. En la
documentación oficial se puede consultar [la lista de operaciones
disponibles](https://docs.pyinfra.com/en/2.x/operations.html). Si salvamos este
_script_ con el nombre `deploy.py`, podemos testearlo usando una imagen Docker:

```shell
pyinfra @docker/ubuntu:20.04 deploy.py
```
