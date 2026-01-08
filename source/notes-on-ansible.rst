Ansible
=======

¿Qué es :index:`Ansible`?
------------------------------------------------------------------------

**Ansible** es un motor de automatización, de código abierto, usado para
**gestión de configuración**, despliegue de aplicaciones, orquestación y
otros procesos habituales de sistemas informáticos. Se sitúa en la misma
categoría que otras herramientas como `Puppet`_, `Chef`_ o `Salt`_. Es
software libre.

Gestor de configuración se entiende generalmente como sistemas que nos
permiten escribir una descripción del estado en que queremos que estén
nuestro servidores, y luego, mediante las herramientas del sistema,
asegurar que los servidores están, efectivamente, en dicho estado.

El nombre lo puso Michael DeHaan, su creador, por el sistema de
comunicación instantáneo del hiper espacio imaginado por Orson Scott
Card en la novela `El juego de Ender`_ y originalmente inventado
por `Ursula K.  LeGuin`_ en su novela de 1966 `El mundo de Rocannon`_.


Características de Ansible
------------------------------------------------------------------------

-  Define un **lenguaje de uso específico** (DSL) para describir el
   estado de los servidores

-  **No usa agentes**: Chef o Puppet son sistemas de gestión de
   configuración que trabajan con agentes. Usan por defecto una
   estrategia basada en ``pull`` o solicitudes. Los agentes instalados
   en las máquinas destino consultan de forma periódica a servicio
   central, para ver si hay cambios en la configuración. En ese caso,
   descargan y aplican la nueva configuración. Por el contrario Ansible
   usa una estrategia basada en ``Push``. Hay ventajas e inconvenientes
   en ambas estrategias.

-  **Sistema de plug ins**: Ansible se estructura sobre un sistema de
   *plug ins*, de los cuales ``Lookup`` y ``Filter`` son los más usados.
   Con este sistema, Ansible puede aumentar su funcionalidad básica con
   lógica y capacidades que pueden ser usadas por todos los módulos.

-  Los módulos son **idempotentes**. Se pueden ejecutar varias veces sin
   problema.

-  **No** es la clase de herramienta que *automágicamente* toma
   decisiones o realiza acciones por ti.

Instalar Ansible
------------------------------------------------------------------------

Con pip:

.. code:: shell

   pip install ansible

Dependiendo de los *plug ins* que usemos, puede que tengamos que
instalar algunos paquetes adicionales. Por ejemplo, si queremos
interactuar con máquina windows hay que instalar ``pywinrm``. Si
trabajamos con Docker, necesitamos ``docker``:

.. code:: shell

   pip install docker pywinrm

Conceptos de Ansible
------------------------------------------------------------------------

-  **Inventario** (*Inventory*): Catálogo de máquinas destino sobre los
   que podemos actuar. Fichero con extensión ``.ini``, pero en formato
   ```yaml`` <http://yaml.org/>`__.

-  **Variables** (*Variables*): Valores definidos por Ansible y
   disponibles en módulos y ``playbooks``.

-  **Guias** o (*Playooks*): Descripción secuencial de tareas. En
   formato ``yaml``. Llaman a los módulos.

-  **Plantillas** (*Templates*): Generación dinámica de ficheros. En
   formato ``Jinja2``. Tienen acceso a las variables definidas en tiempo
   de ejecución de los *playbooks*. Lógica simple con sentencias de
   control como ``if``, ``else``, ``for`` y variables.

-  **Extensiones** (*Plug-ins*): Extienden las capacidades básicas de
   Ansible. Se escriben en Python. Posibilidad de escribir nuestros
   propios ``plug-ins``.

-  **Módulos** (*Modules*): Se pueden escribir en Python y en
   Powershell. Los fabricantes suelen proporcionar sus propios módulos
   específicos para comunicarse con sus dispositivos.

Como obtener información de Ansible desde la línea de comando
------------------------------------------------------------------------

Una vez instalado, podemos usar el comando ``ansible-doc`` para ver la
documentación oficial y consultar aspectos de la configuración,
inventario, etc.

.. code:: shell

   ansible-doc

Cómo funcional el inventario con Ansible
------------------------------------------------------------------------

Hay varias formas de definir el inventario en Ansible; la más sencilla
es usar un fichero de texto ``.ini``. La tradición es usar un directorio
``inventory`` para almacenar el fichero. Es posible usar un inventario
dinámico, pero no veremos esas opciones aquí. Aunque el fichero tiene la
extensión ``.ini``, **no** es un fichero ``.ini`` del tipo usado en
Windows, es un fichero ``yaml``.

El inventario consiste en máquinas, agrupadas en grupos. Podemos acceder
después a estos datos usando las variables predefinidas ``group_vars`` y
``host_vars``.

Si no se especifica, Ansible usa ``/etc/ansible/hosts`` como
localización por defecto del fichero de inventario. Normalmente se
recomienda usar un directorio de inventario propio, en el mismo sitio
donde tengamos definidos nuestros *playbooks*. Esto permite mantener un
inventario específico para cada proyecto, en vez de tener un inventario
global.

Módulos en Ansible
------------------------------------------------------------------------

