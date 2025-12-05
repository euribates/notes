---
title: Notas sobre Prometheus
tags:
    - scale
    - web
    - logs
    - foss
---

## Notas sobre Prometheus

**[Prometheus](https://prometheus.io/)** es una herramienta de software libre
que permite la monitorización de alertas y eventos generados en el propio
servidor o en otras máquinas. Guarda la información en
una base de datos de series temporales. 


is an open-source tool that allows you to keep tabs on
 different types of rgq}esources including applications running either locally or on some server, and even servers themselves.
With Prometheus, you keep track of various data (metrics) related to your app or server.

## Arquitectura típica de un sistema de monitorización con Prometheus

Un entorno habitual con Prometheus consiste en una serie de herramientas:

- Múltiples *exportadores*, que general métricas.

- Un nodo de Prometheus que centraliza y almacena las métricas

- *AlertManager*, que dispara alertas basándose en los datos de las métricas

- *Grafana* para producir gráficas y paneles de mando.

- *PromQL* es el lenguaje de consulta utilizado tanto para las alertas como para
  los cuadros de mando.

