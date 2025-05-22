---
title: Notas sobre OpenData, transparencia, etc.
tags:
    - opendata
    - transparencia
    - api
---

## Términos

### RDF

**[RDF](http://www.w3.org/RDF/)** (_Resource Description Framework_) es un
modelo estándar para el intercambio de datos en la Web. El objetivo es
describir la semántica de los datos para ser procesables por máquinas. Entre
sus características se encuentran la posibilidad de la fusión de datos basados
en esquemas diferentes y permitir la evolución de dichos esquemas sin necesidad
de hacer cambio en los sistemas que hacen uso de estos datos.

Este estándar se base en la estrategia de enlazado de la Web basado en URIs
(Uniform Resource Identifier), y extiende esta estrategia de nombrado para
describir relaciones entre entidades o cosas, las cuales vienen identificadas
de igual manera por una URI. El componente producido por dicha relación es
conocido como **tripleta** y está formado por un **Sujeto**, un **Predicado** y un **Objeto**.

El conjunto de estructuras de este tipo forman grafos RDF, y el conjunto de dichos
grafos conforman un RDF Dataset, que puede ser consultado utilizando el lenguaje
SPARQL.

### SPARQL

**[SPARQL](https://es.wikipedia.org/wiki/SPARQL)** es un acrónimo recursivo del
inglés _SPARQL Protocol and RDF Query Language_. Se trata de un lenguaje
estandarizado para la consulta de grafos RDF, normalizado por el _RDF Data
Access Working Group_ (DAWG) del _World Wide Web Consortium_ (W3C). Es una
tecnología clave en el desarrollo de la web semántica que se constituyó como
recomendación oficial del W3C el 15 de enero de 2008.

Al igual que sucede con SQL, es necesario distinguir entre el lenguaje de
consulta y el motor para el almacenamiento y recuperación de los datos. Por
este motivo, existen múltiples implementaciones de SPARQL, generalmente ligados
a entornos de desarrollo y plataforma tecnológicas.

En un principio SPARQL únicamente incorpora funciones para la recuperación
sentencias RDF. Sin embargo, algunas propuestas también incluyen operaciones
para el mantenimiento (creación, modificación y borrado) de datos. 
