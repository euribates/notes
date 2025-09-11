---
title: Notas sobre Linux
tags:
    - Linux
    - systemd
    - ram
---

## Cómo saber cuanta memoria hay en el equipo y de qué tipo

El comando a escribir puede variar dependiendo de la distribución, pero por lo 
general es:

```shell
sudo dmidecode --type memory
```

El comando devolverá una tabla con toda la información sobre tu memoria RAM. En
__Maximum Capacity__ la cantidad exacta de memoria que tienes instalada, En
__Number of devices__ el número de módulos de memoria instalados. Más abajo, en
__Type__ podrás saber el tipo de memoria que tienes.

De la documentación de `dmidecode`:

> dmidecode  is  a  tool for dumping a computer's DMI (some say SMBIOS) table
> contents in a human-readable format. This table contains a description of the
> system's hardware components, as well as  other  useful pieces  of
> information such as serial numbers and BIOS revision. Thanks to this table,
> you can retrieve this information without having to probe for the actual
> hardware.

- Fuente: [Cómo saber cuánta memoria RAM tienes y de qué tipo es, en Windows, macOS y GNU/Linux](https://www.xataka.com/basics/como-saber-cuanta-memoria-ram-tienes-que-tipo-windows-macos-gnu-linux)



## Cómo reiniciar Cinnamon

Se puede hacer de diversas formas:

- Presionando ++alt+f2++, tecleamos `r` y pulsamos ++enter++.

- Con la combinación de teclas ++ctrl+alt+backspace++ (Reiniciar Xorg)

- Desde una terminal: `sudo service mdm restart`


Fuente: [How do I restart Cinnamon from the tty](https://askubuntu.com/questions/143838/how-do-i-restart-cinnamon-from-the-tty)


## Cómo usar xargs para convertir varios ficheros con convert/magick

Ejemplo: 

```shell
find -iname "*.png" -print0 | xargs --null  basename -s .png | xargs -I fn convert fn.png fn.pdf
```

La primera parte busca los ficheros que terminan en `.png`, y los imprime, pero
poniendo un `NULL` al final del nombre, al estilo `c`. Esto nos permite
trabajar con ficheros con espacios en los nombres, ya que usaremos como
carácter de separación el nulo y no el espacio.

La segunda parte acepta el listado anterior, usando como separador los nulos
gracias a la opción `--null`. Usamos la utilidad
[`basename`](https://linux.die.net/man/1/basename) que nos da el nombre del
fichero sin separadores de directorios. Además, usamos la opción `-s` de
`basename` para eliminar el sufijo (_suffix_) `.png`.

La tercera parte ejecuta `convert` para pasar las imágenes _PNG_ a documentos
_PDF_.  La opción `-I` la indica a `xargs` que debe ejecutar tantas ordenes
`convert` como líneas haya en la entrada (El comportamiento por defecto es
invocar el programa una vez y pasarle la lista de parámetros). También le
pedimos que sustituya cada valor de entrada por el nombre que le hemos
asignado, en este caso fn (Ojo porque cualquier aparición del texto `fn` será
sustituido por el dato de entrada, en este caso el nombre del archivo).

Fuentes:

- [Invoking the shell from xargs](https://www.gnu.org/software/findutils/manual/html_node/find_html/Invoking-the-shell-from-xargs.html)
- [12 Practical Examples of Linux Xargs Command for Beginners](https://www.tecmint.com/xargs-command-examples/)
- [basename](https://linux.die.net/man/1/basename)


## Cómo copiar la salida de un comando al portapapeles

Se puede usar el comando **`xclip`**, que interactúa con el porta papeles. Por ejemplo,
el siguiente código copia el texto "Hola, Mundo" al porta papeles de Linux:

```shell
ls | xclip -sel clip
```

Se puede ahora pegar este contenido usando las combinaciones de teclas
++ctrl+v++ o ++ctrl+shift+v++.

El sistema de ventanas _X-window_ mantiene tres servicios de porta papeles diferentes:

- `primary`: El servidor primario o `primary` se usa normalmente para implementar las
  operaciones de copiado y pegado realizadas con el ratón. Este el el servicio por
  defecto de `xclip`. Para pegar el texto se usa el tercer botón o
  botón central del ratón (A menudo implementado en la rueda)

- `secondary`: El porta papeles secundario se usa con mucha menos frecuencia. Hay que usar
  la constante `XA_SECONDARY` para seleccionar este porta papeles.

- `clipboard`: El porta papeles del sistema, de forma similar al secundario, para poder
   usarlo especificamos la constante `XA_CLIPBOARD`. Se pega el contenido
   usando las combinaciones de teclas al efecto.

Fuentes:

- [Copy and paste at the Linux command line with xclip | Opensource.com](https://opensource.com/article/19/7/xclip)

- [How do I copy a file to the clipboard in Linux?](https://www.cyberciti.biz/faq/how-do-i-copy-a-file-to-the-clipboard-in-linux/)

- [How To Copy Command Output To Linux Clipboard Directly](https://www.cyberciti.biz/faq/xclip-linux-insert-files-command-output-intoclipboard/)


## Cómo mostrar imágenes en la terminal con Viu

**[Viu](https://github.com/atanunq/viu)** es unaaplicación de línea de comandos que permite visualizar imágenes en
la consola. Es libre y está escrito en Rust.

Con Viu pdemos:

- Mostrar tipos de imágenes muy usadas, como .jpg, .png, igif etc.
- Mostrar las imágenes con unas dimensiones ajustadas.
- Mostrat imágenes directamente desde una web, como por ejemplo giphy.

Como está escrito en Rust, podemos instalarlo usando cargo:

```shell
$ cargo install viu
```

El uso es trivial:

```shell
$ viu image.jpg
```

![Ejemplo viu](./linux/viu-sample.png)

Para modificar las dimensiones, se pueden usar los parámetros `-h` (_Height_) o
`-w` (_Width_):

```shell
$ viu image.jpg -w 40
```

Podemos mostrar todas las imágenes dentro de una carpetas, usando comodines:

```shell
$ viu Desktop/pic*
```

Entre los formatos que reconoce, se encuantran los gifs animados. Para salir de
la visualización, bastya con pulsar ++ctrl+c++.

```shell
$ viu animated.gif
```


Fuente: [3 CLI Image Viewers To Display Images In The Termina](https://ostechnix.com/how-to-display-images-in-the-terminal/)

tags:
  - rust
  - terminal
  - cli


### Cómo ejecutar comandos con sudo sin tener que especificar la contraseña

Primero accedemos como `root`:

```shell
sudo su -
```

Realizamos una copia del sichero `/etc/sudoers`, por si acaso.

```shell
cp /etc/sudoers /root/sudoers.bak
```

Editar el fichero `/etc/sudoers` usando la orden `visudo`:

```shell
EDITOR=vim visudo
```

Añadir la siguiente línea, por ejemplo para permitir al usuario `euribates`
ejecutar sin necesidad de pedirle la contraseña los programas
`/usr/bin/killall` y `/usr/local/bin/supervisorctl` (Por seguridad es mejor
escribir la ruta completa del binario):

```
euribates ALL = NOPASSWD: /usr/bin/kill, /usr/local/bin/supervisorctl
```

Fuentes: 

- [How to run sudo command without a password on a Linux or Unix](https://www.cyberciti.biz/faq/linux-unix-running-sudo-command-without-a-password/)

tags: sudo


### How to Check timezone

**Method 1**: Check timezone in Linux using `timedatectl` command

You can check timezone in Linux by simply running timedatectl command and
checking the time zone section of the output as shown below:

```shell
[root@localhost ~]# timedatectl
               Local time: Sun 2021-07-11 12:09:14 WEST 
           Universal time: Sun 2021-07-11 11:09:14 UTC  
                 RTC time: Sun 2021-07-11 11:09:14      
                Time zone: Atlantic/Canary (WEST, +0100)
System clock synchronized: yes                          
              NTP service: active                       
          RTC in local TZ: no
```

You can also check the list of timezones using `timedatectl list-timezones`.

**Method 2**: Check timezone in Linux using date command

You can use `date "+%z %Z"` command as shown below:

```shell
+0100 WEST
```

Fuentes: 

- [How to Check timezone in Linux (timedatectl and date commands) Using 4
Easy Methods | CyberITHub](https://www.cyberithub.com/check-timezone-in-linux-timedatectl-command/)

## Cómo insertar un carácter usando su código numérico (Unicode)



Una forma fácil, si sabemos el código numérico en hexadecimal, es
usando ++ctrl+shift+u++ y luego el código hexadecimal. Por ejemplo
++ctrl+shift+u++ seguido de ++4++, ++0++, ++enter++ produce el carácter `@`,
que es el carácter 64 decimal, `40` en hexadecimal.

Algunos código útiles son:

| Hex code |  Caracter |
|----------|:---------:|
| `23`     | `#`       |
| `40`     | `@`       |
| `5b`     | `[`       |
| `5d`     | `]`       |
| `7b`     | `{`       |
| `7d`     | `}`       |

Este truco funciona al menos con xfce4-terminal, gnome-terminal, lxterminal,
libreoffice, mousepad, chromium-browser y firefox.

Fuente: [keyboard - How to type special characters in Linux? - Super User](https://superuser.com/questions/59418/how-to-type-special-characters-in-linux)

## Cómo hacer para que sudo recuerde la contraseña un cierto tiempo

Hay que ejecutar `visudo`:

```shell
sudo visudo
```

Buscar el texto `Defaults env_reset`, y poner en la siguiente línea:

```
Defaults timestamp_timeout=<time-in-minutes>
```

Por ejemplo, para una hora:

```
Defaults timestamp_timeout=60
```

Para 12 horas:

```
Defaults timestamp_timeout=720
```

Fuentes:

- [How to Change Sudo Timeout Period on Linux - OMG! Linux](https://www.omglinux.com/change-sudo-timeout-linux/)

## Cómo funciona el _firewall_ UFM

El _software_ de configuración de_firewall_ por defecto en Ubuntu (Y por tanto,
en Mint) en **ufw**. Se desarroillo para facilitar la configuración de las
`iptables`, de forma amigable. Hay que tener en cuenta que UFW, por defecto,
está desabilitado.

### Enable UFW

To turn UFW on with the default set of rules:

```shell
sudo ufw enable
```

To check the status of UFW:

```shell
sudo ufw status verbose
```

### Reglas para permitir o denegar (_Allow and Deny specific rules_)

Para permitir el acceso a un puerto:

```
sudo ufw allow <port>/<optional: protocol>
```

Por ejemplo, para permitir acceso usando UDP y/o TCP, al puerto $53$.

```shell
sudo ufw allow 53
```

Si solo queremos habilitar acceso por TCP:

```shell
sudo ufw allow 53/tcp
```

De forma similar, solo habilitar acceso por UDP:


```shell
sudo ufw allow 53/udp
```

Para denegar el acceso, usariamos:

```shell
sudo ufw deny <port>/<optional: protocol>
```


Ejemplo: Denegar acceso al puerto $53$ tanto para TCP como para UDP:

```
sudo ufw deny 53
```

Solo para TCP:

```shell
sudo ufw deny 53/tcp
```

Y solo par UDP:

```shell
sudo ufw deny 53/udp
```

Fuente: [UFW - Community Help Wiki](https://help.ubuntu.com/community/UFW)


## Cómo comprobar puertos abiertos en Linux

Algunos de los puertos más usados son:

- Puerto 22 (SSH)
- Puerto 80 (HTTP)
- Puerto 443 (HTTPS)
- Puerto 21 (FTP)
- Puerto 25 (SMTP)
- Puerto 3306 (MySQL)
- Puerto 5432 (PostgreSQL)

### Con `nmap`:

```shell
nmap hostname
```

El programa realizará una comprobación de los puertos más usados en el
servidor, y devuelve información de los que estén abiertos. También
podemos especificar un rango de puertos con el parámetro `-p`:

```shell
nmap -p 1-65535 localhost
```

La forma más recomendada de uso es:

```shell
sudo nmap -n -PN -sT -sU -p- localhost
```

Donde:

- `-n`: Se salta la resolución de nombres por DNS.

- `-PN`: Se salta la fase de descubrimiento, asumiendo que el _host_
  objetivo esta activo sin necesidad de comprobarlo.

- `-sT`: Inicia un _TCP connect scan_, que intenta establecer una
  conexión completa TCP con cada puerto.

- `-sU`: Realiza un escaneo también con el protocolo UDP

- `-p-`: Escanea todos los puertos, sin especificar rangos.

La salida identifica tanto los puertos abiertos como los servicios que
están utilizándolos.

### Con `lsof`:

El comando `lsof` (_list open files_) tembién se puede usar para descubrir puertos abiertos. Muestra todas las conexiones activas, ya que unix las mentiene como un tipo especial de ficheros ([_everything is a file_](https://en.wikipedia.org/wiki/Everything_is_a_file)). La forma más usada es:

```shell
sudo lsof -P -n
```

Donde:

- `-n`: No intenta resolver los nombres

- `-P`: Muestro los números de los puertos, en vez de los nombres de los
  servicios.

- `-i`: Permite especificar una dirección IP. Si no se indica ninguna,
  se interpreta como cualquier dirección IP. Las formas `-i4` y `-i6`
  permite indicar conexiones IP4 o IP6.

Podemos filtrar el resuiltado buscando por `LISTEN` para ver los puertos
abiertos.


### Con netstat:

Esta herramienta se ha quedao un poco antigua, pero si está instalada
podemos usarla también para ver los puertos abiertos en local:

```shell
sudo netstat -tuln
```

Donde:

- `-t`: Muestra los puertos TCP
- `-u`: Muestra los puertos UDP
- `-l`: Muestra los puertos abiertos en modo `LISTEN`
- `-n`: No resuelve los nombres mediante DNS

### Con `ss`:

El programa `ss` (_socket statistics_) es una alternativa moderna a `netstat`.
En principio es más rápido y eficiente. Proporciona la misma información
que `netstat`, pero de una forma mas condensada. Para ver los puertos
abiertos, hay que hacer:

```shell
sudo ss -tuln
```

Los parámetros toman el mismo significado que en `netstat`.

### Con `netcat` (`nc`):

`Netcat` (often abbreviated as `nc`) is a flexible tool for network
exploration, troubleshooting, and port scanning. You can use it to
see if a specific port is open. For example:

```shell
nc -zv localhost 22
```

This command checks if port 22 (SSH) is open on the local machine,
where `-z` prevents actual data transfer and `-v` provides verbose
output. Netcat is particularly useful when you want to quickly
verify the status of specific ports.

Fuentes:

- [How to Check Open Ports in Linux: 6 Essential Methods](https://www.liquidweb.com/blog/how-to-locate-open-ports-in-linux/)

## Cómo saber en que terminal (`tty`) estamos

Solo hay que ejecutar el comando `tty`. Saldrá algo como `/dev/pts/1`,
por ejemplo.

```shell
❯ tty
/dev/pts/1
```

Si ahora, desde otra terminal, hacemos:

```shell
echo matraka > /dev/pts/0
```

El texto `matraka` aparecerá en la primera terminal. 

## Cómo saber a que grupos pertenece un usuario

Podemos usar el comando `id`, con la opción `-nG`, para mostrar a que
grupos pertenece un usuario del sistema. Si no se indica el login del
usuario, se muestra la información del usuario actual. El primer grupo
mostrado es el grupo primario.

El comando `id` sin opciones muestra el `ID` del usuario (`uid`), su
grupo primario (`gid`) y cualquier grupo secundario al que pertenezca el
usuario.

En este ejemplo, se muestra que el usuario actual̀, `jileon`, tiene como
grupo principal un grupo llamado igualmente `jileon`, y que también pertenece
a los grupos `adm`, `cdrom`, `sudo`, `dip`, `plugdev`, `users`,
`lpadmin`, `sambashare` y `docker`.

```shell
$ id
uid=1000(jileon) gid=1000(jileon) groups=1000(jileon),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),100(users),105(lpadmin),125(sambashare),984(docker)
$ id -nG
jileon adm cdrom sudo dip plugdev users lpadmin sambashare docker
```

- Fuente: [How to List All Groups in Linux](https://kodekloud.com/blog/how-to-list-all-groups-in-linux/)

### Cómo montar una unidad USB en Linux

Mounting USB drive is no different than mounting USB stick or even a regular SATA drive.In Linux, you can mount all file systems including ext4, FAT, and NTFS.

Los pasos son:

- Detectar/identificar la unidad USB
- Crear un directorio que sirva como punto de montaje
- Montar la unidad

- **Detecting USB hard drive**: After you plug in your USB device to the
  USB port, Linux system adds a new block device into `/dev/` directory.
  At this stage, you are not able to use this device as the USB
  filesystem needs to be mounted before you can retrieve or store any
  data. To find out what name your block device file have you can run
  `fdisk -l` command (Probablemente con `sudo`):

      ```
      Disk /dev/sdc: 7.4 GiB, 7948206080 bytes, 15523840 sectors
      Units: sectors of 1 * 512 = 512 bytes
      Sector size (logical/physical): 512 bytes / 512 bytes
      I/O size (minimum/optimal): 512 bytes / 512 bytes
      Disklabel type: dos
      Disk identifier: 0x00000000

      Device     Boot Start      End  Sectors  Size Id Type
      /dev/sdc1  *     8192 15523839 15515648  7.4G  b W95 FAT32
      ```

  The above output will most likely list multiple disks attached to your
  system. Look for your USB drive based on its size and filesystem. Once
  ready, take a note of the **block device name** of the partition you
  intent to mount. For example in our case that will be `/dev/sdc1` with
  FAT32 filesystem.

- **Crear un direcotrio como punto de montaje**: Un simple `mkdir`, si
  no tenemos uno creado previamente. Las unidades USB suelen montarse en
  una carpeta dentro de `/media/`.

      ```
      mkdir -p /media/usb-drive
      ```

-- **Montar la unidad USB**: At this stage we are ready to mount our USB’s partition `/dev/sdc1` into `/media/usb-drive` mount point:

      ```
      mount /dev/sdc1 /media/usb-drive/
      ```

To check whether your USB drive has been mounted correctly execute mount
command again without any arguments and use grep to search for USB block
device name:

```
$ mount | grep sdc1
/dev/sdc1 on /media/usb-drive type vfat (rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=utf8,shortname=mixed,errors=remount-ro
```

#### Montar la unidad USB de forma permanente en Linux

In order to mount your USB in Linux permanently after reboot add the
following line into your /etc/fstab config file:

```
/dev/sdc1     /media/usb-drive        vfat    defaults     0    0
```

For any other file system type simply set correct type. For example the
bellow command will mount USB driver with NTFS file system:

```
/dev/sdc1     /media/usb-drive        ntfs    defaults     0    0
```


#### NTFS Filesystem Unsupported

Al intentar montar una unidad formateada con NTFS, podemos encontrarnos
con el siguiente error:

```
mount: /mnt/usb: unknown filesystem type 'ntfs'.
```

Hay que instalar el paquete `ntfs-3g` para añadir soporte NTFS al
sistema de archivos de Linux: `sudo apt install ntfs-3g`.


- Fuente: 
[Mount USB Drive in Linux: Step-by-step guide | Cloudflare](https://linuxconfig.org/howto-mount-usb-drive-in-linux)
