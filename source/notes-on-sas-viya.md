---
title: Notas sobre SAS Viya
tags:
    - stats
    - api
    - ia
---

# Notas sobre SAS Viya

## ¿Qué es SAS Viya?

**SAS Viya** es una plataforma de anælisis, gestión de datos e
inteligencia artificical desarrollado por [SAS Institute]().

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
