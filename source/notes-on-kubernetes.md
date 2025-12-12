---
title: Notas sobre kubenetes
tags:
    - virtualization
    - os
    - API
    - backend
    - cloud
    - devops
    - docker
---

## Qué es kubernetes

**Kubernetes** es una plataforma *open source* para la organización de
contenedores que automatiza muchos de los procesos manuales involucrados
en la implementación, la gestión y el ajuste de las aplicaciones que se
alojan allí.

Además, automatiza la configuración de sus aplicaciones, mantiene y
supervisa la asignación de recursos. Desarrollado inicialmente por
Google, ahora Es un proyecto de la fundación [Cloud Native Computing
Foundation (CNCF)](https://www.cncf.io/).

Se presentó por primera vez en 2014 y que adquirió una gran popularidad
entre las empresas como plataforma para ejecutar aplicaciones y
servicios distribuidos según sea necesario.

## ¿Cuál es la arquitectura mínima de un sistema Kubernetes?

Para un sistema mínimo, se necesita:

- Un nodo maestro

- Un nodo trabajador o _worker_ (Normalmente habrá más de uno)

- Al menos un *pod*, que es una agrupación de uno o más contenedores.

Es interesante hacer notar que todos los contenedores dentro de un *pod*
comparten la misma dirección IP y puertos, los mismos volúmenes
compartidos y generalmente se pueden considerar como una pequeña máquina
virtual compuesta de muchos servicios y que está compuesta por los
diferentes contenedores corriendo en paralelo.

En Kubernetes, los nodos (que pueden ser máquinas físicas o máquinas
virtuales) contienen *Pods*, y los *Pods* contiene contenedores.

Los contenedores dentro de un *pod* pueden comunicarse entre si usando
cualquier sistema de comunicación entre procesos (IPC, *Interprocess
Communication*), como semáforos, memoria compartida o volúmenes de
almacenamiento de ficheros temporales, que existen en tanto en cuando
exista el *pod*. Todos los contenedores dentro del *pod* comparten con
él el ciclo de vida: se crean junto con el *pod* y se destruyen cuando
se destruye el *pod*. El objetivo es reducir el coste de conexiones,
manteniendo cerca a los contenedores que están interrelacionados.

## El cliente de kubernetes

El cliente oficial de Kubernetes es `kubectl`, una utilidad de línea de
comandos que interactúa con la API de Kubernetes. Con `kubectl` se
puede gestionar la mayoría de los componentes de Kubernetes, como
*pods*, *replicasets*, servicios, etc. También se puede usar para
comprobar y verificar la estabilidad y el estado del cluster.

Podemos comprobar si tenemos instalado el cliente con:

```shell
kubectl version
```

## Cómo listar los nodos contenidos en un cluster de Kubernetes

Con `kubeclt get nodes`.

En Kubernetes, los nodos se separan en roles. En `control-plane` están
los nodos que contienen los sistemas de gestión como el servicio de API,
el *scheculer*, etc. Los nodos de tipo *worker* son los que realizan el
trabajo real. La idea es mantener los nodos en el `control-plane` no se
vean afectados por la carga de trabajo.


