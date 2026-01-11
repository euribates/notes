Nginx
========================================================================

.. tags:: web, devops


Nginx
-----

**Nginx** es un servidor web/proxy inverso ligero de alto rendimiento y
un proxy para protocolos de correo electrónico. Es software libre y de
código abierto, licenciado bajo la Licencia BSD simplificada; también
existe una versión comercial distribuida bajo el nombre de Nginx Plus.

Increase Request Timeout in NGINX
------------------------------------------------------------------------

For example, you want to increase request timeout to 300 seconds. Then
you need to add ``proxy_read_timeout``, ``proxy_connect_timeout``,
``proxy_send_timeout`` directives to http or server block. Here the http
block allows the changes in all server in NGINX.

To make changes for all servers, edit the NGINX main configuration file
and add the following content under ``http`` block.

.. code::

    http {
        ...
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        ...
    }

In case, you just want to increase request timeout for a specific server
or subdomain, then add the directives for its server block only. Edit
the specific server block configuration file and add the following
settings:

.. code::

    server{
        ...
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        ...
    }

After making the changes, you must restart the NGINX service to apply
changes:

.. code:: shell

    sudo systemctl restart nginx

Fuente: `How to Increase Request Timeout in NGINX – TecAdmin <https://tecadmin.net/increase-request-timeout-in-nginx/>`_


Cómo comprobar si el fichero de configuración de nginx es correcto
------------------------------------------------------------------------

Se puede ejecutar:

.. code:: shell

    nginx -t


Cómo saber que version de nginx tengo instalada
-----------------------------------------------

Desde la línea de comandos:

.. code:: shell

    nginx -v


Como instalar php con nginx
---------------------------

Suponemos instalado nginx, si no:

.. code:: shell

    sudo apt-get install nginx -y
    sudo systemctl start nginx
    sudo systemctl enable nginx

Instalamos PHP 7.4:

.. code:: shell

    sudo apt-get install php7.4 -y
    php --version

Debería devolver:

.. code::

    PHP 7.4.3-4ubuntu2.19 (cli) (built: Jun 27 2023 15:49:59) ( NTS )
    Copyright (c) The PHP Group
    Zend Engine v3.4.0, Copyright (c) Zend Technologies
    with Zend OPcache v7.4.3-4ubuntu2.19, Copyright (c), by Zend Technologies

Instalar PHP7.4-FPM y otras extensiones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nginx no procesa directamente PHP, es necesario instalar PHP-FPM, que es
una alternativa PHP a FastCGI, con algunas funcionmalidades adicionales
para sitios con mucha carga.

.. code:: shell

    sudo apt install php7.4-fpm php7.4-cli php7.4-mysql php7.4-curl php7.4-json -y

Y si todo ha ido bien, lo activamos:

.. code:: shell

    sudo systemctl start php7.4-fpm
    sudo systemctl enable php7.4-fpm

Fuente: | `How to install PHP 7.4 With Nginx on Ubuntu 20.04 - RoseHosting <https://www.rosehosting.com/blog/how-to-install-php-7-4-with-nginx-on-ubuntu-20-04/>`_
