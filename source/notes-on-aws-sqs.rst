Amazon Web Services: SQS
========================

..tags:: deploy, os

Para usar los servicios de Amazon (*Amazon Web Services*, AWS) desde
Python podemos usar la librería :index:`boto`. Los servicios incluidos
en SQS nos permite enviar mensajes a colas para procesarlos en forma
asíncrona, ya sea un otro momento o en otra máquina.

Las operaciones básicas que veremos aquí son crear una cola, conseguir
acceso a una cola ya existente, enviar (_push_) mensajes a la cola y
después recuperarlos para procesarlos.

Como crear una cola en SQS
--------------------------

Para crear una cola el primer paso es asignarle un nombre. Además,
podemos definir ciertos atributos de la cola como el número de segundos
que debe esperar un mensaje en la cola antes de ser procesado. En los
siguientes ejemplos se usará una cola con el nombre ``test``.

Antes de crear la cola, tenemos que acceder al recurso ``sqs``:

.. code:: python

   
   sqs = boto3.resource('sqs')  # Get the service resource
   queue = sqs.create_queue(
        QueueName='test',
        Attributes={'DelaySeconds': '5'},
        )  # Create the queue

   # You can now access identifiers and attributes
   print(queue.url)
   print(queue.attributes.get('DelaySeconds'))

.. warning:: Posible excepción

   El uso de este código podría producir que se elevara una excepción,
   si ya tuvieses una cola creada previamente con el mismo nombre.


Fuentes:

- `SQS.ServiceResource.create_queue() <http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.ServiceResource.create_queue>`__)


Cómo usar una cola ya existente en SQS
--------------------------------------

Es posible buscar una cola si conocemos su nombre, con
``get_queue_by_name``. Si la cola no existe, se elevará una excepción:

.. code:: python

   sqs = boto3.resource('sqs')
   queue = sqs.get_queue_by_name(QueueName='test')
   print(queue.url)
   print(queue.attributes.get('DelaySeconds'))

También podemos listar todas las colas existentes:

.. code:: python

   for queue in sqs.queues.all():
       print(queue.url)

.. warning:: El nombre de la cola
   
   Para obtener el nombre de la cola, debemos usar su ``ARN``, al cual
   podemos acceder como uno de los atributos de la cola. Con
   ``queue.attributes['QueueArn'].split(':')[-1]`` lo obtendriamos.

Fuentes:

-  `SQS.ServiceResource.get_queue_by_name() <http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.ServiceResource.get_queue_by_name>`__
-  `SQS.ServiceResource.queues <http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.ServiceResource.queues>`__

Cómo enviar un mensaje usando SQS
---------------------------------

Al enviar un mensaje a una cola, se añade al final de la misma:

.. code:: python

   sqs = boto3.resource('sqs')
   queue = sqs.get_queue_by_name(QueueName='test')

   # Create a new message
   response = queue.send_message(MessageBody='world')

   # The response is NOT a resource, but gives you a message ID and MD5
   print(response.get('MessageId'))
   print(response.get('MD5OfMessageBody'))

También se pueden crear mensajes con atributos personalizados:

.. code:: python

   queue.send_message(MessageBody='boto3', MessageAttributes={
       'Author': {
           'StringValue': 'Daniel',
           'DataType': 'String'
       }
   })

Los mensajes pueden ser enviados también en lotes. El siguiente ejemplo
muestra como enviar dos mensajes realizando una sola petición:

.. code:: python

   response = queue.send_messages(Entries=[
       {
           'Id': '1',
           'MessageBody': 'world'
       },
       {
           'Id': '2',
           'MessageBody': 'boto3',
           'MessageAttributes': {
               'Author': {
                   'StringValue': 'Daniel',
                   'DataType': 'String'
               }
           }
       }
   ])
   # Print out any failures
   print(response.get('Failed'))

En este caso, la respuesta contendrá una lista de respuesta de mensajes
exitosos o fallidos, que permite, por ejemplo, volver a encolar los
que hubieran fallado.

Fuentes:

-  `SQS.Queue.send_message() <http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Queue.send_message>`__
-  `SQS.Queue.send_messages() <http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Queue.send_messages>`__

Procesando mensajes de SQS
--------------------------

Los mensajes se procesan por lotes:

.. code:: python

   sqs = boto3.resource('sqs')
   queue = sqs.get_queue_by_name(QueueName='test')

   # Process messages by printing out body and optional author name
   for message in queue.receive_messages(MessageAttributeNames=['Author']):
       # Get the custom author message attribute if it was set
       author_text = ''
       if message.message_attributes is not None:
           author_name = message.message_attributes.get('Author').get('StringValue')
           if author_name:
               author_text = ' ({0})'.format(author_name)

       # Print out the body and author (if set)
       print('Hello, {0}!{1}'.format(message.body, author_text))

       # Let the queue know that the message is processed
       message.delete()

Suponiendo los dos mensajes envidos en la sección anterior, el
resultado del ejemplo sería:

::

   Hello, world!
   Hello, boto3! (Daniel)

Fuentes:

-  `SQS.Queue.receive_messages() <http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Queue.receive_messages>`__
-  `SQS.Message.delete() <http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Message.delete>`__
