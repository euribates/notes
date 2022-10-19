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

Para nosotros es interesante porque el único requerimento es Redis, que nosostros
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
pueda terminar correctamamente.

Hagomos un primer intento de ejecutar este código 10 veces, para ello definimos
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

```
result = q.enqueue(heavy_and_flawed_function, 3)
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

Muy bien ahora nuestro programa es asombrosamente rápido, las tareas están en
una cola, pero el caso es que siguen sin ejecutarse. Pero esto es muy
fácil de resolver, solo tenemos que arrancar uno o más **workers** que se ocupen
de hacer el trabajo sucio. Con `rq` es muy sencilla, solo hay que ejecutar:

```
rq worker <nombre de la cola>[, <otra cola>]
```

O, si es la cola por defecto, simplemente:

```
rq worker
```

En nuestro caso, vamos a decirle al worker que procese trabajos en todas las
colas que tenomos definidas ahora mismo, para estar preparados:

```
rq worker high default low
```

Los _workers_ leeran los trabajos de las colas indicadas, en el orden indicado.
En nuestro caso, se ejecutaran siempre primero las tareas en la cola `high`,
si no hubiera ninguna se encargará de las tareas en la cola `default`, y solo en
el caso de que las dos anteriores estén vacias se encargará de trabajos en la
cola `low`.

Cada _worker_ se encargará de **un único trabajo** cada vez. Dentro del _worker_
no hay procesamiento concurrente, ni threads. Si se quiere ejecutar más trabajos
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
15:09:04 default: Job OK (9dca76a2-488b-487c-b176-f74413d6aae6)
15:09:04 Result is kept for 500 seconds
15:09:04 default: tareas.tarea_pesada_y_falible(6) (23a46523-6870-4416-97af-96f1915469c5)
tarea_pesada_y_falible (6) ...... [OK]
15:09:10 default: Job OK (23a46523-6870-4416-97af-96f1915469c5)
15:09:10 Result is kept for 500 seconds
15:09:10 default: tareas.tarea_pesada_y_falible(2) (b6194437-a741-4fd9-9d52-43712ae5c30e)
tarea_pesada_y_falible (2) .. [OK]
15:09:12 default: Job OK (b6194437-a741-4fd9-9d52-43712ae5c30e)
15:09:12 Result is kept for 500 seconds
15:09:12 default: tareas.tarea_pesada_y_falible(4) (407ff77d-60cf-4cae-abbc-9d4b96c37bc8)
tarea_pesada_y_falible (4) .... [OK]
15:09:16 default: Job OK (407ff77d-60cf-4cae-abbc-9d4b96c37bc8)
15:09:16 Result is kept for 500 seconds
15:09:16 default: tareas.tarea_pesada_y_falible(2) (2279178c-7630-4684-8cbd-02d806549a2e)
tarea_pesada_y_falible (2) .. [OK]
15:09:18 default: Job OK (2279178c-7630-4684-8cbd-02d806549a2e)
15:09:18 Result is kept for 500 seconds
15:09:18 default: tareas.tarea_pesada_y_falible(6) (dbfd9dc6-6535-40f8-acb2-f10c03a298b4)
tarea_pesada_y_falible (6) ...... [OK]
15:09:24 default: Job OK (dbfd9dc6-6535-40f8-acb2-f10c03a298b4)
15:09:24 Result is kept for 500 seconds
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
15:09:35 default: tareas.tarea_pesada_y_falible(4) (166f5bba-1f2b-47c9-b590-be3e20fc2096)
tarea_pesada_y_falible (4) .... [OK]
15:09:39 default: Job OK (166f5bba-1f2b-47c9-b590-be3e20fc2096)
15:09:39 Result is kept for 500 seconds
```


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


