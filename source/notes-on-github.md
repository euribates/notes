---
title: Notas sobre GitHub y el cliente GH
tags:
    - git
    - cli
---

## Sobre GitHub


## Autenticación con Git/SSH: Sistemas de seguridad en GitHub

En GitHub hay varias formas de identificarse y autenticarse. De menor a mayor
complejidad, las más habituales son:

- SSH _agent forwarding_

- Usando HTTPS con _Auth tokens_

- Claves de despliegue

Veremos brevemente cada una de estas formas, con sus ventajas e inconvenientes

### SSH _Agent forwarding_

Este es un sistema especialmente apto para desarrollo. Usa el mismo mecanismo
de _ssh_ que hay instalado en el sistema operativo. Las ventajas principales
son:

✅ No hay necesidad de generar o gestionar nuevas claves.

✅ La gestión de la seguridad es mínima, los usuarios tienen en local
   los mismos privilegios que tengan en remoto.

✅ No se almacenan las claves secretas en el servidor.

En su contra tiene:

❌ Los usuarios tienen que autenticarse en _ssh_, esto dificulta el despliegue
automático.

❌ En windows el sistema ssh puede dar problemas.

El sistema se basa en tener un agente, apropiadamente llamado `ssh-agent`, que
se ejecuta como un proceso en segundo plano, y que puede almacenar internamente
las parejas de clave privada/pública, y realizar las operaciones de
autenticación por nosotros cada vez que se requiera.

Este programa carga por defecto las claves `~/.ssh/id_rsa` y
`~/.ssh/id_rsa_public`, así que normalmente ni llegamos a enterarnos de que
está funcionando, simplemente trabajamos con el comando `git` y si este
necesita autenticación/autorización para alguna operación, habla con
`ssh-agent`.

### Usando HTTPS con Auth tokens

Si no queremos usar `ssh`, la siguiente alternativa es usar el protocolo
`https` y un token _OAuth_.

Ventajas de _HTTPS/OAuth Token_:

✅ Cualquiera que tenga acceso al servidor puede desplegar el repositorio.

✅ No hay que usar ni configurar el sistema _ssh_.

✅ No hacen falta múltiples tokens, uno por cada usuario. Un único _token_
   es suficiente.

✅ El token se puede revocar en cualquier momento, por lo que en la práctica
   funciona como una contraseña compartida.

Inconvenientes

❌ La gestión de la seguridad del _token_ es complicada, porque se tiene que
   definir con cierto detalles los ámbitos, es decir, el _token_ actúa como un
   conjunto de permisos, algunos activos y otros no, y puede resultar complejo
   definir correctamente caules son necesarios y cuales no.

❌ A todos los efectos, son contraseñas, y tiene que ser protegidas de igual
   manera.

❌ Hay que integrar el token con el cliente _git_. Si usamos _scripts_, por
   ejemplo, y el _token_ esta incluido en el mismo, puede ser un problema
   de seguridad. De nuevo, esto complica el despliegue automático.


### Usando claves de despliegue

Con GitHub podemos asignar un **_deploy key_** o **clave de despliegue** a 
cada repositorio. Una clave de despliegue es solo la parte pública de una
pareja de claves privada/pública RSA. La parte privada nunca sube al servidor,
sino que se mantiene en la máquina sobre la que se quiere desplegar.

Las claves de despliegue solo tienen un permiso que definir: Si se permite
desde este repositorio hacer _push_ al repositorio de origen o no. Para el
resto de permisos, asume los mismos que un usuario con permisos de `admin`, o
los de un colaborador para repositorios personales.

Ventajas de las claves de despliegue

✅ Las claves privadas nunca salen de nuestros servidores. Solo se expone en
_GitHub_ la parte pública.

✅ Cualquiera que tenga acceso al repositorio y al servidor puede desplegar el
proyecto.

✅ Los usuarios no tienen que modificar sus sistemas _ssh_ (Con una importante
excepción que se explica más adelante).

✅ Las claves por defecto son de solo lectura, pero se pueden cambiar por
   claves de escritura/lectura, es decir, que permiten hacer _push_ as
   repositorio.

Inconvenientes:

❌ Las claves de repositorio dan acceso a **un único servidor**. Proyectos que
necesiten acceder a más de un repositorio diferente requieren ciertos ajustes,
básicamente para poder indicar en cada proyecto que clave corresponde con que
repositorio. Esto es así porque _GitHub_ **prohibe** usar la misma clave
pública como clave de despliegue de más de un repositorio. 

