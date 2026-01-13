Samba
========================================================================

.. tags:: samba,linux,widnwod,devops


Sobre Samba
------------------------------------------------------------------------

**Samba** es una implementación libre del protocolo de archivos
compartidos de Microsoft Windows (antiguamente llamado ``SMB``,
renombrado posteriormente a CIFS) para sistemas de tipo UNIX. De esta
forma, es posible que computadoras con GNU/Linux, Mac OS X o Unix en
general se vean como servidores o actúen como clientes en redes de
Windows.

Samba también permite validar usuarios haciendo de Controlador
Principal de Dominio (PDC), como miembro de dominio e incluso como un
dominio *Active Directory* para redes basadas en Windows; servir colas
de impresión, directorios compartidos y autentificar con su propio
archivo de usuarios.

Cómo empezar con Samba
------------------------------------------------------------------------

Fuente:

- Samba on Linux the easy way - Gloves Off Linux: https://glovesoff.substack.com/p/samba-on-linux-the-easy-way


Cómo conectarse a unidades de disco sin *password*
------------------------------------------------------------------------

Tenemos que poner las credenciales en un fichero aparte, solo con
permisos de lectura para ``root``. En el fichero ``fsfab`` ponemos la
ruta del archivo.

.. code:: shell

    $ sudo vi /root/.smbcred
    $ sudo cat /root/.smbcred username=username password=secret
    $ sudo chmod 600 /root/.smbcred
    $ sudo ls -al /root/.smbcred
    -rw-------. 1 root root 36 Sep 9 15:43 /root/.smbcred

La línea en ``/etc/fstab``:

.. code:: shell

    //192.168.202.2/drive_e /mnt  cifs  credentials=/root/.smbcred  0 0

La línea se divide en 6 partes:

- La localización remota (``//192.168.202.2/drive_e``)

- El punto de montaje local (``/mnt``)

- El tipo de sistema de ficheros (``cifs``)

-Las opciones (``credentials=/root/.smbcred``)

- ``dump-option`` (``0``)

- ``check/pass-option`` (``0``)

Incluyendo esta línea en el fichero, se puede montar con `mount /mnt`,
pero normalmnete no hará falta hacer nada, ya que se montará
automáticamente en el arranque.

Fuente: 

- Mount Windows (CIFS) shares on Linux with credentials in a secure
way: https://jensd.be/229/linux/mount-windows-cifs-shares-on-linux-with-credentials-in-a-secure-way

Compartir carpetas con Samba en Linux Mint
------------------------------------------------------------------------

Primero, instalar Samba:

.. code:: shell

    sudo apt install samba

Para hacer el sistema "descubrible" y accesible para Windows 7 y
superior, hay que instalar ``wsdd``:

.. code:: shell

    sudo apt install wsdd

Para verificar que el demonio está ejecutándose:

.. code:: shell

    sudo service wsdd status

En Windows 8, 10, 11, también se puede conectar al servidor usado su
nombre ``mDNS``, que es solo el *host name* con el sufijo ``.local``
(``\\nova.local``).

Para hacer el sistema "descubrible" y accesible para MaxOS hay que
instalar:

.. code:: shell

    sudo apt install avahi-daemon

Pata verificar que está activo:

.. code:: shell

    sudo service avahi-daemon status

Fuentes:

- wsdd: https://github.com/christgau/wsdd

- *Share Folders using Samba in Home Network with Mint 21 - Linux
  Mint Forums*: https://forums.linuxmint.com/viewtopic.php?t=377372
