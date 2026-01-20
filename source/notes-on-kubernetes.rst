Kubernetes
========================================================================

tags: docker, kubernetes, dev-ops


Qué es :index:`Kubernetes`
------------------------------------------------------------------------

**Kubernetes** es una plataforma *open source* para la organización de
contenedores que automatiza muchos de los procesos manuales involucrados
en la implementación, la gestión y el ajuste de las aplicaciones que se
alojan allí.

Además, automatiza la configuración de sus aplicaciones, mantiene y
supervisa la asignación de recursos. Desarrollado inicialmente por
Google, ahora Es un proyecto de la fundación `Cloud Native Computing
Foundation (CNCF)`_.

Se presentó por primera vez en 2014 y que adquirió una gran popularidad
entre las empresas como plataforma para ejecutar aplicaciones y
servicios distribuidos según sea necesario.

¿Cuál es la arquitectura mínima de un sistema Kubernetes?
------------------------------------------------------------------------

Para un sistema mínimo, se necesita:

-  Un nodo maestro

-  Un nodo trabajador o *worker* (Normalmente habrá más de uno)

-  Al menos un *pod*, que es una agrupación de uno o más contenedores.

Es interesante hacer notar que todos los contenedores dentro de un *pod*
comparten la misma dirección IP y puertos, los mismos volúmenes
compartidos y generalmente se pueden considerar como una pequeña máquina
virtual compuesta de muchos servicios y que está compuesta por los
diferentes contenedores corriendo en paralelo.

En Kubernetes, los nodos (que pueden ser máquinas físicas o máquinas
virtuales) contienen *pods*, y los *pods* contienen contenedores. Los
contenedores son máquinas, ya sea físicas o virtuales.

Los contenedores dentro de un *pod* pueden comunicarse entre si usando
cualquier sistema de comunicación entre procesos (IPC, *Interprocess
Communication*), como semáforos, memoria compartida o volúmenes de
almacenamiento de ficheros temporales, que existen en tanto en cuando
exista el *pod*. Todos los contenedores dentro del *pod* comparten con
él el ciclo de vida: se crean junto con el *pod* y se destruyen cuando
se destruye el *pod*. El objetivo es reducir el coste de conexiones,
manteniendo cerca a los contenedores que están interrelacionados.

Cómo funciona un sistema de orquestación
------------------------------------------------------------------------

Antes de los sistemas de orquestación, como Kubernetes, desplegar
*software* a una cierta escala se realizaba más o menos de la siguiente
manera:

- Conectar vía SSH al servidor 1
- Obtener la última versión del *software*
- Instalar dependencias
- (Re) Iniciar la aplicación
- Repetir para los servidores [1..n]
- Rezar para que nada casque a las 3 de la mañana

Este es un sistema de gestión **imperativo**, en el que se le dice a
cada máquina que tiene que hacer, paso a paso. Funciona bien con pocas
máquinas, pero no escala bien, es mas proclive a errores y cuando algo
falla, tú eres la última línea de defensa.

Con Kubernetes, el modelo cambia: en vez de especificar **cómo**
realizar el despliegue, se especifica **el estado final que deseamos
tener**. La siguiente configuración de Kubernetes:

.. code:: yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: my-app
    spec:
      replicas: 3


Especifica que queremos tres copias de la aplicación ejecutándose.
Kubernetes hace el resto: Decide qué máquinas usar, como distribuir la
carga, e incluso qué hacer ante una caída de sistemas.

Este enfoque es **infraestructura declarativa**. Se define el estado
final deseado, y el sistema trabaja constantemente para que la realidad
coincida con dicho estado. Este supervisión constante se conoce como el
**bucle de control** de Kubernetes (*Kunbernetes Control Loop*).

-  Fuente: `What on earth is Kubernetes?`_


Qué es un contenedor / imagen docker
------------------------------------

