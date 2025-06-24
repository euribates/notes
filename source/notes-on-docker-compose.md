---
title: Notes on Docker Compose
---

## Introdución a  Docker Compose

Con **docker-compose** podemos ejecutar aplicaciones en un entorno aislado compuesto de contendores y que puede funcionar en cualquier ordenador que tenga  Docker instalado (Ver[[notes-on-docker]]). Esto facilita trabajar y testear las aplicaciones en un entorno lo máß parecido posible al entorno de producción.

El fichero `docker-compose.yaml` gestiona todas las dependencias (bases de datos, sistemas de colas, caché, etc.) y puede crear y arrancar cada contenedor usando una sola orden.


## Ventajas principales de Docker-compose

- **Portability**

  Docker Compose lets you bring up a complete development environment with only
  one command: `docker-compose up`, and tear it down just as easily using
  `docker-compose down`. This allows us developers to keep our development
  environment in one central place and helps us to easily deploy our
  applications.

- **Testing**

  Another great feature of Compose is its support for running unit and E2E
  tests in a quick a repeatable fashion by putting them in their own
  environments. That means that instead of testing the application on your
  local/host OS, you can run an environment that closely resembles the
  production circumstances.


## Estructirua del fichero de composición

El fichero `docker-compose.yml` consiste un multiples niveles que se subdividen usando indentación, en vez de llaves, al usar el formato YAML. Existen **cuatro entradas principales** que prácticamente todo fichero de composición debería tener:

- La versión de la especificación de docker-compose usada en el fichero
- Los servicios que se construiran y arrancarán
- Todos los valúmenes usados
- Las redes que conectan los diferentes servicios.

Un fichero de ejemplo podría ser:

```docker-compose
version: '3.3'

services:
   db:
     image: mysql:5.7
     volumes:
       - db_data:/var/lib/mysql
     restart: always
     environment:
       MYSQL_ROOT_PASSWORD: somewordpress
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD: wordpress

   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     ports:
       - "8000:80"
     restart: always
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD: wordpress
       WORDPRESS_DB_NAME: wordpress
volumes:
    db_data: {}
```

Como se ve en el fichero, se describen dos servicios, un servidor de Wordoress y un serivodr de nases de datos MySQL. Cada uno de los servicios se tratará como un contenedor separado, que puede ser reemplazado cuando sea necesario.


## Conceptos y terminología

The core aspects of the Compose file are its concepts which allow it to manage
and create **a network of containers**.

### Servicios

The services tag contains all the containers which are included in the Compose
file and acts as their parent tag.

### Volúmenes

Volumes are Docker's preferred way of persisting data which is generated and
used by Docker containers. They are completely managed by Docker and can be
used to share data between containers and the Host system.

They do not increase the size of the containers using it, and their context is
independent of the lifecycle of the given container.

There are [multiple types of volumes](https://docs.docker.com/storage/volumes/)
you can use in Docker. They can all be defined using the volumes keyword but
have some minor differences which we will talk about now.

- **Normal Volume**:

  The normal way to use volumes is by just defining a specific path and let the
  Engine create a volume for it. This can be done like this:

  ```
  volumes:
    # Just specify a path and let the Engine create a volume
    - /var/lib/mysql
  ```

- **Path mapping**:

  You can also define absolute path mapping of your volumes by defining the
  path on the host system and mapping it to a container destination using the:
  operator.

  ```
  volumes:
    - /opt/data:/var/lib/mysql
  ```

  Here you define the path of the host system followed by the path of the container.


- **Named volume**:

  Another type of volume is the named volume which is similar do the other
  volumes but has it's own specific name that makes it easier to use on
  multiple containers. That's why it's often used to share data between
  multiple containers and services.
  
  ```docker-compose
  volumes:
    - datavolume:/var/lib/mysql
  ```

### Redes

Instead of only using the default network you can also specify your own
networks within the top-level `networks` key, allowing to create more complex
topologies and specifying network drivers and options.

```dockerfile
networks:
  frontend:
  backend:
    driver: custom-driver
    driver_opts:
      foo: "1"
```

Each container can specify what networks to connect to with the service level
"`networks`" keyword, which takes a list of names referencing entries of  the
top-level "`networks`" keyword.

```
services:
  proxy:
    build: ./proxy
    networks:
      - frontend
  app:
    build: ./app
    networks:
      - frontend
      - backend
  db:
    image: postgres
    networks:
      - backend
```

You can also provide a custom name to your network (since version 3.5):

```
version: "3.5"
networks:
  webapp:
    name: website
    driver: website-driver
```

For a full list of the network configuration options, see the following references:

- [Top-level network key](https://docs.docker.com/compose/compose-file/compose-file-v2/#network-configuration-reference)

- [Service-level network key](https://docs.docker.com/compose/compose-file/compose-file-v2/#networks)

## Docker cli

All the functionality of Docker-Compose is executed through its build in CLI,
which has a very similar set of commands to what is offered by Docker.

- `build`: Build or rebuild services 
- `help`: Get help on a command 
- `kill`: Kill containers 
- `logs`: View output from containers 
- `port`: Print the public port for a port binding 
- `ps`: List containers 
- `pull`: Pulls service images 
- `rm`: Remove stopped containers 
- `run`: Run a one-off command 
- `scale`: Set number of containers for a service 
- `start`: Start services 
- `stop`: Stop services 
- `restart`: Restart services 
- `up`: Create and start containers
- `down`: Stops and removes containers

They are not only similar but also behave like their Docker counterparts. The
only difference is that they affect the entire multi-container architecture
which is defined in the `docker-compose.yml` file instead of a single container.

Some Docker commands are not available anymore and have been replaced with
other commands that make more sense in the context of a completely
multi-container setup. The most important new commands are `docker-compose up`
and `docker-compose down`.

Fuente: [The definitive Guide to Docker compose](https://gabrieltanner.org/blog/docker-compose)
