---
title: Notas sobre Caches y arquitectura de sistemas
tags:
    - linux
    - development
    - devops
---

## Sobre el concepto de caché

Una técnica de desarrollo de software orientada a conseguir un acceso más rápido
a los datos, reducir tiempos de espera y mejorar la experiencia de usuario.

## Tipos de Caché

- Caché en el lado del cliente

- Caché en en CDN

- Caché a nivel de aplicación (Por ejemplo, Redis)

- Caché en el nivel de base de datos

- Caché distribuida

El parámetro más importante para diseñar un sistema de caché es
definir que datos vamos a cachear, y para ello tenemos que tener en
cuenta las **patrones de uso**, la **volatibilidad de los datos**
y la **frecuencia de acceso**.

Otro parámetro importante es la **política de descarte** (_cache 
eviction policy_), como por ejemplo LRU (_Least Recently Used_) o TTL
(_Time-to-Live). Mediante estas políticas no aseguramos de que la información
almacenada en la caché es purgada en algún momento, manteniendo así
la relevancia de los datos cacheados.

## Conceptos básicos sobre Caché

### Politicas de descarte o refresco de la caché

Existen diversas estrategias de descarte, entre las más conocidas tenemos:

- **LRU**: (_Least recently Used_) A la hora de descartar una entrada, elimina
  la que se ha utilizado por última vez hace más tiempo, es decir, a la menos
  recientemente usada.

- **MRU**: (_More Recently Used_) A la hora de descartar una entrada, elimina la
  que se ha utilizado por última vez hace menos tiempo, es decir, la más
  recientemente usada. Esta estrategia es muy eficiente si sabemos, ya sea por
  el diseño del sistema o por algún tipo de heurística, que una vez accedido
  al recurso es muy poco probable que se vaya a solitar otra vez.

- **LFU**: (_Least Frequently Used_) Elimina la entrada que se haya usado menos
  veces.

### Jerarquía de caché

Se puede organizar un sistema de caché por niveles (Por ejemplo, L1, L2, etc.)
para obtener un equilibrio entre velocidad y capadidad de almacenaje. Este
sistema es muy utilizado en el diseñó de CPUs.

### Invalidación de caché

Las entradas en la caché se pueden invalidar cuando sabemos que los datos
almacenados ya no son válidos, forzando así al sistema a cargar eventualmente
la nueva información. Algunos de los métodos más usados para esto son:

- **Time-to-Live (TTL)**: Define una fecha de expiración para los datos en la
  caché. Podemos ajustar este valor a un tiempo pasado para invalidar la caché,

- **Event-based Invalidation**: Dispara un evento de invalidación ante determinados
  sucesos o condiciones.
    
- **Manual Invalidation**: Permite a los desarrolladores o a los técnicos de
  sistemas actualizar manualmente la caché.

### Patrones de sincronización

SOn estrategias usados para sincronizar el estado de la caché con
el de la base de datos. Algunos de los patrones más usados son:

- **Write-through**: Escribe los datos de forma simultanea en la base de datos y
  en la caché.

- **Write-behind**: Escribe primero y de forma inmediata
  los datos en la caché y luego, de forma asíncrona,
  escribe los datos en la base de datos.

- **Write-around**: Escribe primero y de forma inmediata
  los datos en la base de datos y luego, de forma asíncrona,
  escribe los datos en la base de datos.


## Recursos para aprender sobre diseño de caché

- [System Design Basics - Caching - DEV Community](https://dev.to/somadevtoo/system-design-basics-caching-4fge)

- [Design Gurus - One-Stop Portal For Tech Interviews](https://bit.ly/3pMiO8g): An interactive learning platform with hands-on exercises and real-world scenarios to strengthen your system design skills.

- [Codemia | Master System Design Interviews Through Active Practice](https://codemia.io/)


- [GitHub - donnemartin/system-design-primer: Learn how to design large-scale systems. Prep for the system design interview.  Includes Anki flashcards.](https://bit.ly/3bSaBfC)


