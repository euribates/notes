---
title: Nontas sobre Samba (SMB server)
---

## Sobre Samba

## Cómo empezar con Samba

Fuente:

- [Samba on Linux the easy way - Gloves Off Linux](https://glovesoff.substack.com/p/samba-on-linux-the-easy-way)


## Cómo usar credenciales para conectarse a unidades de disco sin password

we'll provide the credentials required in an external file. The file
contains the required username and password and we can restrict the file
to be only readable by root. The fstab-entry contains only the path to
the file.

The file providing the credentials which is made only readable by root:

```shell 
$ sudo vi /root/.smbcred
$ sudo cat /root/.smbcred username=username password=secret
$ sudo chmod 600 /root/.smbcred
$ sudo ls -al /root/.smbcred
-rw-------. 1 root root 36 Sep 9 15:43 /root/.smbcred
```

The line to automatically mount the share on boot in `/etc/fstab`:

```shell
$ cat /etc/fstab|grep /mnt //192.168.202.2/drive_e
/mnt  cifs  credentials=/root/.smbcred  0 0
```

The line in /etc/fstab consists out of 6 parts:

- the remote location ([//192.168.202.2/drive_e]{.title-ref})

- the local mountpoint ([/mnt]{.title-ref})

- the type of filesystem ([cifs]{.title-ref})

- the options ([credentials=/root/.smbcred]{.title-ref})

- dump-option ([0]{.title-ref})

- check/pass-option ([0]{.title-ref})

After adding the above line, we can simply mount our share without
providing credentials. On top of that, the share should be mounted at
boot time automatically

Sources:

- [Mount Windows (CIFS) shares on Linux with credentials in a secure way](https://jensd.be/229/linux/mount-windows-cifs-shares-on-linux-with-credentials-in-a-secure-way)

## Compartir carpetas con Samba en Linux Mint

Primero, instalar Samba:

```shell
sudo apt install samba
```

Para hacer el sistema "descubrible" y accesible para Windows 7 y superior, hay
que instalar [`wsdd`](https://github.com/christgau/wsdd):

```shell
sudo apt install wsdd
```

Para verificar que el demonion está ejecutandose:

```shell
sudo service wsdd status
```

En Windows 8, 10, 11, también se puede conectar al servidor usado su nombre
`mDNS`, que es solo el _host name_ con el sufifo `.local` (`\\nova.local`).


Para hacer el sistema "descubrible" y accesible para MaxOS hay que instalar:

```shell
sudo apt install avahi-daemon
```

Pata verificar que está activo:

```shell
sudo service avahi-daemon status
```

Fuente: [Share Folders using Samba in Home Network with Mint 21 - Linux Mint Forums](https://forums.linuxmint.com/viewtopic.php?t=377372)
