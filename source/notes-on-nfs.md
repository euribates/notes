---
title: Notas sobre NFS
---

## Cómo montar una unidad NFS

Para montar NFS:

```bash
sudo mount -t nfs <nfs_server>:/web /mnt/static 
```

## The /etc/exports file

The file `/etc/exports` contains a table of local physical file systems
on an NFS server that are accessible to NFS clients. The contents of the
file are maintained by the server\'s system administrator.

Each file system in this table has a list of options and an access
control list. The table is used by exportfs(8) to give information to
mountd(8).

Each line contains an export point and a whitespace-separated list of
clients allowed to mount the file system at that point. Each listed
client may be immediately followed by a parenthesized, comma-separated
list of export options for that client. No whitespace is permitted
between a client and its option list.

Also, each line may have one or more specifications for default options
after the path name, in the form of a dash (\"-\") followed by an option
list. The option list is used for all subsequent exports on that line
only.

Blank lines are ignored. A pound sign (\"\#\") introduces a comment to
the end of the line. Entries may be continued across newlines using a
backslash. If an export name contains spaces it should be quoted using
double quotes. You can also specify spaces or other unusual character in
the export name using a backslash followed by the character code as
three octal digits.

Ejemplo de fichero /etc/exports:

    # sample /etc/exports file
    /               master(rw) trusty(rw,no_root_squash)
    /projects       proj*.local.domain(rw)
    /usr            *.local.domain(ro) @trusted(rw)
    /home/joe       pc001(rw,all_squash,anonuid=150,anongid=100)
    /pub            *(ro,insecure,all_squash)
    /srv/www        -sync,rw server @trusted @external(ro)
    /foo            2001:db8:9:e54::/64(rw) 192.0.2.0/24(rw)
    /build          buildhost[0-9].local.domain(rw)

The first line exports the entire filesystem to machines `master` and
`trusty`. In addition to write access, all uid squashing is turned off
for host trusty.

The second and third entry show examples for wildcard hostnames and
netgroups (this is the entry `'@trusted'`).

The fourth line shows the entry for a PC/NFS client.

Line 5 exports the public FTP directory to every host in the world,
executing all requests under the nobody account. The insecure option in
this entry also allows clients with NFS implementations that don\'t use
a reserved port for NFS.

The sixth line exports a directory read-write to the machine \'server\'
as well as the \'\@trusted\' netgroup, and read-only to netgroup
\'\@external\', all three mounts with the \'sync\' option enabled.

The seventh line exports a directory to both an IPv6 and an IPv4 subnet.

The eighth line demonstrates a character class wildcard match


## Machine name formats

NFS clients may be specified in a number of ways:

single host

> You may specify a host either by an abbreviated name recognized be the
> resolver, the fully qualified domain name, an IPv4 address, or an IPv6
> address. IPv6 addresses must not be inside square brackets in
> /etc/exports lest they be confused with character-class wildcard
> matches.

netgroups

> NIS netgroups may be given as \@group. Only the host part of each
> netgroup members is consider in checking for membership. Empty host
> parts or those containing a single dash (-) are ignored.

wildcards

> +Machine names may contain the wildcard characters \* and ?, or may
> contain character class lists within \[square brackets\]. This can be
> used to make the exports file more compact; for instance,
> `*.cs.foo.edu` matches all hosts in the domain `cs.foo.edu`. As these
> characters also match the dots in a domain name, the given pattern
> will also match all hosts within any subdomain of `cs.foo.edu`.

IP networks

> You can also export directories to all hosts on an IP (sub-) network
> simultaneously. This is done by specifying an IP address and netmask
> pair as address/netmask where the netmask can be specified in
> dotted-decimal format, or as a contiguous mask length.
>
> For example, either `'/255.255.252.0'` or `'/22'` appended to the
> network base IPv4 address results in identical subnetworks with 10
> bits of host. IPv6 addresses must use a contiguous mask length and
> must not be inside square brackets to avoid confusion with
> character-class wildcards. Wildcard characters generally do not work
> on IP addresses, though they may work by accident when reverse DNS
> lookups fail.


## Ejecutar un servidor NFS con Docker
-----------------------------------

Necesitamos un servidor de la version 3 del protocolo. Esta imagen de
docker esta preparada para NFSv3 y NFSv4:

```
https://hub.docker.com/r/erichough/nfs-server/
```

Este es el comando basico para ejecutar:

```bash
docker run -v /host/path/to/shared/files:/some/container/path -v
/host/path/to/exports.txt:/etc/exports:ro \--cap-add SYS\_ADMIN -p
2049:2049 -p 2049:2049 -p 2049:2049/udp -p 111:111 -p 111:111/udp -p
32765:32765 -p 32765:32765/udp -p 32767:32767 -p 32767:32767/udp
erichough/nfs-server
```

### El fichero exports

El fichero principal de configuracion de NFS es `/etc/exports`. En este
fichero se especifican que directorios van a ser compartidos con los
clientes NFS. La sintaxis del fichero es:

```
    Directory      hostname(options)
```

Donde `Directory` debe sustituirse por la ruta del directorio que
queremos compatir (Por ejemplo `/usr/shares/doc`). El valor de
`hostname` indica la dirección o direcciones de los clientes que tienen
permitido el acceso. Puede usarse direcciones IP o nmobres. El campo de
`opcions` se utiliza para especificar el modo de acceso, solo lectura
(`ro`) o lectura y escritura (`rw`).

Por ejemplo, la siguiente entrada comparte el directorio
`/etc/shares/doc` con los clientes `client01` (con acceso completo de
lectura y escritura) y con `client02` (Con acceso de solo lectura):

```
    /usr/shares/doc      client01(rw) client02(ro)
```

The value of Directory should be replaced with the name of the directory
you want to share (for example, /usr/share/doc). The value hostname
should be a client hostname that can be resolved into an IP address. The
options value is used to specify how the resource should be shared.

```bash
> docker run -v /home/jileon/Dropbox/<notes:/var/shares/notes> -v
> /home/jileon/workarea/euribates/agnostic-file-stores/exports.txt:/etc/exports:ro
> \--cap-add SYS\_ADMIN -p 2049:2049 -p 2049:2049 -p 2049:2049/udp -p
> 111:111 -p 111:111/udp -p 32765:32765 -p 32765:32765/udp -p
> 32767:32767 -p 32767:32767/udp erichough/nfs-server
```
