---
title: Notas sobre rq y django-rq
---

## Qué es rq

Con **[rq](https://python-rq.org/docs/)** tenemos un sistema sencillo de colas,
similar --pero no tan potente-- a otros como
[Celery](https://docs.celeryq.dev/en/stable/),
[RabbitMQ](https://www.rabbitmq.com/), [Kafka](https://kafka.apache.org/intro),
[Amazon SQS](https://aws.amazon.com/es/sqs/) o [MQTT](https://mqtt.org/) entre
otros.

Para nosotros es interesante porque el único requerimiento es Redis, que nosotros
ya estamos usando, y al ser mucho más sencillo que las alternativas, la barrera
de entrada es muy baja.


### Ejemplo de tareas desacopladas 

Vamos a usar solo `rq` para desacoplar una hipotética tarea que lleva mucho
tiempo. Vamos trabajar con el siguiente código, que simula una tarea que toma
entre **2 y 7 segundos**, y que puede fallar un **20%** de las veces:

```
--8<--
./notes/rq/tareas.py
--8<--
```

La función `tarea_pesada_y_falible` simula una función que tarda un tiempo
variable y considerable en ejecutarse, y que, como todas, está sujeta a error.
En este caso simulamos un 20% de posibilidades de que, por la razón que sea, no
pueda terminar correctamente.

Hagamos un primer intento de ejecutar este código 10 veces, para ello definimos
este primer ejemplo, `rq-demo-01.py`:

```
--8<--
./notes/rq/rq-demo-01.py
--8<--
```

Una ejecución típica de este código podría ser la siguiente:

```
tarea_pesada_y_falible (5) ..... [OK]
tarea_pesada_y_falible (4) Hoy no me puedo levantar ♪♫
tarea_pesada_y_falible (4) .... [OK]
tarea_pesada_y_falible (3) ... [OK]
tarea_pesada_y_falible (4) .... [OK]
tarea_pesada_y_falible (3) ... [OK]
tarea_pesada_y_falible (3) ... [OK]
tarea_pesada_y_falible (2) .. [OK]
tarea_pesada_y_falible (5) ..... [OK]
tarea_pesada_y_falible (5) ..... [OK]
He tardado 34 segundos en total
```

Vemos que es este caso hemos tardado **34** segundos (La segunda tarea falló muy
rápidamente, así que no consumió los 4 segundos que en principio habría
tardado).


Vamos ahora a intentar desacoplarla. Lo primero que necesitamos es poder acceder
a un sistema Redis. Con la conexión a redis establecida, podemos empezar a usar al
sistema de colas de `rq`:

```
from redis import Redis
from rq import Queue

REDIS_SERVER = 'localhost'

q = Queue(connection=Redis(REDIS_SERVER))
```

Con el sistema de colas que acabamos de crear, `q`, podemos encolar nuestra
función. Esto lo que hace es, en vez de ejecutarla, ponerla en la cola que
digamos (Si no especificamos ninguna cola se usará la cola por defecto,
`default`)


Es decir, en vez de

```python
tarea_pesada_y_falible(3)
```

Haremos:

```python
result = q.enqueue(tarea_pesada_y_falible, 3)
```

Nuestra versión 2 del programa encola ahora estas llamadas a la función, en vez
de ejecutarlas directamente:

```
--8<--
./notes/rq/rq-demo-02.py
--8<--
```

Ahora, si ejecutamos `rq-demo-02.py`:

```
❯ python ./rq-demo-02.py 
He tardado 0 segundos en total
```

¡Guau! ¡Eso ha sido rápido!

Claro, es rápido porque, en realidad, todavía no se ha hecho ningún trabajo,
simplemente ha puesto en la cola `default` 10 peticiones para que alguien,
cuando pueda, se encargue de ellas.

¿Cómo podemos estar seguros de que cola contiene efectivamente estos
trabajos? Vamos a escribir un sencillo programa que nos muestre el número de
trabajos en las colas `default`, `low` y `high`:

```
--8<--
./notes/rq/rq-demo-03.py
--8<--
```

Con el sistema tal y como lo hemos dejado antes, deberíamos ver 10 peticiones en
la cola `default`. Las colas `low` y `high` (que se crean si no existen
prevamente, como es el caso) tienen que estar vacias.

```
❯ python ./rq-demo-03.py 
default: 10
low: 0
high: 0
```


<section data-markdown>
<textarea data-template>
Muy bien ahora nuestro programa es asombrosamente rápido, las tareas están en
una cola, pero el caso es que siguen sin ejecutarse. Pero esto es muy
fácil de resolver, solo tenemos que arrancar uno o más **workers** que se ocupen
de hacer el trabajo sucio. Con `rq` es muy sencilla, solo hay que ejecutar:
</textarea> 
</section>


Muy bien ahora nuestro programa es muy rápido, las tareas están en
una cola, pero el caso es que siguen sin ejecutarse.

Pero esto es muy
fácil de resolver, solo tenemos que arrancar uno o más **workers** que se ocupen
de hacer el trabajo sucio. Con `rq` es muy sencilla, solo hay que ejecutar:

```
rq worker <nombre de la cola>[, <otra cola>]
```

O, si es la cola por defecto, simplemente:

```
rq worker
```

En nuestro caso, vamos a decirle al _worker_ que procese trabajos en todas las
colas que tenemos definidas ahora mismo, para estar preparados:

```
rq worker high default low
```

Los _workers_ leen los trabajos de las colas indicadas, en el orden indicado.

En nuestro caso, se ejecutaran siempre primero las tareas en la cola `high`,
si no hubiera ninguna se encargará de las tareas en la cola `default`, y solo en
el caso de que las dos anteriores estén vacias se encargará de trabajos en la
cola `low`.

Los nombres de las colas en si no son significativos, lo que importa
es el orden en que se le pasan al _worker_.

Cada _worker_ se encargará de **un único trabajo** cada vez. Dentro del _worker_
no hay procesamiento concurrente, ni _threads_. Si se quiere ejecutar más trabajos
simultaneamente, simplemente hay que arrancar más _workers_.

En producción, obviamente, debemos usar sistemas como **supervisor** o
**systemd** para arrancar los _workers_, pero aquí vamos a arrancarlo
manualmente por calidad.

Vamos entonces a ejecutar el _worker_ y veamos que pasa:

```shell
❯ rq worker high default low
15:09:00 Worker rq:worker:80cb0301fa7d49348063f2c093c8eb5e: started, version 1.11.1
15:09:00 Subscribing to channel rq:pubsub:80cb0301fa7d49348063f2c093c8eb5e
15:09:00 *** Listening on high, default, low...
15:09:00 default: tareas.tarea_pesada_y_falible(4) (9dca76a2-488b-487c-b176-f74413d6aae6)
tarea_pesada_y_falible (4) .... [OK]

[... Omitido por claridad ...]

15:09:24 default: tareas.tarea_pesada_y_falible(6) (a9079de4-33c9-4f2d-b1ec-a11314cca9d5)
tarea_pesada_y_falible (6) 15:09:24 Traceback (most recent call last):
  File "/usr/local/lib/python3.10/dist-packages/rq/worker.py", line 1075, in perform_job
    rv = job.perform()
  File "/usr/local/lib/python3.10/dist-packages/rq/job.py", line 854, in perform
    self._result = self._execute()
  File "/usr/local/lib/python3.10/dist-packages/rq/job.py", line 877, in _execute
    result = self.func(*self.args, **self.kwargs)
  File "/home/jileon/Dropbox/notes/rq/./tareas.py", line 10, in tarea_pesada_y_falible
    raise ValueError("Hoy no me puedo levantar ♪♫")
ValueError: Hoy no me puedo levantar ♪♫
Traceback (most recent call last):
  File "/usr/local/lib/python3.10/dist-packages/rq/worker.py", line 1075, in perform_job
    rv = job.perform()
  File "/usr/local/lib/python3.10/dist-packages/rq/job.py", line 854, in perform
    self._result = self._execute()
  File "/usr/local/lib/python3.10/dist-packages/rq/job.py", line 877, in _execute
    result = self.func(*self.args, **self.kwargs)
  File "/home/jileon/Dropbox/notes/rq/./tareas.py", line 10, in tarea_pesada_y_falible
    raise ValueError("Hoy no me puedo levantar ♪♫")
ValueError: Hoy no me puedo levantar ♪♫
15:09:24 default: tareas.tarea_pesada_y_falible(5) (9f3779ab-1058-4aa6-b746-c54efeba06d4)
tarea_pesada_y_falible (5) ..... [OK]
15:09:29 default: Job OK (9f3779ab-1058-4aa6-b746-c54efeba06d4)
15:09:29 Result is kept for 500 seconds
15:09:29 default: tareas.tarea_pesada_y_falible(6) (10ffd599-c63c-4867-851a-900f6875d405)
tarea_pesada_y_falible (6) ...... [OK]
15:09:35 default: Job OK (10ffd599-c63c-4867-851a-900f6875d405)
15:09:35 Result is kept for 500 seconds

[... Omitido por claridad ...]
```

### Parámetros que podemos usar al encolar una tarea

Además de especificar la cola, se pueden añadir otros parámetros
para especificar el comportamiento. Todos estos valores seran extraidos
con `pop` de los parámetros por nombre (`kwargs`) de la función que queremos
encolar:

- `job_timeout` especifica el tiempo maximo de ejecución de una tarea hasta que
  se la de por fallada. Las unidades por defecto son segundos, y se puede usar o
  bien un entero o una cadena de texto en la que se indique la cantidad y la
  unidad a usar, por ejemplo `'1h'`, `'3m'` o `'5s'`.

- `result_ttl` espedicifica cuanto tiempo se mantendran el estado y los
  resultados de las tareas ejecutadas con éxito. De nuevo la unidad por defecto
  son segundos. El valor por defecto es de **500** segundos. Trascurrido ese
  tiempo los trabajos terminados serán eliminados.

- `ttl` especifica el tiempo máximo que se mantendrá esperando un trabajo en la
  cola. Pasada esa cantidad de tiempo, si el trabajo no se ha ejecutado, se
  descarta. El valor por defecto es `None`, que se interpreta como _para
  siempre_.


- `failure_ttl` es el tiempo máximo durante el cual se mentienen las tareas
  fallidas. El valor por defecto es un año. 

- `depends_on`  especifica uno o más tareas que se deben ejecutar antes de
  encolar esta tarea.

- `job_id` permite especificar manualmente el identificador de la tarea.

- `at_front` pondrá esta tarea en la primera posición de la cola

- `description` añade una descripcion textual de la tarea.

- `on_success` permite ejecutar una función después de que la tarea termine con
  éxito

- `on_failure` permite ejecutar una función después de que la tarea termine con un fallo.

- `args` y `kwargs`: Esto nos permite pasar parámetros por posición y por nombre
  directamente a la función subyacente. Normalmente se usa para pasar algún
  parametro a la función cuyo nombre entrara en conflicto con los parámetros de
  `rq`, como por ejemplo `descriptio` o `ttl`.

### Métodos de las colas

Las colas en si tienen algunos métodos, por ejemplo, vimos que usando la funcion
`len` sobre una cola nos devuelve el número de trabajos en la misma.

Accediendo al atributo `job_ids` obtenemos una lista de los identificadores de
las tareas que están en la cola. Con `jobs` accedes a una lista de las tareas en
si. Se puede usar el método `fetch_job(job_id)` para obtener un trabajo en concreto (por
ejemplo para obtener su resultado) si conocemos su identificador.

El método `empty` nos permite borrar todo el contenido de una cola, mientras que
`delete(job_id)` nos permite borrar una tarea, si conocemos su identificador.


## Como empezar a usar rq y django-rq

### Paso 1: Instalar rq y django-rq

```shell
pip install rq django-rq
```

y añadir `"django_rq"` a la entrada `INSTALLED_APPS` del fichero `settings.py`


### Paso 2: Configurar/definir las colas a usar en `settings.py`

En la configuración del proyecto, tenemos que definir es una variable `RQ_QUEUES` los
parámetros de las colas que vayamos a usar. En el siguiente ejemplo definiremos tres colas:
`default`, `high` y `low` (Los nombres on arbitrarios, usamos estos porque son los que se
usan en la documentación de `rq`). En nuestro fichero settings tenemos definidas las
entradas `REDIS_SERVER', `REDIS_PORT`, `REDIS_DB` y `REDIS_PASSWORD`, y además definimos una
entrada llamada simplemente `REDIS`:

```python
REDIS = f"redis://{REDIS_SERVER}:{REDIS_PORT}/{REDIS_DB}"
```

Con estos valores se simplifica la definición de las colas, ya que solo debemos asignarles
un
nombre, apuntar la entrada `URL` al servidor `REDIS` e indicar la contraseña con la entrada
`PASSWORD`:

```
RQ_QUEUES = {
    'default': {
        'URL': REDIS,
        'PASSWORD': REDIS_PASSWORD,
        'DEFAULT_TIMEOUT': 360,
    },
    'high': {
        'URL': REDIS,
        'PASSWORD': REDIS_PASSWORD,
        'DEFAULT_TIMEOUT': 360,
    },
    'low': {
        'URL': REDIS,
        'PASSWORD': REDIS_PASSWORD,
        'DEFAULT_TIMEOUT': 360,
    },
}
```

### Incluir las urls para la gestión de las colas

En el fichero `urls.py`, incluir una ruta para la administración, por ejemplo:

```
urlpatterns += [
    path('django-rq/', include('django_rq.urls'))
]
```

## Administrar las colas

COn los cambios anteriores, si todo ha ido bien y ejecutamos el `manage.py`,
veremos que nos aparecen nuevas opciones de línea de comandos, que han sido
agregadas por la _app_ `django_rq`:

- `rqenqueue`
- `rqscheduler`
- `rqstats`
- `rqworker`

Ahora nos interesa el `rqstats`, que nos muestra las colas definidas y
estadísticas asociadas con las mismas:

```
❯ ./manage.py rqstats
```

Django RQ CLI Dashboard

------------------------------------------------------------------------------
| Name           |    Queued |    Active |  Deferred |  Finished |   Workers |
------------------------------------------------------------------------------
| default        |         0 |         0 |         0 |         0 |         0 |
| high           |         0 |         0 |         0 |         0 |         0 |
| low            |         0 |         0 |         0 |         0 |         0 |
------------------------------------------------------------------------------
```

POdemos ejecutarlo con la opción `--interval` que nos permite ejcutarlo para
monitorizar de forma continua las colas. El parámetro necesita especificar el
número de segundos entre cada refresco:

```
python manage.py rqstats --interval 5
```

También podemos ejecutar `rqstats` para conseguir la misma información en
formato `json` o `yaml`, con los parámetros `--json` y `--yaml` respectivamente:

```
python manage.py rqstats --json
```

Produce la siguienbte salida (reformateada [ara mayor legibilidad):

```json
{
  "queues": [
    {
      "name": "default",
      "jobs": 0,
      "oldest_job_timestamp": "-",
      "index": 0,
      "connection_kwargs": {
        "db": 0,
        "host": "localhost",
        "port": 6379
      },
      "workers": 0,
      "finished_jobs": 0,
      "started_jobs": 0,
      "deferred_jobs": 0,
      "failed_jobs": 0,
      "scheduled_jobs": 0
    },
    {
      "name": "high",
      "jobs": 0,
      "oldest_job_timestamp": "-",
      "index": 1,
      "connection_kwargs": {
        "db": 0,
        "host": "localhost",
        "port": 6379
      },
      "workers": 0,
      "finished_jobs": 0,
      "started_jobs": 0,
      "deferred_jobs": 0,
      "failed_jobs": 0,
      "scheduled_jobs": 0
    },
    {
      "name": "low",
      "jobs": 0,
      "oldest_job_timestamp": "-",
      "index": 2,
      "connection_kwargs": {
        "db": 0,
        "host": "localhost",
        "port": 6379
      },
      "workers": 0,
      "finished_jobs": 0,
      "started_jobs": 0,
      "deferred_jobs": 0,
      "failed_jobs": 0,
      "scheduled_jobs": 0
    }
  ]
}
```