Antes de Kubernetes, tenemos que entender Docker. Un
**{index}\ ``contenedor Docker``** en una unidad auto-contenido y ligera
de ejecución de un determinado *software*. Es auto-contenida porque
incluye todo lo que pueda necesitar para ser ejecutada: Código,
dependencias, librerías, recursos, etc.

Hay que distinguir entre contenedor e imagen. Una
**{index}\ ``imagen Docker``** es el fichero que contiene nuestro
*software*, mientras que el **contenedor** es una instancia en ejecución
de una determinada imagen. La diferencia es equivalente a la del fichero
que contiene el programa con respecto al proceso que lo ejecuta.

Normalmente la imagen se construye una vez, incluyendo la aplicación y
todas sus dependencias, se sube a un repositorio de imágenes, y luego se
ejecutan tantos contenedores como se quiera y donde se desee.

Podemos listar las imágenes que tenemos en el sistema con:

.. code:: shell

    docker images

Y listar los contenedores en ejecución con:

.. code:: shell

    docker ps

Para listar todos los contenedores, estén ejecutándose o no:

.. code:: shell

    docker ps --all

Esto puede ser muy importante, ya que los contenedores que no se están
ejecutando siguen ocupando espacio en disco.

Qué es un pod en Kubernetes
------------------------------------------------------------------------

Un **{index}\ ``Pod``** es la mínima unidad de despliegue de Docker. Es
una envoltura alrededor de uno o más contenedores, que comparten
recursos de almacenamiento y de red.

Casi siempre un *pod* contiene un único contenedor, pero a veces se
configura con un contenedor principal y otros de apoyo: Un agente de
*logging*, un *proxy*, un servicio de caché, etc. Todos los contenedores
que están dentro de un mismo Pod pueden conectarse entre si usando
``localhost`` y comparten los sistemas de archivos montados.

Podemos pensar en un Pod como un apartamento compartido: Los contenedores
son los habitantes, que comparten la cocina y el salón, pero cada uno de
ellos tiene su propio dormitorio.

Un ejemplo de descripción de un Pod podría ser el siguiente:

.. code:: yaml

    apiVersion: v1
    kind: Pod
    metadata:
      name: my-pod
    spec:
      containers:
      - name: app
        image: nginx:1.14.2
        ports:
        - containerPort: 80
      # Second container
      - name: sidecar
        image: fluent/fluent-bit

Cómo escala Kubernetes. Qué es el plano de control
========================================================================

Para poder escalar, Kubernetes añade nuevos *pods* a su clúster.  Los
*pods* se ejecutan en el hardware subyacente, que a su vez se puede
escalar añadiendo nuevos nodos al clúster. La parte del clúster de
Kubernetes que administra y facilita la orquestación de los *pods* se
denomina **plano de control**.


El cliente de kubernetes
------------------------------------------------------------------------

El cliente oficial de Kubernetes es {index}\ ``kubectl``, una utilidad
de línea de comandos que interactúa con la API de Kubernetes. Con
``kubectl`` se puede gestionar la mayoría de los componentes de
Kubernetes, como *pods*, *replicasets*, servicios, etc. También se puede
usar para comprobar y verificar la estabilidad y el estado del cluster.

Podemos comprobar si tenemos instalado el cliente con:

.. code:: shell

    kubectl version


Cómo listar los nodos contenidos en un cluster de Kubernetes
------------------------------------------------------------------------

Con ``kubeclt get nodes``.

En Kubernetes, los nodos se separan en roles. En ``control-plane`` están
los nodos que contienen los sistemas de gestión como el servicio de API,
el *scheculer*, etc. Los nodos de tipo *worker* son los que realizan el
trabajo real. La idea es mantener los nodos en el ``control-plane`` no


.. _What on earth is Kubernetes?: https://kylejeong.com/blog/what-is-kubernetes
.. _Cloud Native Computing Foundation (CNCF): https://www.cncf.io/
se vean afectados por la carga de trabajo.
