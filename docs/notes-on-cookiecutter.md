---
title: Notas sobre cookiecutter
tags:
    - python
    - django
    - templates
---

## Acerca de CookieCutter

[CookieCutter](https://github.com/cookiecutter/cookiecutter/) es un programa que
te permite crear una estructura de ficheros y directorios conforma a una
plantilla predefinida. Es multiplataforma y funciona desde la version pyhon 3.7
en adelante. Las plantillas puedes ser de cualquier tipo, siempre que sea texto:
Python, JavaScript, Ruby, CoffeeScript, RST, Markdown, CSS, HTML, etc.

Los contenidos se generan usando
[jinja2](https://jinja.palletsprojects.com/en/3.1.x/).  Las etiquetas de jinja
se pueden aplicar a carpetas, nombres de ficheros y contenidos de los mismos.

## Cómo hacer un ejemplo sencillo de uso de CookieCutter

Si no está instalado, el primer paso sera instalar cookiecutter:

```
pip install cookiecutter
```

Podemos crear un directorio donde CookieCutter busca por defecto las
plantillas que puede usar, `~/.cookiecutters`:

```shell
mkdir ~/.cookiecutter
```

Pero no es necesario usarlo, podemos usar como plantillas directamente desde un
repositorio git o desde un directorio local. Para este caso vamos a usar
carpetas locales, que son la forma máß sencilla.

Vamos a crear una plantilla para que nos genere el programa "Hola, mundo", pero
con nuestro nombre. Para eso creamos, dentro de `.cookiecutter`, la carpeta
`cookiecutter-hola`, y nos cambiamos a ella:

```shell
mkdir cookiecutter-hola && cd $_
```

Dentro de esta carpeta tenemos que crear, obligatoriamente, un fichero en
formato ".json" que contendra los datos que vamos a inyectar en el sistema
de plantillas. Este fichero se tiene que llamar `cookiecutter.json`. 

```
$ touch cokiecutter.json
$ vim cookiecutter.json
```

En nuestro caso, solo vamos a inyectar el nombre de la persona que queremos
saludar, así que nos valdría con este contenido:

```json
{
    "app_name": "hola",
    "name": "<Tu nombre aqui>"
}

Ahora tenemos que crear una carpeta cuyo nombre contenga alguno de los valores
definidos en este fichero. Normalmente se usa la entrada `project-name`, pero
cualquier clave que esté en este diccionario valdria. En nuestro caso, usaremos
el
valor en `app_name` para la carpeta que contendrá nuestrp programa, asi que
tenenos que crear una carpeta que se llame:

```shell
$ mkdir "{{cookiecutter.app_name}}"
```

y, dentro de esta carpeta (Todo lo que está fuera, se ignora, excepto el fichero
`cookiecutter.json`) crearemos la plantilla o plantillas para nuestro proyecto, en este caso, el
fichero python:

```
{{ raw }}
$ touch "{{cookiecutter.app_name}}"/hola.py
$ vim "{{cookiecutter.app_name}}"/hola.py
{{ endraw }}
```

Cuyo contendo podria ser:

```python
{{ raw }}
#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
    print("Hola {{ cookiecutter.name }}")


if __name__ == "__main__":
    main()
{{ endraw }}
```

Dentro de la plantilla estamos inyectando la variable definida como `name`. Es
necesario cualificar la variable con el prefijo `cookiecutter.`

Ahora podriamos hacer:

```shell
$ cookiecutter cookiecutter-hola
app_name [hola]: hola
name [<Tu nombre aqui>]: Pepe Monagas
```

Y esto nos generaría una carpeta `hola` y un fichero `hola/hola.py`, con el
siguiente contenido:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
    print("Hola Pepe Monagas")


if __name__ == "__main__":
    main()
```



