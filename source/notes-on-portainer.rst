Portainer
========================================================================

.. labels:: docker, docker-compose,devops
    
.. contents:: Relación de contenidos
    :depth: 3


Sobre Portainer
------------------------------------------------------------------------

**Portainer** es una plataforma de despliegue de
servicios ligera para aplicaciones en contenedores que se puede utilizar
para administrar entornos Docker, Swarm, Kubernetes y ACI. Está diseñado
para ser simple de implementar y de utilizar. La aplicación le permite
gestionar todos sus recursos orquestados (contenedores, imágenes,
volúmenes, redes y más) a través de una interfaz gráfica de usuario y
una API.

Portainer consiste en un solo contenedor que puede ejecutarse en
cualquier clúster.

La versión de pago *Portainer Business Edition* se basa en la base de
código abierto e incluye una gama de características y funciones
avanzadas que son específicas de las necesidades
de usuarios empresariales.


Configurar una red propia para múltiples contenedores.
------------------------------------------------------------------------

Al desplegar nuevos contenedores, a menudo se los deja en la red puente
predeterminada, sin entender lo que eso significaba para la comunicación
entre servicios. Los contenedores en redes separadas no pueden hablar
entre sí a menos que se les puentee explícitamente, lo que causó
problemas de conectividad.

Portainer hace que la creación de redes sea simple, pero las opciones
pueden ser engañosas si no sabes lo que estás viendo. En una
configuración de múltiples contenedores se debe crear una red de puentes
definida por el usuario compartido y adjunté los contenedores a ella.

Vale la pena tomarse unos minutos para configurar una red consistente
como parte de la configuración de mi proyecto.

Otro beneficio es que las redes con nombre persisten a través de pilas y
contenedores. Esto hace que las actualizaciones, se reinicien y
reconstruyan mucho más limpio.

Qué es un *Stack* en Portainer
------------------------------------------------------------------------

Una pila o *Stack* es un grupo de contenedores que trabajan juntos,
generalmente descritos en un archivo ``docker-compose.yml``.

Portainer le da una manera fácil de pegar en un archivo *Compose*,
nombrar la pila, e implementar todo con un solo clic. Este es el método
preferido para ejecutar cualquier cosa más allá de las aplicaciones más
simples.

Portainer leerá el archivo ``docker-compose.yaml`` y creará cada
servicio en consecuencia. Una vez implementado, se verán todos los
contenedores enumerados en esa pila, y pueden administrarse
tanto individualmente o como grupo.

La interfaz de pilas es útil para monitorear y depurar aplicaciones de
contenedores múltiples. Puede ver los registros de cada servicio,
reiniciarlos individualmente e incluso actualizar el archivo Compose más
tarde para realizar cambios. Este flujo de trabajo refleja cómo se
implementan los contenedores en entornos de producción, por lo que
aprenderlo ahora le brinda una ventaja significativa. También hace que
los proyectos complejos se sientan más manejables agrupando los
servicios relacionados.


Uso de plantillas en Portainer
------------------------------------------------------------------------

Una característica que a menudo pasa por alto por los principiantes son
las plantillas de aplicaciones integradas de Portainer. Estos son
contenedores preconfigurados que puede implementar al instante, a menudo
con una entrada mínima requerida.

Encontrarás plantillas para herramientas comunes como WordPress,
Portainer Agent y varias herramientas para desarrolladores. Elegir uno
de estos es una forma rápida de hacer que algo útil funcione mientras
todavía está aprendiendo.

Cada plantilla muestra qué imagen utiliza y qué puertos expondrá. Puede
modificar estos ajustes antes de la implementación si desea más control.
Después de iniciar, el contenedor se comporta como cualquier otro que
haya creado manualmente, por lo que aún puede acceder a registros,
consolas y otras herramientas. Es una excelente manera de realizar
configuraciones de ingeniería inversa inspeccionando cómo se
configuraron.

Las plantillas también son una excelente manera de explorar los casos de
uso que aún no haya considerado. Si tiene curiosidad por alojar un
servidor multimedia, un administrador de contraseñas o un entorno de
desarrollo, probablemente haya una plantilla para ayudarlo a comenzar.
Puede tratarlos como oportunidades de aprendizaje o como herramientas
completamente funcionales para mantener en su *kit* de herramientas
Docker.

