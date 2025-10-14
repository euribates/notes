---
title: Notas sobre CKAN
tags:
    - opendata
    - free-software
    - python
---

## Qué es CKAN?


**CKAN** es una herramienta para crear sitios web de datos abiertos.
Como un gestor de contenidos, del estilo de _Wordpress_, pero 
para datos. En vez de páginas, publica colecciones de datos.

Una vez que los datos han sido publicados, los usuarios pueden realizar
búsquedas segmentadas para navegar y localizar los datos que necesitan,
y previsualiarlos usando mapas, gráficos y tablas.

En CKAN, los datos se publican en unidades llamadas __datasets__.


## Qué es un DataSet

Un **dataset** es un conjunto de datos, por ejemplo, puede ser uanas
estadísticas de crímenes acumulados por región, los gastos de un
departamento gubernamental, o las lecturas de temperatura de diferentes
estaciones meteorológicas. Los resultados de lasd búsquedas de un
usuario siempre son _datasets_.

Un _dataset_ consta de dos partes:

- Los **Metadatos**, es decir, la información acerca de los datos.
  Ejemplos pueden ser el autor, la fecha, el formato o formatos en los
  que están disponibles los datos, la licencia que regula su uso, etc.

- Un número de **recursos** (_resources_) que contiene los datos en si.
  A CKAN no le importa demasiado el formato que se haya usado, un
  recurso puede ser un fichero CSV, una hoja de cálculo, un fichero XML,
  un documento PDF, un aimagen, datos enlazados en [formato
  RDF](https://es.wikipedia.org/wiki/Resource_Description_Framework),
  etc. CKAN puede almacenar los datos localmente, o solo guardar el
  enlace a los mismos, residiendo los datos, por tanto, en otro sitio.

  Un _dataset_ puede contener un número arbitrario de recursos. Por
  ejemplo, puede usar diferentes recursos para segmentar los datos por
  año, o pueden usarse también para almacenar los mismo datos, pero en
  diferentes formatos.

    Nota: En versiones anteriores, los _datasets_ eran llamados
    "packages", y ese nombre todavía puede encontrse en algunas partes,
    como en la documentación, llamadas --especialmente internas--  de la
    API. Hay que considerarlos como sinónimos.


## Usuario, organización y autorización

CKAN users can register user accounts and log in. Normally (depending on the site setup), login is not needed to search for and find data, but is needed for all publishing functions: datasets can be created, edited, etc by users with the appropriate permissions.

Normally, each dataset is owned by an “organization”. A CKAN instance can have any number of organizations. For example, if CKAN is being used as a data portal by a national government, the organizations might be different government departments, each of which publishes data. Each organization can have its own workflow and authorizations, allowing it to manage its own publishing process.

An organization’s administrators can add individual users to it, with different roles depending on the level of authorization needed. A user in an organization can create a dataset owned by that organization. In the default setup, this dataset is initially private, and visible only to other users in the same organization. When it is ready for publication, it can be published at the press of a button. This may require a higher authorization level within the organization.

Datasets cannot normally be created except within organizations. It is possible, however, to set up CKAN to allow datasets not owned by any organization. Such datasets can be edited by any logged-in user, creating the possibility of a wiki-like datahub.

Note

The user guide covers all the main features of the web user interface (UI). In practice, depending on how the site is configured, some of these functions may be slightly different or unavailable. For example, in an official CKAN instance in a production setting, the site administrator will probably have made it impossible for users to create new organizations via the UI. You can try out all the features described at http://demo.ckan.org.

