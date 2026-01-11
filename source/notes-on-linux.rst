Linux
========================================================================

.. tags:: Linux,systemd,ram


Cómo saber cuanta memoria hay en el equipo y de qué tipo
--------------------------------------------------------

El comando a escribir puede variar dependiendo de la distribución, pero
por lo general es:

.. code:: shell

    sudo dmidecode --type memory

El comando devolverá una tabla con toda la información sobre tu memoria
RAM. En **Maximum Capacity** la cantidad exacta de memoria que tienes
instalada, En **Number of devices** el número de módulos de memoria
instalados. Más abajo, en **Type** podrás saber el tipo de memoria que
tienes.

De la documentación de ``dmidecode``:

    dmidecode is a tool for dumping a computer’s DMI (some say SMBIOS)
    table contents in a human-readable format. This table contains a
    description of the system’s hardware components, as well as other
    useful pieces of information such as serial numbers and BIOS
    revision. Thanks to this table, you can retrieve this information
    without having to probe for the actual hardware.

-  Fuente: `Cómo saber cuánta memoria RAM tienes y de qué tipo es, en
Windows, macOS y
GNU/Linux <https://www.xataka.com/basics/como-saber-cuanta-memoria-ram-tienes-que-tipo-windows-macos-gnu-linux>`_

Cómo reiniciar Cinnamon
------------------------------------------------------------------------

Se puede hacer de diversas formas:

-  Presionando ++alt+f2++, tecleamos ``r`` y pulsamos ++enter++.

-  Con la combinación de teclas ++ctrl+alt+backspace++ (Reiniciar Xorg)

-  Desde una terminal: ``sudo service mdm restart``

Fuente: `How do I restart Cinnamon from the
tty <https://askubuntu.com/questions/143838/how-do-i-restart-cinnamon-from-the-tty>`__

Cómo usar xargs para convertir varios ficheros con convert/magick
------------------------------------------------------------------------

Ejemplo:

.. code:: shell

    find -iname "*.png" -print0 | xargs --null  basename -s .png | xargs -I fn convert fn.png fn.pdf

La primera parte busca los ficheros que terminan en ``.png``, y los
imprime, pero poniendo un ``NULL`` al final del nombre, al estilo ``c``.
Esto nos permite trabajar con ficheros con espacios en los nombres, ya
que usaremos como carácter de separación el nulo y no el espacio.

