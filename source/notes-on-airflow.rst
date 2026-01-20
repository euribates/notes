Sobre  airflow
========================================================================

:index:`Apache Airflow` es una plataforma de gestión de flujo de trabajo
de código abierto escrita en Python, donde los flujos de trabajo se crean
a través de *scripts* de Python.

Fue creada por Airbnb en octubre de 2014 como solución para la gestión de
flujos de trabajo dentro de la empresa.  Desde el principio, el proyecto
fue distribuido como código abierto, se convirtió en un proyecto de la
Incubadora de Apache en marzo de 2016 y un proyecto de software de nivel
superior de la Fundación Apache en enero de 2019.

Visión general de Apache Airflow
------------------------------------------------------------------------

Airflow utiliza **grafos acíclicos dirigidos** (DAG) para gestionar la
orquestación del flujo de trabajo. Las tareas y dependencias se definen en
Python y luego Airflow gestiona la programación de tareas y la ejecución.

Los DAG se pueden ejecutar en un horario definido (por ejemplo, cada hora
o cada día) o en función de la ocurrencia de eventos externos (por
ejemplo, un archivo que aparece en Hive). Los programadores anteriores
basados en DAG como Oozie y Azkaban tendían a depender de múltiples
archivos de configuración y árboles del sistema de archivos para crear un
DAG, mientras que en Airflow, los DAG a menudo se pueden escribir en un
solo archivo Python.[

Qué es un DAG
------------------------------------------------------------------------

Se escriben en Python, pero pueden usar componentes escritos en otros
lenguajes. Compuestos de tareas **tasks*). Las dependencias entre tareas
se define explicita o implicitamente.


.. code:: python

    from airflow import DAG
    from datetime import datetime as DateTime

    arguments = {
        'owner': 'joe',
        'email': 'jdoedatacamp.com',
        'start_date': datetime(2026, 1, 20),
        }

    with DAG('etl_workflow', default_args=arguments) as etl_workflow:


La utilidad de línea de comando ``airflow``
------------------------------------------------------------------------

Se usa para

- Arrancar procesos airflow

- Ejecutar manualmente tareas o DAGs

- Obtener información de los ologs de Airflow

Más información con:

.. code:: shell

    airflow -h

Fuentes:

- [Apache Airflow](https://airflow.apache.org/)

- Datacamp [Introduction to Apache Airflow](https://campus.datacamp.com/courses/introduction-to-apache-airflow-in-python/intro-to-airflow?ex=1)
