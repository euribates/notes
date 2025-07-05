---
title: Notas sobre pyinfra
tags:
    - python
    - sysadmin
    - devops
    - curl
    - jinja2
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

## Cómo definir y usar operaciones en pyinfra

Las **operaciones** son lo que usamos para instruir a pyinfra sobre lo que
tiene que hacer. Por ejemplo, la operación `server.shell` sirve para que pyinfra
ejecute un comando mediante la _shell_.

Es preferible que las operaciones **definan un estado**,
mejor que listar acciones a ejecutar. Es decir, en vez de
especificar "Arranca este servicio", indicamos "Este servicio debería estar
arrancado". De esta forma pyinfra solo ejecuta las acciones
si es necesario. En el ejemplo anterior, si el servicio ya
está arrancado, no haría nada.

La siguiente operación especifica que debe existir un usuario `pyinfra`, con su
directorio inicial en `/home/pyinfra`, y que debe existir un fichero en
`/var/log/pyinfra.log`, propiedad de dicho usuario:

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
disponibles](https://docs.pyinfra.com/en/2.x/operations.html).

Si salvamos este _script_ con el nombre `deploy.py`, podemos testearlo usando una imagen Docker:

```shell
pyinfra @docker/ubuntu:20.04 deploy.py
```

## Operaciones sobre ficheros

Las operaciones sobre ficheros gestionan el estado de los ficheros del sistema,
las cargas de ficheros y la generación de ficheros mediante plantillas.

### [`files.block`](https://docs.pyinfra.com/en/2.x/operations/files.html#files-block)

Verifica que un determinado contenido, comprendido entre
unos marcadores apropiados, esté -o no-, en el fichero indicado. El
estado final será que el fichero tendrá -o no- ese texto.

Ejemplo:

```python
# add entry to /etc/host
files.block(
    name="add IP address for red server",
    path="/etc/hosts",
    content="10.0.0.1 mars-one",
    before=True,
    regex=".*localhost",
)
```

### [`files.directory`](https://docs.pyinfra.com/en/2.x/operations/files.html#files-directory)

Añadir/borrar/actualizar directorios. Ejemplo:

```python
files.directory(
    name="Ensure the /tmp/dir_that_we_want_removed is removed",
    path="/tmp/dir_that_we_want_removed",
    present=False,
)
```

[`files.download`](https://docs.pyinfra.com/en/2.x/operations/files.html#files-download)

Descargar ficheros de una localización remota usango `curl` o `wget`.
Ejemplo:

```python
files.download(
    name="Download the Docker repo file",
    src="https://download.docker.com/linux/centos/docker-ce.repo",
    dest="/etc/yum.repos.d/docker-ce.repo",
    )
```

### [`files.file`](https://docs.pyinfra.com/en/2.x/operations/files.html#files-file)

Añadir/borrar/actualizar archivos. Ejemplo:

```python
# Note: The directory /tmp/secret will get created with the default umask.
files.file(
    name="Create /tmp/secret/file",
    path="/tmp/secret/file",
    mode="600",
    user="root",
    group="root",
    touch=True,
    create_remote_dir=True,
    )
```

### [`files.flags`](https://docs.pyinfra.com/en/2.x/operations/files.html#files-flags)

Ajustar _flags_ de ficheros

Ejemplo:

```python
files.flags(
    name="Ensure ~/Library is visible in the GUI",
    path="~/Library",
    flags="hidden",
    present=False
)
```

### [`files.get`](https://docs.pyinfra.com/en/2.x/operations/files.html#files-get) Descargar
un archivo desde el sistema

!!! warning "Esta operación no tiene estado"

    La operación siempre se ejecutará, **no es idempotente**.

Ejemplo:

```python
files.get(
    name="Download a file from a remote",
    src="/etc/centos-release",
    dest="/tmp/whocares",
    )
```

### [`files.line`](https://docs.pyinfra.com/en/2.x/operations/files.html#files-line)

Verifica líneas de un fichero usando `grep` para localizarlas y `sed` para
cambiarlas. Ejemplo:

```python
files.line(
    name="Ensure myweb can run /usr/bin/python3 without password",
    path="/etc/sudoers",
    line=r"myweb .*",
    replace="myweb ALL=(ALL) NOPASSWD: /usr/bin/python3",
    )
```

### [`files.link`](https://docs.pyinfra.com/en/2.x/operations/files.html#files-link)

Añadir/borrar/actualizar enlaces


[`files.put`](https://docs.pyinfra.com/en/2.x/operations/files.html#files-put)

Subir un fichero (O un objeto de tipo fichero) a los sistemas remotos. Ejemplo:

```python
files.put(
    name="Update the message of the day file",
    src="files/motd",
    dest="/etc/motd",
    mode="644",
    )
```


### [`files.replace`](https://docs.pyinfra.com/en/2.x/operations/files.html#files-replace)

Reemplaza el contenido de un fichero usand `sed`.


### [`files.rsync`](https://docs.pyinfra.com/en/2.x/operations/files.html#files-rsync)

!!! warning "Esta operación no tiene estado"

    La operación siempre se ejecutará, **no es idempotente**.
    Además, está en versioón de pruebas (alfa). Solo chuta
    con `ssh`.

Sincronizar los contenidos de una carpeta local con otra en el sistema remoto,
usando `rsync`. Está operación ejecutará el binario `rsync` en el sistema local.

### [`files.sync`](https://docs.pyinfra.com/en/2.x/operations/files.html#files-sync)

Sincroniza un directorio local con otro remoto, incluyendo borrados. Esta
operación borrará os ficheros extra que encuentre en el sistema remoto, pero
**no** los directorio extra.

### [`files.template`](https://docs.pyinfra.com/en/2.x/operations/files.html#files-template)

Genera un fichero en el servidor remoto, a partir de una plantilla Jinja2.

Ejemplo:

```python
# Example showing how to pass python variable to template file. You can also
# use dicts and lists. The .j2 file can use `{{ foo_variable }}` to be interpolated.

foo_variable = 'This is some foo variable contents'
foo_dict = { "str1": "This is string 1", "str2": "This is string 2" }
foo_list = [ "entry 1", "entry 2" ]

template = StringIO("""
name: "{{ foo_variable }}"
dict_contents:
    str1: "{{ foo_dict.str1 }}"
    str2: "{{ foo_dict.str2 }}"
list_contents:
{% for entry in foo_list %}
    - "{{ entry }}"
{% endfor %}
""")

files.template(
    name="Create a templated file",
    src=template,
    dest="/tmp/foo.yml",
    foo_variable=foo_variable,
    foo_dict=foo_dict,
    foo_list=foo_list
)
```