La segunda parte acepta el listado anterior, usando como separador los
nulos gracias a la opción ``--null``. Usamos la utilidad
``basename`` (https://linux.die.net/man/1/basename) que nos da el
nombre del fichero sin separadores de directorios. Además, usamos la
opción ``-s`` de ``basename`` para eliminar el sufijo (*suffix*)
``.png``.

La tercera parte ejecuta ``convert`` para pasar las imágenes *PNG* a
documentos *PDF*. La opción ``-I`` la indica a ``xargs`` que debe
ejecutar tantas ordenes ``convert`` como líneas haya en la entrada (El
comportamiento por defecto es invocar el programa una vez y pasarle la
lista de parámetros). También le pedimos que sustituya cada valor de
entrada por el nombre que le hemos asignado, en este caso fn (Ojo porque
cualquier aparición del texto ``fn`` será sustituido por el dato de
entrada, en este caso el nombre del archivo).

Fuentes:

- `Invoking the shell from xargs <https://www.gnu.org/software/findutils/manual/html_node/find_html/Invoking-the-shell-from-xargs.html>`_

- `12 Practical Examples of Linux Xargs Command for Beginners <https://www.tecmint.com/xargs-command-examples/>`_

- `basename <https://linux.die.net/man/1/basename>`_


Cómo copiar la salida de un comando al portapapeles
------------------------------------------------------------------------

Se puede usar el comando **``xclip``**, que interactúa con el porta
papeles. Por ejemplo, el siguiente código copia el texto “Hola, Mundo”
al porta papeles de Linux:

.. code:: shell

    ls | xclip -sel clip

Se puede ahora pegar este contenido usando las combinaciones de teclas
:keys`ctrl+v` o :keys:`ctrl+shift+v`.

El sistema de ventanas *X-window* mantiene tres servicios de porta
papeles diferentes:

- ``primary``: El servidor primario o ``primary`` se usa normalmente
para implementar las operaciones de copiado y pegado realizadas con
el ratón. Este el el servicio por defecto de ``xclip``. Para pegar el
texto se usa el tercer botón o botón central del ratón (A menudo
implementado en la rueda)

- ``secondary``: El porta papeles secundario se usa con mucha menos
frecuencia. Hay que usar la constante ``XA_SECONDARY`` para
seleccionar este porta papeles.

- ``clipboard``: El porta papeles del sistema, de forma similar al
secundario, para poder usarlo especificamos la constante
``XA_CLIPBOARD``. Se pega el contenido usando las combinaciones de
teclas al efecto.

Fuentes:

- `Copy and paste at the Linux command line with xclip \| Opensource.com <https://opensource.com/article/19/7/xclip>`_

- `How do I copy a file to the clipboard in Linux? <https://www.cyberciti.biz/faq/how-do-i-copy-a-file-to-the-clipboard-in-linux/>`_

- `How To Copy Command Output To Linux Clipboard Directly <https://www.cyberciti.biz/faq/xclip-linux-insert-files-command-output-intoclipboard/>`_


Cómo mostrar imágenes en la terminal con Viu
------------------------------------------------------------------------

`Viu <https://github.com/atanunq/viu>`__ es una aplicación de línea de
comandos que permite visualizar imágenes en la consola. Es libre y está
escrito en Rust.

Con Viu pdemos:

- Mostrar tipos de imágenes muy usadas, como .jpg, .png, igif etc.
- Mostrar las imágenes con unas dimensiones ajustadas.
- Mostrar imágenes directamente desde una web, como por ejemplo giphy.

Como está escrito en Rust, podemos instalarlo usando cargo:

.. code:: shell

    $ cargo install viu

El uso es trivial:

.. code:: shell

    $ viu image.jpg

.. figure:: ./linux/viu-sample.png
   :alt: Ejemplo viu


Para modificar las dimensiones, se pueden usar los parámetros ``-h``
(*Height*) o ``-w`` (*Width*):

.. code:: shell

    $ viu image.jpg -w 40

Podemos mostrar todas las imágenes dentro de una carpetas, usando
comodines:

.. code:: shell

    $ viu Desktop/pic*

Entre los formatos que reconoce, se encuentran los *gifs* animados. Para
salir de la visualización, basta con pulsar :keys:`ctrl+c`.

.. code:: shell

    $ viu animated.gif

Fuente: `3 CLI Image Viewers To Display Images In The Termina <https://ostechnix.com/how-to-display-images-in-the-terminal/>`_


Cómo ejecutar comandos con sudo sin tener que especificar la contraseña
------------------------------------------------------------------------

Primero accedemos como ``root``:

.. code:: shell

    sudo su -

Realizamos una copia del fichero ``/etc/sudoers``, por si acaso.

.. code:: shell

    cp /etc/sudoers /root/sudoers.bak

Editar el fichero ``/etc/sudoers`` usando la orden ``visudo``:

.. code:: shell

    EDITOR=vim visudo

Añadir la siguiente línea, por ejemplo para permitir al usuario
``euribates`` ejecutar sin necesidad de pedirle la contraseña los
programas ``/usr/bin/killall`` y ``/usr/local/bin/supervisorctl`` (Por
seguridad es mejor escribir la ruta completa del binario):

.. code::

    euribates ALL = NOPASSWD: /usr/bin/kill, /usr/local/bin/supervisorctl

Fuentes:

- `How to run sudo command without a password on a Linux or Unix <https://www.cyberciti.biz/faq/linux-unix-running-sudo-command-without-a-password/>`_


How to Check timezone
------------------------------------------------------------------------

**Method 1**: Check timezone in Linux using ``timedatectl`` command

You can check timezone in Linux by simply running timedatectl command
and checking the time zone section of the output as shown below:

.. code:: shell

    [root@localhost ~]# timedatectl
    Local time: Sun 2021-07-11 12:09:14 WEST
    Universal time: Sun 2021-07-11 11:09:14 UTC
    RTC time: Sun 2021-07-11 11:09:14
    Time zone: Atlantic/Canary (WEST, +0100)
    System clock synchronized: yes
    NTP service: active
    RTC in local TZ: no

You can also check the list of timezones using
``timedatectl list-timezones``.

**Method 2**: Check timezone in Linux using date command

You can use ``date "+%z %Z"`` command as shown below:

.. code:: shell

    +0100 WEST

Fuentes:

-  `How to Check timezone in Linux (timedatectl and date commands) Using
4 Easy Methods \| CyberITHub <https://www.cyberithub.com/check-timezone-in-linux-timedatectl-command/>`_


Cómo insertar un carácter usando su código numérico (Unicode)
------------------------------------------------------------------------

Una forma fácil, si sabemos el código numérico en hexadecimal, es usando
:keys:`ctrl+shift+u` y luego el código hexadecimal. Por ejemplo
:keys:`ctrl+shift+u` seguido de :keys:`4`, :keys:`0`, :keys:`enter`
produce el carácter ``@``, que es el carácter 64 decimal, ``40`` en
hexadecimal.

Algunos código útiles son:

======== ========
Hex code Caracter
======== ========
``23``   ``#``
``40``   ``@``
``5b``   ``[``
``5d``   ``]``
``7b``   ``{``
``7d``   ``}``
======== ========

Este truco funciona al menos con xfce4-terminal, gnome-terminal,
lxterminal, libreoffice, mousepad, chromium-browser y firefox.

Fuente: `keyboard - How to type special characters in Linux? - Super User <https://superuser.com/questions/59418/how-to-type-special-characters-in-linux>`_


Cómo hacer para que sudo recuerde la contraseña un cierto tiempo
------------------------------------------------------------------------

Hay que ejecutar ``visudo``:

.. code:: shell

    sudo visudo

Buscar el texto ``Defaults env_reset``, y poner en la siguiente línea:

.. code::

    Defaults timestamp_timeout=<time-in-minutes>

Por ejemplo, para una hora:

.. code::

    Defaults timestamp_timeout=60

Para 12 horas:

.. code::

    Defaults timestamp_timeout=720

Fuentes:

-  `How to Change Sudo Timeout Period on Linux - OMG! Linux <https://www.omglinux.com/change-sudo-timeout-linux/>`_


Cómo funciona el *firewall* UFM
------------------------------------------------------------------------

El *software* de configuración de *firewall* por defecto en Ubuntu (Y
por tanto, en Mint) en **ufw**. Se desarrolló para facilitar la
configuración de las ``iptables``, de forma amigable. Hay que tener en
cuenta que UFW, por defecto, está deshabilitado.

Enable UFW
~~~~~~~~~~

To turn UFW on with the default set of rules:

.. code:: shell

    sudo ufw enable

To check the status of UFW:

.. code:: shell

    sudo ufw status verbose

Reglas para permitir o denegar (*Allow and Deny specific rules*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para permitir el acceso a un puerto:

::

    sudo ufw allow <port>/<optional: protocol>

Por ejemplo, para permitir acceso usando UDP y/o TCP, al puerto
:math:`53`.

.. code:: shell

    sudo ufw allow 53

Si solo queremos habilitar acceso por TCP:

.. code:: shell

    sudo ufw allow 53/tcp

De forma similar, solo habilitar acceso por UDP:

.. code:: shell

    sudo ufw allow 53/udp

Para denegar el acceso, usariamos:

.. code:: shell

    sudo ufw deny <port>/<optional: protocol>

Ejemplo: Denegar acceso al puerto :math:`53` tanto para TCP como para
UDP:

::

    sudo ufw deny 53

Solo para TCP:

.. code:: shell

    sudo ufw deny 53/tcp

Y solo par UDP:

.. code:: shell

    sudo ufw deny 53/udp

Fuente: `UFW - Community Help Wiki <https://help.ubuntu.com/community/UFW>`_


Cómo comprobar puertos abiertos en Linux
------------------------------------------------------------------------

Algunos de los puertos más usados son:

- Puerto 22 (SSH)
- Puerto 80 (HTTP)
- Puerto 443 (HTTPS)
- Puerto 21 (FTP)
- Puerto 25 (SMTP)
- Puerto 3306 (MySQL)
- Puerto 5432 (PostgreSQL)

Con ``nmap``:
~~~~~~~~~~~~~

.. code:: shell

    nmap hostname

El programa realizará una comprobación de los puertos más usados en el
servidor, y devuelve información de los que estén abiertos. También
podemos especificar un rango de puertos con el parámetro ``-p``:

.. code:: shell

    nmap -p 1-65535 localhost

La forma más recomendada de uso es:

.. code:: shell

    sudo nmap -n -PN -sT -sU -p- localhost

Donde:

- ``-n``: Se salta la resolución de nombres por DNS.

- ``-PN``: Se salta la fase de descubrimiento, asumiendo que el *host*
objetivo esta activo sin necesidad de comprobarlo.

- ``-sT``: Inicia un *TCP connect scan*, que intenta establecer una
conexión completa TCP con cada puerto.

- ``-sU``: Realiza un escaneo también con el protocolo UDP

- ``-p-``: Escanea todos los puertos, sin especificar rangos.

La salida identifica tanto los puertos abiertos como los servicios que
están utilizándolos.


Con ``lsof``:
~~~~~~~~~~~~~

El comando ``lsof`` (*list open files*) tembién se puede usar para
descubrir puertos abiertos. Muestra todas las conexiones activas, ya que
unix las mentiene como un tipo especial de ficheros (`everything is a
file <https://en.wikipedia.org/wiki/Everything_is_a_file>`__). La forma
más usada es:

.. code:: shell

    sudo lsof -P -n

Donde:

- ``-n``: No intenta resolver los nombres

- ``-P``: Muestro los números de los puertos, en vez de los nombres de
los servicios.

- ``-i``: Permite especificar una dirección IP. Si no se indica
ninguna, se interpreta como cualquier dirección IP. Las formas
``-i4`` y ``-i6`` permite indicar conexiones IP4 o IP6.

Podemos filtrar el resultado buscando por ``LISTEN`` para ver los
puertos abiertos.

Con netstat:
~~~~~~~~~~~~

Esta herramienta se ha quedado un poco antigua, pero si está instalada
podemos usarla también para ver los puertos abiertos en local:

.. code:: shell

    sudo netstat -tuln

Donde:

- ``-t``: Muestra los puertos TCP
- ``-u``: Muestra los puertos UDP
- ``-l``: Muestra los puertos abiertos en modo ``LISTEN``
- ``-n``: No resuelve los nombres mediante DNS

Con ``ss``:
~~~~~~~~~~~

El programa ``ss`` (*socket statistics*) es una alternativa moderna a
``netstat``. En principio es más rápido y eficiente. Proporciona la
misma información que ``netstat``, pero de una forma mas condensada.
Para ver los puertos abiertos, hay que hacer:

.. code:: shell

    sudo ss -tuln

Los parámetros toman el mismo significado que en ``netstat``.

Con ``netcat`` (``nc``):
~~~~~~~~~~~~~~~~~~~~~~~~

``Netcat`` (often abbreviated as ``nc``) is a flexible tool for network
exploration, troubleshooting, and port scanning. You can use it to see
if a specific port is open. For example:

.. code:: shell

    nc -zv localhost 22

This command checks if port 22 (SSH) is open on the local machine, where
``-z`` prevents actual data transfer and ``-v`` provides verbose output.
Netcat is particularly useful when you want to quickly verify the status
of specific ports.

Fuentes:

-  `How to Check Open Ports in Linux: 6 Essential Methods <https://www.liquidweb.com/blog/how-to-locate-open-ports-in-linux/>`_


Cómo saber en que terminal (``tty``) estamos
------------------------------------------------------------------------

Solo hay que ejecutar el comando ``tty``. Saldrá algo como
``/dev/pts/1``, por ejemplo.

.. code:: shell

    ❯ tty
    /dev/pts/1

Si ahora, desde otra terminal, hacemos:

.. code:: shell

    echo matraka > /dev/pts/0

El texto ``matraka`` aparecerá en la primera terminal.

Cómo saber a que grupos pertenece un usuario
--------------------------------------------

Podemos usar el comando ``id``, con la opción ``-nG``, para mostrar a
que grupos pertenece un usuario del sistema. Si no se indica el login
del usuario, se muestra la información del usuario actual. El primer
grupo mostrado es el grupo primario.

El comando ``id`` sin opciones muestra el ``ID`` del usuario (``uid``),
su grupo primario (``gid``) y cualquier grupo secundario al que
pertenezca el usuario.

En este ejemplo, se muestra que el usuario actual̀, ``jileon``, tiene
como grupo principal un grupo llamado igualmente ``jileon``, y que
también pertenece a los grupos ``adm``, ``cdrom``, ``sudo``, ``dip``,
``plugdev``, ``users``, ``lpadmin``, ``sambashare`` y ``docker``.

.. code:: shell

    $ id
    uid=1000(jileon) gid=1000(jileon) groups=1000(jileon),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),100(users),105(lpadmin),125(sambashare),984(docker)
    $ id -nG
    jileon adm cdrom sudo dip plugdev users lpadmin sambashare docker

-  Fuente: `How to List All Groups in Linux <https://kodekloud.com/blog/how-to-list-all-groups-in-linux/>`_


Cómo montar una unidad USB en Linux
------------------------------------------------------------------------

Mounting USB drive is no different than mounting USB stick or even a
regular SATA drive.In Linux, you can mount all file systems including
ext4, FAT, and NTFS.

Los pasos son:

- Detectar/identificar la unidad USB

- Crear un directorio que sirva como punto de montaje

- Montar la unidad

- **Detecting USB hard drive**: After you plug in your USB device to
the USB port, Linux system adds a new block device into ``/dev/``
directory. At this stage, you are not able to use this device as the
USB filesystem needs to be mounted before you can retrieve or store
any data. To find out what name your block device file have you can
run ``fdisk -l`` command (Probablemente con ``sudo``):

.. code::

    Disk /dev/sdc: 7.4 GiB, 7948206080 bytes, 15523840 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0x00000000

    Device     Boot Start      End  Sectors  Size Id Type
    /dev/sdc1  *     8192 15523839 15515648  7.4G  b W95 FAT32


The above output will most likely list multiple disks attached to
your system. Look for your USB drive based on its size and
filesystem. Once ready, take a note of the **block device name** of
the partition you intent to mount. For example in our case that will
be ``/dev/sdc1`` with FAT32 filesystem.

-  **Crear un direcotrio como punto de montaje**: Un simple ``mkdir``,
si no tenemos uno creado previamente. Las unidades USB suelen
montarse en una carpeta dentro de ``/media/``.

.. code::

    mkdir -p /media/usb-drive

– **Montar la unidad USB**: At this stage we are ready to mount our
USB’s partition ``/dev/sdc1`` into ``/media/usb-drive`` mount point:

.. code::

    mount /dev/sdc1 /media/usb-drive/

To check whether your USB drive has been mounted correctly execute mount
command again without any arguments and use grep to search for USB block
device name:

.. code::

    $ mount | grep sdc1
    /dev/sdc1 on /media/usb-drive type vfat (rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=utf8,shortname=mixed,errors=remount-ro


Montar la unidad USB de forma permanente en Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to mount your USB in Linux permanently after reboot add the
following line into your /etc/fstab config file:

.. code::

    /dev/sdc1     /media/usb-drive        vfat    defaults     0    0

For any other file system type simply set correct type. For example the
bellow command will mount USB driver with NTFS file system:

.. code::

    /dev/sdc1     /media/usb-drive        ntfs    defaults     0    0


NTFS Filesystem Unsupported
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Al intentar montar una unidad formateada con NTFS, podemos encontrarnos
con el siguiente error:

.. code::

    mount: /mnt/usb: unknown filesystem type 'ntfs'.

Hay que instalar el paquete ``ntfs-3g`` para añadir soporte NTFS al
sistema de archivos de Linux: ``sudo apt install ntfs-3g``.

-  Fuente: `Mount USB Drive in Linux: Step-by-step guide \| Cloudflare <https://linuxconfig.org/howto-mount-usb-drive-in-linux>`_


Cómo crear un disco vistual en memoria (RAMdisk) en Linux
------------------------------------------------------------------------

Hay que ejecutar las dos ordenes siguientes, cambiando ``4096M`` por el
tamaño de disco que queramos. Recuerda que este disco no será
persistente y habrá desaparecido, junto con todo su contenido, en el
siguiente arranque del sistema.

.. code:: shell

    sudo mkdir -p /media/ramdisk
    sudo mount -t tmpfs -o size=4096M tmpfs /media/ramdisk

Fuente: `Linux Mint Commands: A Cheatsheet For Linux Mint With Examples
- Kompulsa <https://www.kompulsa.com/linux-mint-commands-a-cheatsheet-for-linux-mint-with-examples/>`_


Cómo enviar notificaciones de escritorio con notify-send (DBus)
------------------------------------------------------------------------

Cada entorno de escritorio en Linux tiene su propio sistema de
notificaciones que implementa las especificaciones de
`Freedesktop <https://www.freedesktop.org/wiki/>`__. Algunos, como GNOME
o KDE, utilizan sistemas integrados que no se pueden reemplazar; otros,
como Xfce o Mate, utilizan componentes más modulares: el demonio de
notificaciones de Xfce y el demonio de notificaciones de Mate,
respectivamente.

También existen sistemas de notificaciones independientes del entorno de
escritorio (como `dunst <https://wiki.archlinux.org/title/Dunst>`__):
generalmente se utilizan en configuraciones mínimas (por ejemplo, al
usar un gestor de ventanas simple en lugar de entornos de escritorio
completos).

La utilidad **``notify-send``** viene instalada normalmente por defecto
en la mayoría de los casos, como parte de la librería ``libnotify``. Si
no fuera el caso, podemos instalarla con:

.. code:: shell

    sudo apt install libnotify-bin

La forma más simple de usarla es con un solo parámetro:

.. code:: shell

    notify-send "Este es el mensaje"

Con dos parámetros, se interpreta el primero como el título y el segundo
como el cuerpo del mensaje:

.. code:: shell

    notify-send "Este es el título" "Este es el cuerpo del mensaje"

Se puede usar un conjunto muy limitado de etiquetas HTML dentro del
cuerpo: ``b``, ``i``, ``u``, ``a`` e ``img``.

Se puede indicar la urgencia del mensaje con el parámetro
``-u/--urgency`` que acepta los niveles ``low``, ``normal`` (por
defecto) y ``critical``. Si se usa este último, el mensaje no desaparece
pasado un cierto tiempo, sino que tiene que ser cerrado manualmente por
el usuario. Hablando del tiempo que se muestra el mensaje, algunos
sistemas aceptan el parámetro ``-t/--expire-time`` con un valor de
segundos.

Fuente: `How to send desktop notifications using notify-send <https://linuxconfig.org/how-to-send-desktop-notifications-using-notify-send>`_
