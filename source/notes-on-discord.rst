Discord
========================================================================

Qué es :index:`discord`
------------------------------------------------------------------------

**Discord** es un servicio de mensajería instantánea y *chat* de voz
VolP. En esta plataforma, los usuarios tienen la capacidad de
comunicarse por llamadas de voz, videollamadas, mensajes de texto, o con
archivos y contenido multimedia en conversaciones privadas o como parte
de comunidades llamadas "servidores".

La librería `discord.py`_ es una librería de Python para interactuar con
la API de Discord. Es asíncrona, y requiere Python 3.8 o superior


Instalación de discord.py
------------------------------------------------------------------------

.. code:: shell

   pip install discord.py

Eventos
------------------------------------------------------------------------

Discord trabaja sobre el concepto de **eventos**. Un evento es algo a lo
que te suscribes y luego actuas cunado ocurre. POr ejemplo, el envío de
un mensaje en un canal es un evento al que podemos respoder.

Un ejemplo de como funcionan los eventos:

.. code:: python

    import discord
 
    class MyClient(discord.Client):
        async def on_ready(self):
            print(f'Logged on as {self.user}!')
 
        async def on_message(self, message):
            print(f'Message from {message.author}: {message.content}')
 
    intents = discord.Intents.default()
    intents.message_content = True
 
    client = MyClient(intents=intents)
    client.run('my token goes here')


Un *bot* mínimo en Discord
------------------------------------------------------------------------

Esto podría ser el hola,mundo de los *bots* de Discord:

.. code:: python

    # This example requires the 'message_content' intent.
 
    import discord
 
    intents = discord.Intents.default()
    intents.message_content = True
 
    client = discord.Client(intents=intents)
 
    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
 
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
 
        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')
 
    client.run('your token here')

Puntos interesantes en este código:

- La instancia ``client`` de ``Client`` es nuestra conexión con Discord

- El decorador ``client.event`` nos permite registrar funciones
  *callbacK* que serám invocadas cuando se produzca un evento. El nombre
  de la función es lo que determina a que evento debe resonder:
  ``on_ready`` se llamara cuando el cliente se haya logeado a Discord, y
  ``on_message`` cada vez que se envíen un mensaje al *bot*.

- Como ``on_message`` se llamaa **para todos los mensajes**, tenemos que
  asegurarnos de ignorar los mensajes que el propio *bot* envía. Eso lo
  hacemos en la comparación ``message.author == client.user``.

- En este caso, pasada la comprobación anterior, se comprueba si el
  texto del mensaje empieza por ``$hello``. Esta es una forma básica de
  responder a los mensajes, pero hay toda una parte de la API dedicada a
  `implementar comandos en Discord`_

- Por último, para que todo funcione necesitamos en token que permite
  identificar al *bot*. Obtenemos ese token cuando damos de alta al
  *bot*.


.. _discord.py: https://discordpy.readthedocs.io/en/stable/index.html
.. _implementar comandos en Discord: https://discordpy.readthedocs.io/en/stable/ext/commands/index.html
