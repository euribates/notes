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

This command will scan all commonly used ports on your server and return
information on any that are open. You can also specify a particular
range of ports if you’re looking for something specific:

```shell
nmap -p 1-65535 localhost
```

Nmap’s detailed output helps identify not only open ports but also the
services running on them, making it a robust tool for security checks.

### Con `lsof`:

The lsof (list open files) command is another useful tool for viewing
open ports. It shows all active connections by listing open files,
including network connections. To check for open ports, run:

```shell
sudo lsof -i -P -n
```

This command lists all network connections without resolving hostnames
(`-n`) and displays port numbers rather than service names (`-P`). Look for
entries marked with “LISTEN” to see which ports are open for incoming
connections.

### Con netstat:

The netstat command has long been a favorite for checking network status
on Linux. Although it’s gradually being replaced by newer tools, it’s
still available on many systems. To view open ports, try:

```shell
sudo netstat -tuln
```

This command displays all TCP (`-t`) and UDP (`-u`) ports in a listening
state (`-l`), without resolving hostnames (`-n`). Each line in the
output will show the local address and port, making it easy to see which
ports are open.

### Con `ss`:

El programa `ss` (_socket statistics_) es una alternativa moderna a `netstat`.
En principio es más ráöido y eficiente. Proporciona la misma información
que `netstat`, pero de una forma mas condensada. Para ver los puertos
abiertos, hay que hacer:

```shell
sudo ss -tuln
```

The output structure is comparable to netstat, showing active TCP and
UDP ports in a listening state. This command is highly efficient,
especially on newer systems, and is a good replacement for netstat:.

### Com `netcat` (`nc`):

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

