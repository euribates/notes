---
title: Notas sobre RQ y Django-RQ
---

## Qué es RQ (Redis Queue)

Con **[RQ](https://python-rq.org/docs/)** tenemos un sistema sencillo de colas,
similar --aunque no tan potente-- a:

- [Celery](https://docs.celeryq.dev/en/stable/)

- [RabbitMQ](https://www.rabbitmq.com/)

- [Kafka](https://kafka.apache.org/intro)

- [Amazon SQS](https://aws.amazon.com/es/sqs/)

- [MQTT](https://mqtt.org/)

Entre otros.

Para nosotros es interesante porque es muy sencillo y el único requerimiento es
Redis, que nosotros
ya estamos usando, y al ser mucho más sencillo que las alternativas, la barrera
de entrada es muy baja.

- [Documentación de RQ](https://python-rq.org/)

### Ejemplo de tareas desacopladas 

Vamos a usar solo RQ para desacoplar una hipotética tarea que lleva mucho
tiempo. Vamos trabajar con el siguiente código, que simula una tarea que toma
entre **2 y 7 segundos**, y que puede fallar un **20%** de las veces:

```
--8<--
./docs/rq/tareas.py
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
./docs/rq/rq-demo-01.py
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

Vemos que es este caso hemos tardado **34** segundos (La segunda tarea falló
muy rápidamente, así que no consumió los 4 segundos que en principio habría
tardado).

Vamos ahora a intentar desacoplarla. Lo primero que necesitamos es poder
acceder a un sistema _Redis_. Con la conexión a _redis_ establecida, podemos
empezar a usar al sistema de colas de RQ:

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


Es decir, en vez de:

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
./docs/rq/rq-demo-02.py
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
./docs/rq/rq-demo-03.py
--8<--
```

Con el sistema tal y como lo hemos dejado antes, deberíamos ver 10 peticiones en
la cola `default`. Las colas `low` y `high` (que se crean si no existen
previamente, como es el caso) tienen que estar vacías.

```
❯ python ./rq-demo-03.py 
default: 10
low: 0
high: 0
```

## Cómo arrancar los _workers_

Muy bien ahora nuestro programa es muy rápido, las tareas están en una cola,
pero el caso es que siguen sin ejecutarse.  Pero esto es muy fácil de resolver,
solo tenemos que arrancar uno o más **workers** que se ocupen de hacer el
trabajo sucio. Con RQ es muy sencillo, solo hay que ejecutar:

```
rq worker <nombre de la cola>[, <otra cola>]
```

O, si solo usamos la cola por defecto, simplemente:

```
rq worker
```

En nuestro caso, vamos a decirle al _worker_ que procese trabajos en todas las
colas que tenemos definidas ahora mismo, para estar preparados:

```
rq worker high default low
```

Los _workers_ leen los trabajos de las colas indicadas, en el orden indicado.

En nuestro caso, se ejecutarán siempre primero las tareas en la cola `high`,
si no hubiera ninguna se encargará de las tareas en la cola `default`, y solo en
el caso de que las dos anteriores estén vacías se encargará de trabajos en la
cola `low`.

Los nombres de las colas en si **no son significativos**, lo que importa
es **el orden** en que se le pasan al _worker_.

Cada _worker_ se encargará de **un único trabajo** cada vez. Dentro del _worker_
no hay procesamiento concurrente, ni _threads_. Si se quiere ejecutar más trabajos
simultáneamente, solo hay que arrancar más _workers_.

En producción, obviamente, debemos usar sistemas como **supervisor** o
**systemd** para arrancar los _workers_, pero aquí vamos a arrancarlo
manualmente por simplicidad.

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

## Métodos y propiedades de las colas en RQ

Las colas en si tienen algunos métodos y atributos. Ya vimos en los ejemplos
que la funcion `len` sobre una cola nos devuelve el número de trabajos en la
misma.

- `job_ids`: Accediendo al atributo `job_ids` obtenemos una lista de los
  identificadores de las tareas que están en la cola.

- `jobs`: Con el atributo `jobs` accedes a una lista de las tareas en si.

- `fetch_job(job_id)`: Se puede usar este método para obtener un trabajo en
  concreto (por ejemplo para obtener su resultado), a partir de su
  identificador.

- `empty()`: Borra todo el contenido de una cola

- `delete(job_id)`: Borra una tarea, conocido su identificador.


## Cómo Administrar las colas en _rq_

Con los cambios anteriores, si todo ha ido bien y ejecutamos el `manage.py`,
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

Django RQ CLI Dashboard:

```
------------------------------------------------------------------------------
| Name           |    Queued |    Active |  Deferred |  Finished |   Workers |
------------------------------------------------------------------------------
| default        |         0 |         0 |         0 |         0 |         0 |
| high           |         0 |         0 |         0 |         0 |         0 |
| low            |         0 |         0 |         0 |         0 |         0 |
------------------------------------------------------------------------------
```

Podemos ejecutarlo con la opción `--interval` que nos permite ejecutarlo para
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

Produce la siguiente salida (reformateada para mayor legibilidad):

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

## Cómo ejecutar los _workers_

Para que los trabajadores empiezan a trabajar, debemos ejecutarlos desde
el mismo directorio que el proyecto, especialmente si tenemos que usar
librerías de terceros. En este caso, también es ideal que se ejecuten en el
mismo entrono virtual.

Para arrancar un _worker_, hacemos simplemente:

```shell
$ rq worker high default low
```

Que producirá algo similar a:

```
*** Listening for work on high, default, low
```

Obsérvese que los nombres de las colas se especifican en la línea de comandos.
Mientras el _worker_ esté en ejecución, seguirá leyendo trabajos de las colas
(en el orden indicado, esto es importante) y ejecutándolos, en un bucle continuo.

Cada _worker_ procesara un único trabajo cada vez. Si no hay ningún _worker_ en
ejecución, no habrá procesamiento concurrente. Podemos tener más de un
_worker_ funcionando a la vez, el sistema evitará que se pisen entre si.


## Por qué es importante el orden de las colas en _rq_

Los _workers_ procesan las colas en el orden que se les indica. Esto significa
que, por ejemplo, si hemos invocado al _worker_ con estos parámetros:

```shell
$ rq worker high default low
```

Este empezará a procesar los trabajos que encuentre en la cola `high`.
Solo cuando esta cola esté vacía empezará con la cola `default`, y solo cuando
ambas colas `high` y `default` estén vacías, empezará con los trabajos de
la cola `low`.


## Cómo arrancar _workers_ en mode _burst_ (Una sola pasada)

Por defecto, los _workers_ empiezan a trabajar inmediatamente, y entran en un
estado de _bloqueo en espera_ cuando se quedan sin trabajos que procesar. Este
es el modo ideal si los estamos usando en un sistema de gestión de procesos
como `supervisor` o `systemd`.

Pero podemos usar el _worker_ con el _flag_ `--burst` para que ejecuten toda la
carga de trabajo que encuentren al arrancar y, cuando la cola o colas que
atienden estén vacías, en vez de quedarse en espera, simplemente terminen su
ejecución. Este puede resultar útil para desarrollo, para trabajos en bloque
que tiene que ejecutarse de forma periódica, o para escalar el conjunto de
_workers_ de forma temporal ante un incremento grande de la carga de trabajo.

```
$ rq worker --burst high default low

*** Listening for work on high, default, low
Got send_newsletter('me@nvie.com') from default
Job ended normally without result
No more work, burst finished.
Registering death.
```

## Cómo usar _rq_ con Django

La mejor opción es [django-rq](https://github.com/rq/django-rq). Es una _app_
que nos permite configurar las colas dentro del fichero `settings.py`, y además
nos proporciona varios comandos y utilidades para usar RQ desde Django.

Para usarlo:

- Instalar django-rq: `pip install django-rq`

- Añadirlo a la lista de _apps_ instaladas

    ```py
    INSTALLED_APPS = (
        # other apps
        "django_rq",
    )   
    ```

- Configurar las colas en el fichero `settings.py`

    ```py
    RQ_QUEUES = {
        'default': {
            'HOST': 'localhost',
            'PORT': 6379,
            'DB': 0,
            'USERNAME': 'some-user',
            'PASSWORD': 'some-password',
            'DEFAULT_TIMEOUT': 360,
            'REDIS_CLIENT_KWARGS': {    # Eventual additional Redis connection arguments
                'ssl_cert_reqs': None,
            },
        },
        'high': {
            'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'),
            'DEFAULT_TIMEOUT': 500,
        },
        'low': {
            'HOST': 'localhost',
            'PORT': 6379,
            'DB': 0,
        },
    }
    ```

- Incluir `django_rq.urls` en el fichero de rutas `urls.py`:

```py
urlpatterns += [
    ...
    path('django-rq/', include('django_rq.urls'))
]
```

## Como configurar/definir las colas a usar en Djago/RQ

En la configuración del proyecto, tenemos que definir es una variable
`RQ_QUEUES` los parámetros de las colas que vayamos a usar. En el siguiente
ejemplo definiremos tres colas: `default`, `high` y `low` (Los nombres son
arbitrarios, estos son los que se usan en la documentación de
RQ). En nuestro fichero `settings,py` tenemos definidas las entradas
`REDIS_SERVER`, `REDIS_PORT`, `REDIS_DB` y `REDIS_PASSWORD`, y además definimos
una entrada llamada simplemente `REDIS`:

```python
REDIS = f"redis://{REDIS_SERVER}:{REDIS_PORT}/{REDIS_DB}"
```

Con estos valores se simplifica la definición de las colas, ya que solo debemos
asignarles un nombre, apuntar la entrada `URL` al servidor `REDIS` e indicar la
contraseña con la entrada `PASSWORD`:

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

## Cómo encolar una tarea usando RQ

Para encolar una tarea o job partimos de una función normal en Python, por
ejemplo:

```py
import requests

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())
```

En principio, es una función corriente. Pero hay que tener en cuenta que este
código va a ser ejecutado en un momento diferente, en un proceso diferente y
probablemente en una máquina diferente, así que  **no puede depender de
variables de contexto, globales, etc**. Además, tanto el código a ejecutar como
los valores de los parámetros van a ser serializados para almacenarlos en la
cola, así que **no debemos usar como parámetros valores no serializables**. Por
ejemplo, un manejador de un fichero abierto es propio del entorno y no
serializable.

En la práctica, es mejor limitarse a usar tipos simples en los parámetros. Si
quieramos pasar como parámetro, por ejemplo, la conexión a la base de datos, es
mejor y más simple pasarle la cadena de texto o los parámetros de conexión, y
que el proceso realiza la suya propia.

Volviendo al tema inicial, para encolar un trabajo en rq, partimos de
una función normal, como el ejemplo anterior, `count_words_at_url`.
Para encolarla, tenemos que:

- Almacenar la función en un fichero `.py` aparte, que podamos importar. Con
  _rq_ no podemos serializar el código de una función que no esté en un módulo
  propio.

- Definir la cola en la que queremos poner el trabajo. Si no especificamos
  nada, la cola sera `default`.

Supojiendo que hemos guardado nuestra función de ejemplo en un fichero
`somewhere.py`, podriamos hacer algo como esto:

```py
import time
from rq import Queue
from redis import Redis
from somewhere import count_words_at_url

redis_conn = Redis()              # Conseguir una conexión a Redis
q = Queue(connection=redis_conn)  # Obtener acceso a una cola

job = q.enqueue(count_words_at_url, 'http://nvie.com')

print(job.result)        # Normalmente `None`, no ha podido terminar
time.sleep(5)            # Esperamos un poco a que el worker termina

print(job.result)
```

Si queremos el trabajo encolado en una cola diferente de `defaaul`, hariamos el
siguiente cambio:

```py
q = Queue('low', connection=redis_conn)
q.enqueue(count_words_at_url, 'http://nvie.com')
```

## Que opciones tenemos disponibles a la hora de encolar un trabajo en _rq_






Hay muchas opciones interesantes que podemos usar cuando encolamos un trabajo.
Todos estos valores serán extraidos con `pop` de los parámetros por nombre
(`kwargs`) de la función que queremos encolar, d forma que no llegan a la
función subyacente: :

- `job_timeout` espedifica el tiempo máximo de ejecución que se le permite a un
  _worker_. Pasado este tiempo, el proceso se interrumpe y se marca como
  fallido. Podemos usar como valor o bien un entero, indicando el número de
  segundos, o una cadena de texto que incluya un número y un sufijo
  especificando una unidad de tiempo de horas `h`, minutos (`m`) o segundos
  (`s`). Por ejemplo serían valores váłidos `'1h'`, `'30m` o `15s`.

- `result_ttl` especifica el tiempo, en segundos, durante el cual se mantien un
  resultado de un trabajo finalizado con éxito. Por defecto esta establecido a
  **500 segundos**.  Trascurrido ese tiempo los trabajos terminados serán
  eliminados.

- `failure_ttl` es el tiempo máximo durante el cual se mentienen las tareas
  fallidas. El valor por defecto es un año. 

- `ttl` especifica el máximo tiempo que se mantiene un trabajo en la cola antes
  de descartarlo. Pasada esa cantidad de tiempo, si el trabajo no se ha ejecutado, se
  descarta. Por defecto tiene el valor `None` lo que significa que no se
  descartan nunca y, por tanto, los trabajos permaneceran en la cola hasta que
  o bien se ejecuten conéxito o se descaraten manualmente.

- `on_success` permite especificar una función que se ejecutará despues de que
  un trabajo haya finalizado con éxito.

- `on_failure`, de forma similar, permite especificar una función que se
  ejecutará despues de que un trabajo haya finalizado sin éxito.

- `job_id` nos permite establecer el identificador de un trabajo manualmente.

- `at_front` permite posicionar el trabajo al principio de la cola, en vez de
  al final, como sería lo normal.

- `description` permite añadir una descripcion opcional al trabajo.

- `depends_on`  especifica uno o más tareas que se deben ejecutar antes de
  encolar esta tarea.

- `args` y `kwargs`: Estos parámetros nos permiten especificar directamente los
  argumentos posicionales o por nombre a pasar a la función subyacente.  Esto
  resulta útil si alguno de los paráetros que acepta la función
  entra en conflicto con alguno de los que hemos visto para `enqueue`,
  como por ejemplo `description` o `ttl`.


## Qué serializador usa RQ. ¿Se puede cambiar?

El serializador por defecto en RQ es
[pickle](https://docs.python.org/3/library/pickle.html). Aunque se pueden usar
otros serializadores, _pickle_ tienen la ventaja de estar incluido de serie con
Python y además soporta más tipos de datos que, por ejemplo, json. Pero no todo
son ventajas. En la documentación oficial enlazada se describen con más detalle
las diferencias y capacidades de _Piclle_ y _Json_.

!!! Note "Serializar objetos con Pickle

    En la documentación oficial hay un apartado sobre el protocolo
    que debemos implementar en nuestras clases para que puedan ser
    serializables por Pickle. Resumiendo mucho, tenemos que implementar dos
    métodos, `__getstate__` y `__setstate__`. No obstante, es un tema
    complicado y hay ciertas peculiaridades que convienen consultar en la
    documentación.