Obsérvese que lo que si se puede hacer es tener varias claves públicas
diferentes como claves de despliegue del mismo repositorio. Podríamos tener por
ejemplo, con claves de despliegue en el mismo repositorio, uno con acceso de
solo lectura y otro con lectura/escritura.

❌ Para el despliegue automático, las parejas de claves suelen almacenarse sin
contraseña, pudiendo ser un punto débil de la seguridad. Por otro lado, las
claves de despliegue pueden ser eliminadas y cambiarse por otras en cualquier
momento.


## Como configurar la autenticación con _GitHub_

Con servidores como Cronos, donde están desplegados más de un repositorio,
tenemos que realizar ciertos ajustes para poder usar diferentes claves
públicas.

Esto es así porque, por política de _GitHub_, necesitamos definir una clave
pública diferente como clave de despliegue para cada repositorio.  En otras
palabras, hay que tener **una clave de despliegue por cada repositorio**, no se
pueden compartir las claves entre repositorios.

Si el proyecto ya existe, y tiene asignada una clave pública como clave de
despliegue, hay que obtener la parte privada de la clave y guardarla en el
servidor con un nombre distintivo. En el ejemplo del servidor `cronos`, tenemos
que conseguir los ficheros `~/.ssh/id_rsa_cronos` y
`~/.ssh/id_rsa_cronos.pub` (Se sugiere simplemente añadir el nombre del
servidor como sufijo, como en el ejemplo)

Si es una proyecto nuevo, que vamos a desplegar por primera vez, o si no
podemos conseguir la parte privada por la razón que sea, lo primero será
generar una nueva pareja de claves pública/privada. Podemos generar una pareja
de claves con el comando `ssh-keygen`.

Una vez generada la pareja de claves, lo siguiente es asignar la parte pública
como clave de despliegue al repositorio. Esto lo hacemos desde la página web de
_GitHub_ del repositorio, pulsando en ⚙ `settings`, luego la sección _deploy
Keys_, y añadimos la clave pública (En este ejemplo, el contenido del fichero
`~/.ssh/id_rsa_cronos_public`, con un título. Se sugiere indicar el título el
nombre del servidor en que se usará para desplegar, por ejemplo `"Clave
despliegue Cronos"`.

Eso no nos dará mucho problema si un servidor solo necesita acceso a este
repositorio, pero si necesita acceder a más, como en el caso de Cronos, ya no
puede confiar en usar simplemente la clave pública por defecto (normalmente
`~/.ssh/id_rsa.pub`, sino que **hay que indicar en cada repositorio que clave
pública debe usar**.

Para ello, debemos **crear o editar** el fichero de configuración de _ssh_
(normalmente `~/.ssh/config`), y asignar un **alias diferente para cada
repositorio**. Por ejemplo, para Cronos, el fichero que hemos puesto es:

```
Host github.com-parcanweb
        Hostname github.com
        AddKeysToAgent yes
        IdentityFile ~/.ssh/id_rsa

Host github.com-cronos
        Hostname github.com
        AddKeysToAgent yes
        IdentityFile ~/.ssh/id_rsa_cronos
```

!!! note "Para que sirven estos alias?"

    Como vemos, las entradas apuntan al mismo servidor, `github.com`, pero el
    alias nos permite, al usarlo en el repositorio en vez de `github.com`,
    asociar la clave privada con el repositorio. si la parte púíblica de la
    clave está dada de alta como clave de despliegue del erpositorio, se
    permitirá el despliegue.

Ahora, una última observación, si hemos desplegado normalmente, seguramente lo
hicimos desde `github.com`, lo que significa que todavía **no estaríamos usando
los alias**, así que se seguirá intentando autentificar con la clave pública
por defecto `~/.shh/id_rsa.pub`. 

Si desplegaste desde el alias, olvídate de lo que sigue, pero en caso contrario, nos
quedan una o dos cosas por hacer:

1.- Configurar la configuración en el repositorio.

Para asignar el origen usando el alias `github.com-cronos`.
Para ello editamos, situados en la carpeta del proyecto, el fichero
  `.git/config`, y modificamos la entrada `origin` para cambiarla de:

```
[remote "origin"]
      url = git@github.com:parlamentodecanarias/CKAN.git
      fetch = +refs/heads/*:refs/remotes/origin/*
```

a:

```
[remote "origin"]
      url = git@github.com-cronos:parlamentodecanarias/CKAN.git
      fetch = +refs/heads/*:refs/remotes/origin/*
```

2.- Opcionalmente, puede que haga falta reiniciar el demonio `ssh` para que lea 
de nuevo la configuración del fichero `~/.ssh/config` y entienda los alias:

```shell
sudo systemctl restart ssh.service
```

