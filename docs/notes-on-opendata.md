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

**[SPARQL](https://es.wikipedia.org/wiki/SPARQL)** es un acrónimo
recursivo del inglés _SPARQL Protocol and RDF Query Language_. Se trata
de un lenguaje estandarizado para la consulta de grafos RDF, normalizado
por el _RDF Data Access Working Group_ (DAWG) del _World Wide Web
Consortium_ (W3C). Es una tecnología clave en el desarrollo de la web
semántica que se constituyó como recomendación oficial del W3C el 15 de
enero de 2008.

Al igual que sucede con SQL, es necesario distinguir entre el lenguaje
de consulta y el motor para el almacenamiento y recuperación de los
datos. Por este motivo, existen múltiples implementaciones de SPARQL,
generalmente ligados a entornos de desarrollo y plataforma tecnológicas.

En un principio SPARQL únicamente incorpora funciones para la
recuperación sentencias RDF. Sin embargo, algunas propuestas también
incluyen operaciones para el mantenimiento (creación, modificación y
borrado) de datos. 

### Seudoanonimización

**Seudonimización** es un procedimiento de gestión de datos donde se
reemplazan campos de información personal dentro de un registro de datos
por uno o más identificadores artificiales o pseudónimos. Un pseudónimo
único por cada campo reemplazado, o grupo de campos reemplazados, hace
cada registro de datos menos identificable mientras se queda apto para
análisis de datos y procesamiento de datos. 

### RGPD

El **RGPD** o **Reglamento General de Protección de Datos** (RGPD) o
Reglamento (UE) 2016/679, es una ley comunitaria relativa a la
protección de las personas físicas (independientemente de si son
ciudadanos de la Unión) en lo que respecta al tratamiento de sus datos
personales y a la libre circulación de estos datos en la Unión Europea y
el Espacio Económico Europeo (EEE).

El RGPD es un componente importante de la legislación europea sobre
privacidad y de la legislación sobre derechos civiles, en particular el
artículo 8, apartado 1, de la Carta de los Derechos Fundamentales de la
Unión Europea. También delimita la transferencia de datos personales
fuera de la UE y de las zonas del EEE. 

Como el RGPD es un Reglamento, no una Directiva, es directamente
vinculante y aplicable, no ofrece flexibilidad para que los Estados
miembros ajusten determinados aspectos de la Ley.

### OWL

**OWL** (_Web Ontology Language_) es un lenguaje de la Web Semántica
avalado por el [W3C](https://www.w3.org/), diseñado para representar
conocimiento exhaustivo y completo sobre entidades, grupos de entidades
y las relaciones que puede haber entre ellas.
