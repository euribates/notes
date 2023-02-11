---
title: Notas sobre pyenv
tags:
  - python
  - virtualization
---

## Sobre pyenv

[Pyenv](https://github.com/pyenv/pyenv#readme) es una utilidad que te permite
conmutar fácilmente entre versiones de Python. Sigue la filosofía Unix de hacer
solo una cosa pero hacerla bien.

Una ventaja que tiene es que **no depende de python**, es un conjunto de
scripts de shell.

## Instalar pyenv

Lo mejor es instalarlo acompañado de virtualenv, para ello hay que instalar
tanto `pyenv` como `pyenv-virtualenv`.

### En Mac:

```shell
brew install pyenv
brew install pyenv-virtualenv
```

Y luego añadir esto en el fichero `.bashrc`: 

```
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

### En linux:

```shell
curl https://pyenv.run | bash
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
     libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
     libncurses5-dev libncursesw5-dev \
     xz-utils tk-dev libffi-dev liblzma-dev \
     python-openssl git
$ curl https://pyenv.run | bash
```

## Crear un entorno virtual con pyenv

Hay que ejecutar `pyenv virtualenv <python.version> <name>`, donde
`<python.version>` es una especificación de la versión de python usando 4
dígitos separadospor coma, cmo `2.7.18` o `3.11.2`, y `<name>` el nombre del
virtualenv:

```shell
pyenv virtualenv 3.11.2 newacl
```

Si no se especifica la versión, se instlara la última version conocida por
pyenv.

## Listando los virtualenvs existentes

Con el comando `pyenv virtualenvs`.


## Activando/Desactivando los entornos virtuales con pyenv

Si en una carpeta existe un fichero `.python-version` cuyo contenido case con
el nombre de un entorno virtual, y si hemos ejecutado previmente en la shell:

`eval "$(pyenv virtualenv-init -)"`

(Esto normalmente se hace en el fichero `.bash-rc`)

Al cambiar a este directorio **se activa automáticamente el entorno virtual**,
y si nos salimos del directorio, se desactiva también automáticamente.

También podemos activar/desactivar manualmente en entorno con los comandos:

```shell
pyenv activate <name>
pyenv deactivate
```

## Borrar un entorno virtual creaco con pyenv

Usaremos el comando `unnistall` de pyenv:

```shell
pyenv uninstall <name>
```

## Cómo actualizar la lista de versiones de Python conocidas por pyenv

Con el comando **`pyenv update`**. 

O si estás en un Mac, **`brew upgrade pyenv`**.

## Cómo listar las versiones posibles de python disponibles

Con la orden `install`, usando el flag `--list` o `-l`:

```shell
pyenv install --list
```
