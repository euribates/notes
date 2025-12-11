---
title: Notas sobre SAS Viya
tags:
    - statistics
    - api
    - ia
---

# Notas sobre SAS Viya

## ¿Qué es SAS Viya?

**SAS Viya** es una plataforma de análisis, gestión de datos e
inteligencia artificial desarrollado por [SAS Institute]().

## Cómo listar los grupos de usuarios

```
$ sudo sas-viya identities list-groups
```


## Cómo ver los detalles de un grupo

```
$ sudo sas-viya identities show-group --id <id. del grupo>
```


## Cómo listar los usuarios

```
$ sudo sas-viya identities list-users
```

## Cómo ver los detalles de un usuario

```
$ sudo sas-viya identities show-user --id <username>
```

## ¿Qué es un CASLIB?

Una **CASLIB** es una biblioteca que puede contener cero o más tablas
CAS.

Una CASLIB está asociado a una fuente de datos desde la cual el servidor
puede acceder a los datos. Proporciona información de conexión a la
fuente de datos, y tiene controles de acceso asociados que definen qué
grupos y usuarios individuales pueden usar el CASLIB.

La arquitectura del servidor añade automáticamente las CASlibs
personales. Además, cada usuario autenticado tiene dos CASlibs: una para
su directorio personal (`CASUSER`) y otra para el  directorio
`/user/userid`  en HDFS (CASUSERHDFS), si se trata de un CAS
distribuido. 

## Qué nodos de SAS-Viya necesitan acceso a las servidores de bases de datos

Desde los servidores **Compute**, **CAS Controller**, y **CAS Workers**. Esta
conectividad ya está pedida dado que las Caslibs ya están creadas y validadas
su acceso a las fuentes de datos correspondientes. 

## Cómo saber que `plugins` tiene instalados el cliente de SAS-Viya

Con el comando:

```shell
$ sudo sas-viya plugins list
```

## Cómo vincular un grupo Unix local a un grupo de usuarios en SAS-Viya

Necesitamos usar el comando `update-group` del _plugin_ `identities`.
Por ejemplo para vincular el grupo local $2005$ con el grupo de SAS-Viya
`CAPJS-DGTNT-HiperReg-D`, el comando sería:

```shell
sudo sas-viya --output text identities update-group --id "CAPJS-DGTNT-HiperReg-D" --gid 2005
```

## Cómo listar los grupos de usuarios creados en SAS-Viya

Con `sas-cli` podemos listar los grupos de usuarios, (necesitamos tener
instalado el `plugin` `identities`):

```shell
$ sudo ./sas-viya --output text identities list-groups
```

El _flag_ ``--after`` puede ser de utilidad, solo lista los grupos creados
a partir de una determinada fecha. La fecha tiene que ir en formato
[ISO-8601](https://es.wikipedia.org/wiki/ISO_8601), es decir, por
ejemplo `2025-10-27T13:00:00Z` para indicar el 27 de octubre de 2025, a
partir de la una de la tarde.

```shell
$ sudo ./sas-viya --output text identities list-groups --after 2025-10-27T13:00:00Z
```

## Relación de máquinas respectivamente en PRE y EXP: 

PIAD - PRE 

    Stateful 1
    Stateful 2
    Stateless
    Compute
    CAS Controller
    CAS Worker 1
    CAS Worker2
    Bastion host

PIAD - EXP

    Stateful 1
    Stateful 2
    Stateful 3
    Stateless1
    Stateless2
    Compute1
    Compute2
    CAS Controller1
    CAS Controller2
    CAS Worker 1
    CAS Worker 2
    CAS Worker 3
    CAS Worker 4
    CAS Worker 5
    Bastion host
