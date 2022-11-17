---
title: Notes on Linux
---
## Notes on Linux

### Cómo reiniciar Cinnamon

Se puede hacer de diversas formas:

- Presionando ++alt+f2++, tecleamos `r` y pulsamos ++enter++.

- Con la combinación de teclas ++ctrl+alt+backspace++ (Reiniciar Xorg)

- Desde una terminal: `sudo service mdm restart`


Fuente: [How do I restart Cinnamon from the tty](https://askubuntu.com/questions/143838/how-do-i-restart-cinnamon-from-the-tty)


### Cómo usar xargs para convertir varios ficheros con convert/magick

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

La tercera parte ejecuta `convert` para pasar las imágenes PNG a documentos
PDF.  La opción `-I` la indica a `xargs` que debe ejecutar tantas ordenes
`convert` como líneas haya en la entrada (El comportamiento por defecto es
invocar el programa una vez y pasarle la lista de parámetros). También le
pedimos que sustituya cada valor de entrada por el nombre que le hemos
asignado, en este caso fn (Ojo porque cualquier aparición del texto `fn` será
sustituido por el dato de entrada, en este caso el nombre del archivo).

Fuentes:

- [Invoking the shell from xargs](https://www.gnu.org/software/findutils/manual/html_node/find_html/Invoking-the-shell-from-xargs.html)
- [12 Practical Examples of Linux Xargs Command for Beginners](https://www.tecmint.com/xargs-command-examples/)
- [basename](https://linux.die.net/man/1/basename)

### Cómo copiar la salida de un comando al portapapeles o _clipboard_

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


### How to display images in the terminal using Viu

**[Viu](https://github.com/atanunq/viu)** is yet another command line application to view images from the Terminal.
It is free, open source CLI image viewer written using Rust programming
language. Using Viu we can;

- Display popular type of image, including .jpg, .png, igif etc.
- Display images in custom dimensions.
- Display images directly from the image hosting platforms, for example giphy.

Since Viu is written in Rust, we can install it using Cargo package manager.
After installing Rust in your Linux box, run the following command to install
Viu.

```shell
$ cargo install viu
```

Viu usage is trivial. Just type viu followed by the image path and hit ENTER key.

```shell
$ viu image.jpg
```

Sample output:

![Ejemplo viu](viu-sample.png)

You can even display custom dimension image using `-h` (Height) or `-w` (Width)
flags like below.

```shell
$ viu image.jpg -w 40
```

To display multiple images one after another in a folder, use wildcard characters like below.

```shell
$ viu Desktop/pic*
```

Like I already mentioned, Viu is capable of displaying different format images. For example, the following command will display an animated gif image using Viu:

$ viu animated.gif
Display animated images using viu
Display animated images

To exit, just press ++ctrl+c++.

Source:
[3 CLI Image Viewers To Display Images In The Termina](https://ostechnix.com/how-to-display-images-in-the-terminal/)

tags: rust, terminal

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


