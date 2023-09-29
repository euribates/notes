---
title: Notes on AWS SQS
---

## Notes on Amazon Web Services: SQS

This tutorial will show you how to use Boto3 with an AWS service. In
this sample tutorial, you will learn how to use Boto3 with Amazon Simple
Queue Service (SQS) SQS

SQS allows you to queue and then process messages. This tutorial covers
how to create a new queue, get and use an existing queue, push new
messages onto the queue, and process messages from the queue by using
Resources and Collections.


## Como crear una cola en SQS

Queues are created with a name. You may also optionally set queue
attributes, such as the number of seconds to wait before an item may be
processed. The examples below will use the queue name test. Before
creating a queue, you must first get the SQS service resource:

```python
# Get the service resource
sqs = boto3.resource('sqs')

# Create the queue. This returns an SQS.Queue instance
queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})

# You can now access identifiers and attributes
print(queue.url)
print(queue.attributes.get('DelaySeconds'))
```

Please note the code above may throw an exception if you already have a queue named
test.

- Fuentes: [SQS.ServiceResource.create\_queue()](http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.ServiceResource.create_queue))


## Cómo usar una cola ya existente en SQS

Es posible buscar una cola si conocemos su nombre, con `get_queue_by_name`. Si
la cola no existe, se elevará una excepción:

```python
# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName='test')

# You can now access identifiers and attributes
print(queue.url)
print(queue.attributes.get('DelaySeconds'))
```

También podemos listar todas las colas existentes:

```python
for queue in sqs.queues.all():
    print(queue.url)
```

!!!Note "The queue name"
    To get the name from a queue, you must use its ARN, which is available
    in the queue's attributes attribute. Using
    `queue.attributes['QueueArn'].split(':')[-1]` will return its name.

Fuentes:

- [SQS.ServiceResource.get\_queue\_by\_name()](http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.ServiceResource.get_queue_by_name)
- [SQS.ServiceResource.queues](http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.ServiceResource.queues)


## Cómo enviar un mensaje usando SQS

Al enviar un mensaje a una cola, se añade al final de la misma:

```python
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='test')

# Create a new message
response = queue.send_message(MessageBody='world')

# The response is NOT a resource, but gives you a message ID and MD5
print(response.get('MessageId'))
print(response.get('MD5OfMessageBody'))
```

You can also create messages with custom attributes:

```python
queue.send_message(MessageBody='boto3', MessageAttributes={
    'Author': {
        'StringValue': 'Daniel',
        'DataType': 'String'
    }
})
```

Messages can also be sent in batches. For example, sending the two
messages described above in a single request would look like the
following:

```python
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
```

In this case, the response contains lists of Successful and Failed
messages, so you can retry failures if needed.

References:

- [SQS.Queue.send\_message()](http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Queue.send_message)
- [SQS.Queue.send\_messages()](http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Queue.send_messages)


## Procesando mensajes de SQS

Los mensajes se procesan por lotes:

```python
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
```

Given only the messages that were sent in a batch with
`SQS.Queue.send_messages()` in the previous section, the above code will
print out:

```
Hello, world!
Hello, boto3! (Daniel)
```

Fuentes:

- [SQS.Queue.receive\_messages()](http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Queue.receive_messages)
- [SQS.Message.delete()](http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Message.delete)
