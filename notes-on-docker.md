---
title: Notes on Docker
---

## Introduction to Docker

Docker is an open platform for developing, shipping, and running applications.
Docker enables you to separate your applications from your infrastructure so
you can deliver software quickly. With Docker, you can manage your
infrastructure in the same ways you manage your applications. By taking
advantage of Docker’s methodologies for shipping, testing, and deploying code
quickly, you can significantly reduce the delay between writing code and
running it in production.

### How to dockerize Python

- Use python:3.7.3-stretch as the base image, to pin the version and
  OS. Or, python:3.7-stretch if you're feeling less worried about
  point releases.

- Create `requirements.txt` with transitively-pinned versions of all
  dependencies, e.g. by using pip-tools, poetry, or Pipenv.

- If you want fast builds, you want to rely on Docker's layer caching.
  But by copying in the file before running pip install, all later
  layers are invalidated---this image will be rebuilt from scratch
  every time. Solution: Copy in files only when they're first needed.

- By default Docker containers **run as root**, which is a security
  risk. It's much better to run as a non-root user, and do so in the
  image itself so that you don't listen on ports &lt; 1024 or do other
  operations that require a subset of root's permissions.

Here's a somewhat better---though still not ideal---Dockerfile that
addresses the issues above:

```dockerfile
FROM python:3.7.3-stretch

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY yourscript.py .
CMD [ "python", "./yourscript.py" ]
```

Sources:

