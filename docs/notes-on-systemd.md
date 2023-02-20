---
title: Notas sobre Systemd
---

## Qué es Systemd

**[Systemd](https://es.wikipedia.org/wiki/Systemd)** es un sistema de
inicialización (_init_) usado por varias distribuciones de Linux. El sistema de
inicialización se ocupa de arrancar los componentes del sistema que deben
ejecutarse después de que el kernel ya haya arrancado. Además, debe ocuparse de
gestionar a los servicios y
**[daemons](https://es.wikipedia.org/wiki/Daemon_%28computing%29)**.


El comando `systemctl` es la herramienta principal para gestionar `systemd`.
Con respecto a los servicios o _daemons_, las opciones más usadas típicas son
arrancar un servicio (`start`), pararlo (`stop`), reiniciarlo (`restart`) y
habilitarlo para que se arranque automáticamente al inicio, o no (`enable` y
`disable`).


## Unidades

En _Systemd_, el objetivo de la mayoría de las acciones es conocido como
**unidades** o **units**, que son recursos que el sistema conoce y sabe como
gestionar. Las unidades se dividen en categorías basadas en los tipos de
recursos que representan y se definen con ficheros conocidos como ficheros de
unidades (_Unit files_). Se puede deducir el tipo de cada unidad por el sufijo
usado en el nombre del fichero.

Para unidades de gestión de servicios, el sufijo es `.service`, pero en la
mayoría de los casos no necesitaremos incluirlo, `systemd` asumirá esta
terminación por defecto. Por ejemplo, para gestionar el _deamon_ `nginx` no hace
falta escribir `nginx.service`, aunque se puede hacer; basta con `ngigx`.


## Como listar todos los servicios en ejecución

Si ejecutamos el comando `systemctl` sin ningún parámetro, el programa listará
**todas** las unidades que conozca, incluyendo los servicios, mostrando además
un indicador de estado que nos indicará si la unidad está activa o no.

Para seleccionar solo los servicios, usaremos el subcomando `list-units`, y con
el parámetro `--type` indicamos el valor `service`:

```shell
systemctl list-units --type=service
```

Podemos filtrar también por el estado con el parámetro `--state`, por ejemplo
para ver solo los servicios activos:

```shell
systemctl list-units --type=service --state=active
```

Podemos indicar varios estados, separados por coma:

```shell
systemctl list-units --type=service --state=active,failed
```

Fuente: [TecMint - How to List All Running Services Under Systemd in Linux](https://www.tecmint.com/list-all-running-services-under-systemd-in-linux/)


## Arrancando y parando servicios

Para arrancar un servicio, cuyas instrucciones de ejecución están detalladas en
el fichero de unidad, se usa el comando `**start**`. Hacen falta privilegios
de `root` para esto, así que normalmente usaremos la orden `sudo`:

```shell
sudo systemctl start servicio.service
```

O, como comentamos antes, omitiendo el sufijo `.service`:

```shell
sudo systemctl start servicio
```

Para pararlo, usaremos el subcomando `**stop**`:

```shell
sudo systemctl stop servicio
```

## Rearranque y recarga

Para arrancar de nuevo un servicio, es decir, para pararlo y volverlo a
arrancar, podemos usar el comando `**restart*`:

```shell
sudo systemctl restart servicio
```

En aquellos casos en que el sistema sea capaz de hacer un arranque en caliente,
es decir, que sea capaz de cargar de nuevo su configuración y continuar
trabajando los nuevos valores, podemos usar la orden `**reload**`:

```shell
sudo systemctl reload servicio
```

Por lo general es siempre preferible hacer un arranque en caliente, pero si no
estamos seguros de si el servicio lo soporta, podemos usar la orden
**`reload-or-restart`**:

```shell
sudo systemctl reload-or-restart servicio
```

- Source: [How To Use Systemctl to Manage Systemd Services and Units  | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units)

## Cómo listar todas las unidades activas gestionadas por systemd

Ejecutamos el comando:

```
sudo systemctl list-units
```

- [Cómo listar todas las unidades de servicios de systemd - Foro Vozidea.com](https://foro.vozidea.com/d/13-como-listar-todas-las-unidades-de-servicios-de-systemd)


## How to see full log from systemctl status service?

Just use the journalctl command, as in:

```shell
journalctl -u service-name.service
```

Or, to see only log messages for the current boot:

```shell
journalctl -u service-name.service -b
```


