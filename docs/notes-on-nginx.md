---
title: Notas sobre nginx
tags:
    - web
---

## Nginx

**Nginx** es un servidor web/proxy inverso ligero de alto rendimiento y un
proxy para protocolos de correo electrónico. Es software libre y de
código abierto, licenciado bajo la Licencia BSD simplificada; también existe
una versión comercial distribuida bajo el nombre de Nginx Plus.


## Increase Request Timeout in NGINX

For example, you want to increase request timeout to 300 seconds. Then you need
to add `proxy_read_timeout`, `proxy_connect_timeout`, `proxy_send_timeout` directives
to http or server block. Here the http block allows the changes in all server
in NGINX.

To make changes for all servers, edit the NGINX main configuration file and add
the following content under `http` block.

```
http{
   ...
   proxy_read_timeout 300;
   proxy_connect_timeout 300;
   proxy_send_timeout 300;
   ...
}
```

In case, you just want to increase request timeout for a specific server or
subdomain, then add the directives for its server block only. Edit the specific
server block configuration file and add the following settings:

```
server{
   ...
   proxy_read_timeout 300;
   proxy_connect_timeout 300;
   proxy_send_timeout 300; 
   ...
}
```

After making the changes, you must restart the NGINX service to apply changes:

```shell
sudo systemctl restart nginx 
```

Fuente: [How to Increase Request Timeout in NGINX &ndash; TecAdmin](https://tecadmin.net/increase-request-timeout-in-nginx/)