- [Broken by default: why you should avoid most Dockerfile examples](https://pythonspeed.com/articles/dockerizing-python-is-hard/)
- [regularly rebuild your images without caching to get security updates](https://pythonspeed.com/articles/docker-cache-insecure-images/)
- [Official Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Dockerizing Python Applications](https://stackabuse.com/dockerizing-python-applications/)

tags: python

### How to install ps command

This is the way:

```shell
apt-get update && apt-get install -y procps
```

### Get process stats with the top command

The docker `top` command is exactly what it sounds like: top that runs
in the container:

```shell
$ docker run -d — name=toptest alpine:3.1 watch “echo ‘Testing top’”
fc54369116fe993ae45620415fb5a6376a3069cdab7c206ac5ce3b57006d4241
$ docker top toptest
UID PID … TIME CMD
root 26339 … 00:00:00 watch “echo ‘Testing top’”
root 26370 … 00:00:00 sleep 2
```

Some columns removed to make it fit here. There is also a docker `stats`
command that is basically top for all the containers running on a host.

### View container details (including env vars) with the inspect command

The `inspect` command returns information about a container or an image.
Here's an example of running it on the toptest container from the last
example above:

```shell
$ docker inspect toptest
[
    {
    “Id”: “fdb3008e70892e14d183f8 ... 020cc34fec9703c821”,
    “Created”: “2016–03–23T17:45:01.876121835Z”,
    “Path”: “/bin/sh”,
    “Args”: [
        “-c”,
        “while true; do sleep 2; echo ‘Testing top’; done”
    ],
    … and lots, lots more.
    }
]
```

I've skipped the bulk of the output because there's a lot of it. Some of
the more valuable bits of intelligence you can get are:

- Estado actual del contenedor (En la propiedad `State`)

- La ruta del archivo histórico o `log` (En la propiedad `LogPath`)

- Values of set environment vars. (In the `Config.Env` field.)

- Mapped ports. (In the `NetworkSettings.Ports` field.)

Probably the most valuable use of inspect for me in the past has been
**getting the values of environment vars**. Even with largely automated
deployments I've run into issues in the past where the wrong arg was
passed to a command and a container ended up running with vars set to
incorrect values. When one of your cloud containers starts choking
commands like inspect can be a quick cure.

Source: [Ten Tips for Debugging Docker Contaniers](https://medium.com/@betz.mark/ten-tips-for-debugging-docker-containers-cde4da841a1d)


### How to copy a file from host machine to docker container (or vice versa)

The docker `cp` utility copies the contents of `SRC_PATH` to the `DEST_PATH`.
You can copy from the container's file system to the local machine or the
reverse, from the local filesystem to the container. If `-` is specified for
either the `SRC_PATH` or `DEST_PATH`, you can also stream a tar archive from
`STDIN` or to `STDOUT`. The `CONTAINER` can be a running or stopped
container. The `SRC_PATH` or `DEST_PATH` can be a file or directory.

Examples:

```shell
docker cp foo.txt mycontainer:/foo.txt
docker cp mycontainer:/foo.txt foo.txt
```

More info: [Docker cp command](https://docs.docker.com/engine/reference/commandline/cp/)


### How to run an image changing the entrypoint

Just use the `--entrypoint` option of the `run` command.

Ejample:

```shell
docker run -it --entry-point python colend_app
```

### How to Purge all unused or dangling Images, Containers, Volumes, and Networks

Docker provides a single command that will clean up any resources ---
images, containers, volumes, and networks --- that are dangling (not
associated with a container):

```shell
docker system prune
```

To additionally remove any stopped containers and all unused images (not
just dangling images), add the -a flag to the command:

```
docker system prune -a
```

### How to add a environment variable to a docker

Use the `--env` parameter in `docker run`:

```shell
docker run <image> --env COLEND_ENV=test
```

or use the `ENV` dockerfile command to define the variable inside the
dockerfile.

### Differences between Docker RUN, CMD and ENTRYPOINT

Some Docker instructions look similar and cause confusion among
developers who just started using Docker or do it irregularly. In a
nutshell:

- `RUN` executes command(s) **in a new layer** and creates a new
  image. E.g., it is often used for installing software packages.

- `CMD` sets default command and/or parameters, which can be
  overwritten from command line when docker container runs.

- `ENTRYPOINT` configures a container that will run as an executable.

`RUN` instruction allows you to install your application and packages
requited for it. It executes any commands on top of the current image
and creates a new layer by committing the results. Often you will find
multiple `RUN` instructions in a Dockerfile.

A good illustration of `RUN` instruction would be to install multiple
version control systems packages:

```dockerfile
RUN apt-get update && apt-get install -y \
    bzr \
    cvs \
    git \
    mercurial \
    subversion
```

Note that `apt-get update` and `apt-get install` are executed **in a
single** `RUN` **instruction**. This is done to make sure that the
latest packages will be installed. If `apt-get install` were in a
separate `RUN` instruction, then it would reuse a layer added by
`apt-get update`, which could had been created a long time ago.

`CMD` instruction allows you to set a default command, which will be
executed **only when you run container without specifying a command**.
If Docker container runs with a command, the default command will be
ignored. If Dockerfile has more than one `CMD` instruction, **only
the last one** is executed.

`ENTRYPOINT` instruction allows you to configure a container that will
run as an executable. It looks similar to `CMD`, because it also allows
you to specify a command with parameters. The difference is `ENTRYPOINT`
command and parameters are **not ignored when Docker container runs with
command line parameters** (There is a way to ignore `ENTTRYPOINT`,
thought, if you really need that).

Source: [Yury Pitsishin blog - Docker RUN vs CMD vs ENTRYPOINT](https://goinbigdata.com/docker-run-vs-cmd-vs-entrypoint/)


### Differences between `COPY` and `ADD`

`COPY` and `ADD` are both Dockerfile instructions that serve similar purposes.
They let you copy files from a specific location into a Docker image.

`COPY` takes in a *source* and *destination*. It only lets you copy in a local
file or directory from your host (the machine building the Docker image) into
the Docker image itself.

`ADD` lets you do that too, but it also supports 2 other sources. First, **you
can use a URL instead of a local file / directory**. Secondly, you can
**extract a tar file from the source directly into the destination**.

### Como ejecutar un servidor Apache

Se puede usar la imagen [httpd](https://hub.docker.com/_/httpd) para arrancar
un servidor web apache. En esta imagen no se incluye interprete de PHP, pero
nodebería ser dificl de instalar, aunque para eso quiza mejor usar directamente
una imagen con PHP ya instalado y que incluya su servido web.

La forma más senclla de usar esta imagen es crear un fichero `dockerfile`
sencillo y copiar en la carpeta `public-html/` de la imagen los ficheros
html a publicar.

Un `Dockerfile` sencillo podría ser:

```docker
FROM httpd:2.4
COPY ./public-html/ /usr/local/apache2/htdocs/
```

Ahora podemos crear nuestra propia imagen personalizada y ejecutarla con las
siguientes ordenes:


```shell
$ docker build -t my-apache2 .
$ docker run -dit --name my-running-app -p 8080:80 my-apache2
```

Abre un navegador apuntando a `http://localhost:8080` y comprueba que funciona.

- La opción `-t` en la orden `build` es para asignarle una etiqueta o `tag` a la
  imagen que vamos a crear. Se usa esta etiqueta en la orden `run` para
  identificar la imagen.

- la opción `--name` en la orden `run` le asigna un nombre al contenedor, que es
  por lo general una buena práctica para no tener que usar los identificadores
  hexadecimales generados automáticamente

- la opción `-p` (o en versión larga, `--publish`) es el mapa de puertos que se
  realiza para comunicar el contenedor con el mundo exterior. En este caso
  indicamos que queremos _mapear_ el puerto **8080** del ordenador anfitrión o
  _host_ con el puerto **80** interno de la imagen, que es donde el servidor
  Apache está esperando las peticiones.




### How to run a shell inside an image and log in

If the container is running:

```
docker exec -it <Container ID or name> bash
```

### How to create a Dockerfile

A Dockerfile is essentially a **text file** with clearly defined
instructions on how to build a Docker image for our project.

Next we\'ll create a Docker image based on Ubuntu 16.04 and Python 3.X:

```dockerfile
FROM ubuntu:16.04
MAINTAINER Madhuri Koushik "madhuri@koushik.com"
RUN apt-get update -y && \  
    apt-get install -y python3-pip python3-dev
COPY ./requirements.txt /requirements.txt
WORKDIR /
RUN pip3 install -r requirements.txt
COPY . /
ENTRYPOINT [ "python3" ]
CMD [ "app/app.py" ]  
```

There are a few commands here which deserve a proper explanation:

- `FROM` - Every Dockerfile starts with a FROM keyword. It\'s used to
  specify the base image from which the image is built. The following
  line provides metadata about the maintainer of the image.

- `RUN` - We can add additional content to the image by running
  installation tasks and storing the results of these commands. Here,
  we simply update the package information, install python3 and pip.
  We use pip in the second RUN command to install all packages in the
  requirements.txt file.

- `COPY` - The COPY command is used to copy files/directories from the
  host machine to the container during the build process. In this
  case, we are copying the application files including
  requirements.txt.

- `WORKDIR` - sets the working directory in the container which is
  used by RUN, COPY, etc\...

- `ENTRYPOINT` - Defines the entry point of the application

- `CMD` - Runs the app.py file in the app directory.


### How Docker Images are Built

Docker images are built using the docker `build` command. When building an
image, Docker creates so-called **layers**. Each layer records the changes
resulting from a command in the Dockerfile and the state of the image after
running the command.

Docker internally _caches_ these layers so that when re-building images it
needs to re-create only those layers that have changed. For example, once it
loads the base image for `ubuntu:16.04`, all subsequent builds of the same
container can re-use this since this will not change.  However, during every
re-build, the contents of the app directory will likely be different and thus
this layer will be rebuilt every time.

Whenever any layer is re-built all the layers that follow it in the
Dockerfile need to be rebuilt too. It's important to keep this fact in
mind while creating Dockerfiles. For example, we `COPY` the
`requirements.txt` file first and install dependencies before COPYing
the rest of the app. This results in a Docker layer containing all the
dependencies. This layer need not be re-built even if other files in the
app change as long as there are no new dependencies.

(Si lo hicieramos al contrario, copiar el codigo fuente y luego copiar
el `requirements.txt` y actualizar, cada vez que cambiamos el código fuente
tiene que descartar todas las imagenes generadas a partir de esta, asi
que tendra que copiar de nuevo los requerimientos y volver a instalar).

Thus we optimize the build process for our container by separating the
pip install from the deployment of the rest of our app.

Now that our Dockerfile is ready and we understand how the build process
works, let\'s go ahead and create the Docker image for our app:

```shell
$ docker build -t docker-flask:latest .
```

the `-t` flags is used to tag we will use for this new container. The
dot means to use the file `Dockerfile` in the current directory.


### How to Run an Application in Debug Mode with Auto-Restart

Due to the advantages of containerization described earlier, it makes sense to
develop applications that will be deployed in containers within the container
itself. This ensures that from the beginning, the environment in which the app
is built is clean and thus eliminates surprises during delivery.

However, while developing an app it's important to have quick re-build and
test cycles to check each intermediate step during development. For this
purpose, web-app developers depend on auto-restart facilities provided by
frameworks like Flask. It's possible to leverage this from within the
container as well.

To enable auto-restart, we start the Docker container mapping our development
directory to the app directory within the container. This means Flask will
watch the files in the host (through this mapping) for any changes and restart
the application automatically when it detects any changes.

Additionally, we also need to forward the application ports from the container
to the host. This is to enable a browser running on the host to access the
application.

To achieve this, we start the Docker container with volume-mapping and
port-forwarding options:

```shell
$ docker run --name flaskapp -v$PWD/app:/app -p5000:5000 docker-flask:latest
```

This does the following:

- Starts a container based on the docker-flask image we built
  previously.

- This container's name is set to `flaskapp`. Without the `--name`
  option, Docker chooses an arbitrary (and a very interesting) name
  for the container. Specifying a name explicitly will help us in
  locating the container (for stopping etc.,.)

- The `-v` option mounts the app folder on the host to the container.

- The `-p` option maps the port on the container to the host.

Now the application can be accessed at `http://localhost:5000`
or `http://0.0.0.0:5000/`.


### How to log inside a docker container image running

- First, use `docker ps` to get the name of the existing container, if you
  don't know it.

- Then, use the command:

```shell
docker exec -it <name> /bin/bash
```

Meaning of the flags:

- `-i`, `--interactive` : Keep STDIN open even if not attached
- `-t`, `--tty` : Allocate a pseudo-TTY


### How to know if a docker image is running

If you know the name of te container:

```
docker inspect -f '{{.State.Running}}' $container_name
```

### How to delete the `exited()` images on several runs

This is the way:

```
docker rm $(docker ps -qa --filter status=exited )
```

### How to stop one or more running containers

You can stop one or several containers:

```shell
docker stop [OPTIONS] CONTAINER [CONTAINER...]
```

Where options can be:

- `--time`, `-t` 10 :  Seconds to wait for stop before killing it


### How to remove all images and containers

You use Docker, but working with it created lots of images and
containers. You want to remove all of them to save disk space.

```bash
#!/bin/bash 
# Delete all containers
docker rm $(docker ps -a -q) 
# Delete all images
docker rmi $(docker images -q)
```

Options:

- `--all` , `-a` : Remove all unused images, not just dangling ones
- `--filter` : Provide filter values (e.g. 'until=\')
- `--force` , `-f` : Do not prompt for confirmation


### Why it is recommended to run only one process in a container?

> In many blog posts, and general opinion, there is a saying that goes "one
> process per container". Why does this rule exist? Why not run ntp, nginx,
> uwsgi and more processes in a single container that needs to have all
> processes to work?

Lets forget the high-level architectural and philosophical arguments for a
moment. While there may be some edge cases where multiple functions in a single
container may make sense, there are very practical reasons why you may want to
consider following \"one function per container\" as a rule of thumb:

- **Scaling** containers horizontally **is much easier** if the container is
  isolated to a single function. Need another apache container? Spin one up
  somewhere else. However if my apache container also has my DB, cron and other
  pieces shoehorned in, this complicates things.

- Having a single function per container allows the container to be easily
  **re-used** for other projects or purposes.

- It also makes it more **portable and predictable** for devs to pull down a
  component from production to troubleshoot locally rather than an entire
  application environment.

- **Patching/upgrades** (both the OS and the application) can be done in a more
  **isolated and controlled** manner

- Juggling multiple bits-and-bobs in your container not only makes for larger
  images, but also **ties these components together**. Why have to shut down
  application X and Y just to upgrade Z?

  Above also holds true for code deployments and rollbacks.

- Splitting functions out to multiple containers allows **more flexibility**
  from a security and isolation perspective. You may want (or require) services
  to be isolated on the network level --either physically or within overlay
  networks-- to maintain a strong security posture or comply with things like
  PCI.

- Other more minor factors such as dealing with stdout/stderr and sending logs
  to the container log, keeping containers as ephemeral as possible etc.

Note that I'm saying function, not process. That language is outdated.  The
official docker documentation has moved away from saying "one process" to
instead recommending "one concern" per container.

### What is a Docker volume?

> tldr: The simplest way to describe a Docker volume is this: a Docker volume
> is a folder that exists on the Docker host and is mounted and accessible
> inside a running Docker container. The accessibility goes both ways, allowing
> the contents of that folder to be modified from inside the container, or on
> the Docker host where the folder lives.

Docker uses a special filesystem called a **Union File System**. This is the
key to Docker's layered image model and allows for many of the features that
make using Docker so desirable. However, the one thing that the Union File
System does not provide for is the persistent storage of data.

This is because the layers of a Docker image are read-only. When you run a
container from a Docker image, the Docker daemon creates a new read-write layer
that holds all of the live data that represents your container. When your
container makes changes to its filesystem, those changes go into that
read-write layer. As such, when your container goes away, taking the read-write
layer goes with it, and any and all changes the container made to data within
that layer are deleted and gone forever. That equals non-persistent storage.
Remember, however, that generally speaking this is a good thing. A great thing,
in fact.  Most of the time, this is exactly what we want to happen. Containers
are meant to be ephemeral and their state data is too. However, there are
plenty of use cases for persistent data, such as customer order data for a
shopping site. It would be a pretty bad design if all the order data went
bye-bye if a container crashed or had to be re-stacked.

Enter the Docker volume. The Docker volume is a storage location that is
**completely outside of the Union File System**. As such, it is not bound by the
same rules that are placed on the read-only layers of an image or the
read-write layer of a container. A Docker volume is a storage location that, by
default, is on the host that is running the container that uses the volume.
When the container goes away, either by design or by a catastrophic event, the
Docker volume stays behind and is available to use by other containers. The
Docker volume can be used by more than one container at the same time.

### How to fix some common kwnow problems

#### Every docker command fails with "Error response from daemon: grpc: the connection is unavailable"

The docker daemon is corrupt. Run this command:

```
systemctl restart docker
```

Maybe you'll need to use `sudo` for this.

- Source: <https://forums.docker.com/t/solved-docker-error-response-from-daemon-grpc-the-connection-is-unavailable/32510>


### Learning resources

#### Play with Docker

A simple, interactive and fun playground to learn Docker

- <https://labs.play-with-docker.com/>

#### Play with Docker Classroom

The Play with Docker classroom brings you labs and tutorials that help
you get hands-on experience using Docker. In this classroom you will
find a mix of labs and tutorials that will help Docker users, including
SysAdmins, IT Pros, and Developers. There is a mix of hands-on tutorials
right in the browser, instructions on setting up and using Docker in
your own environment, and resources about best practices for developing
and deploying your own applications.

- <https://training.play-with-docker.com/mvim>
