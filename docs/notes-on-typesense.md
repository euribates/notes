---
title: Notas sobre Typesense
tags:
    systemd
    linux
    docker
---

## Sobre Typesense

Es un motor de búsqueda libre, escrito en C++. Muy rápido y tolerante a fallos.

- Repositorio: [https://github.com/typesense/typesense](Github typesense)

## Instalar Typesense

En linux:

```shell
curl -O https://dl.typesense.org/releases/0.23.1/typesense-server-0.23.1-amd64.deb
sudo apt install ./typesense-server-0.23.1-amd64.deb
```

Para ver que está instalado y funcionando:

```shell
sudo systemctl status typesense-server.service
```