-  ``ping``

El módulo **``ping``** no hace nada más que comprobar que Ansible puede
iniciar una sesión SSH con los servidores destino. Es una herramienta
para probar la conectividad con los servidores. Resulta muy útil al
principio de un *playbook* si este es muy grande.

-  ``command``

El módulo **``command``** nos permite ejecutar un comando de forma
remota en las máquinas destino. Es tan usada que es el módulo por
defecto, es decir, si no se especifica ningún módulo, se ejecuta
``command``, así que podemos omitirlo.

Si necesitas acceso privilegiado, se puede usar el *flag* ``-b`` o
``--become`` para indicarle a Ansible que debe ejecutar el comando como
dicho usuario (normalmente, ``root``).

-  ``package``

La orden ``package`` sirve para garantizar que un determinado paquete
está instalado en las máquinas destino. Por ejemplo, para garantizar que
``nginx`` está instalado:

.. code:: shell

   ansible testserver -b -m package -a name=nginx

Si la instalación de ``nginx`` fallara, puede que tengamos que
actualizar la lista de paquetes. Para forzar a las máquinas destino que
hagan el equivalente a un ``apt-get update`` antes de intentar instalar
el paquete, podemos cambiar el valor del parámetro ``-a`` de ``nginx`` a
``nginx unpate_cache = yes``.

-  ``service``

Con el módulo **``service``** podemos interactuar con los servicios de
las máquinas destino. Por ejemplo, podemos forzar un reinicio del
servicio ``nginx`` con:

.. code:: shell

   ansible testserver -b -m service -a "name=nginx state=restarted"

-  ``copy``

El Módulo **``copy``** sirve para copiar ficheros o crearlos mediante
plantillas locales en las máquinas destino. Ansible sigue la convención
de copiar ficheros de un directorio llamado ``files``, y buscar las
plantillas ``jinja2`` en un directorio ``templates``.

-  ``file``

-  ``template``

Configuración de Ansible
------------------------------------------------------------------------

Se configura con un archivo ``ansible.cfg``. Ansible busca un archivo en
los siguientes sitios:

-  Si se ha especificado la variable de entorno ``ANSIBLE_CONFIG``, pues
   ahí

-  ``./ansible.cfg``: en el directorio actual

-  ``~/ansible.cfg``: en el directorio *home* del usuario

-  En ``/etc/ansible/ansible.cgf``

-  En ``/usr/local/etc/ansible/ansible.cfg``

Se recomienda crear una vrsión local para cada proyecto.

Qué son los *playbooks* de Ansible
------------------------------------------------------------------------

Un **``Playbook``** es el nombre que le da Ansible a un *script* de
configuración. Consiste en una lista de diccionarios. Más
específicamente, el *playbook* consiste en una lista de guías o
**``plays``**. No hay ningún problema con que un *playbook* tenga un
único *play*.

Cada guión o ``play`` debe contener una variable ``hosts``, que puede
ser o bien un grupo de los definidos en el inventario, el grupo mágico
``all`` (Todas las máquinas del inventario), o una expresión que defina
el conjunto de maquinas destino a configurar.

Otro campo obligatorio es ``name``, que describe de forma sucinta lo que
hace el guión. Ansible imprime este nombre para indicar en que ha
empezado a trabajar en ese *play*. Se recomienda que los nombres
empiecen con mayúscula.

Si se define una entrada ``become`` con el valor booleano ``true``,
Ansible va a ejecutar con el usuario indicado con ``become_user``.

Modo de prueba o *Check Mode*
------------------------------------------------------------------------

Los *playbooks* de Ansible tienen un modo de prueba en el que los
guiones se prueben si llegar a ser aplicados realmente. La combinación
de la idempotencia de los módulos con el modo de prueba es muy potente.

Los *playbooks* de Ansible muestran los resultados en texto verde,
indicando así que no hay necesidad de aplicar los cambios y que, por
tanto, el sistema está en estado consistente. Si el texto sale en
amarillo, la configuración definida por el playbook y la de los sistemas
objetivo no coincide, indicando por tanto que se van a aplicar los
cambios oportunos.

El sistema para desarrollar un *playbook* seria más o menos como sigue:

-  Hacer los cambios en el código del *playbook*.

-  Ejecutar el *playbook* en modo de prueba activo, y con el parámetro
   ``verbosity`` activo.

-  Confirmar que vemos en la salida el cambio realizado.

-  Ejecutar de nuevo el *playbook*, ahora en modo ejecución.

-  Ejecutarlo de nuevo, ahora otra vez en modo de prueba. Deberíamos
   obtener el texto en verde indicando que no hay necesidad de aplicar
   los cambios.

.. _Chef: https://www.chef.io/
.. _El juego de Ender: https://es.wikipedia.org/wiki/El_juego_de_Ender
.. _El mundo de Rocannon: https://es.wikipedia.org/wiki/El_mundo_de_Rocannon
.. _Puppet: https://www.puppet.com/
.. _Salt: https://saltproject.io/
.. _Ursula K. LeGuin: https://es.wikipedia.org/wiki/Ursula_K._Le_Guin
