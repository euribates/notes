---
title: Notas sobre SAS Viya
tags:
    - stats
    - api
    - ia
---

# Notas sobre SAS Viya

## ¿Qué es SAS Viya?

**SAS Viya** es una plataforma de anælisis, gestión de datos
e inteligencia artificical desarrollado por 
[SAS Institute]().

## ¿Qué es un CASLIB?

Una **CASLIB** es una biblioteca que puede contener cero o más tablas CAS.

Una CASLIB está asociado a una fuente de datos desde la cual el servidor
puede acceder a los datos. Proporciona información de conexión a la
fuente de datos, y tiene controles de acceso asociados que definen qué
grupos y usuarios individuales pueden usar el CASLIB.

La arquitectura del servidor añade automáticamente las CASlibs
personales. Además, cada usuario autenticado tiene dos CASlibs: una para
su directorio personal (`CASUSER`) y otra para el  directorio
`/user/userid`  en HDFS (CASUSERHDFS), si se trata de un CAS
distribuido. 


## Servidores de SAS en G.C.

https://cmm.gobiernodecanarias.net/ (Producción)
https://cmm-pre.gobiernodecanarias.net/ (Pre)

Todos los datos deberían leerse desde el _Data-lake_, pero en la práctica
no ocurre así, sino que se va a saco a la fuente. La idea es que en la versión 4
no pase eso.

La idea seria hacer ETL de tipo identidad, para que cojan los datos en origen
y creen las réplicas en el _data lake_.

