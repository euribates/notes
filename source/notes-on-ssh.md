---
title: Notas sobre SSH
tags:
  - unix
---

## Sobreo SSH

**SSH** (_Secure SHell_) es un protocolo y programa cuya principal
función es el acceso remoto a un servidor por medio de un canal seguro
en el que toda la información está cifrada.


## Use Your SSH Agent in a Crontab

Getting access to SSH inside a Crontab is often a problem for many as
the environment in which your cron runs **is not the same as your normal
shell**. Simply running `ssh-add` will not allow you to use your SSH
Agent inside your crontab. Follow the below guide to setup your crontab
to use your ssh-agent:

1) Install Keychain.

2) Add the following to your `~/.zlogin` file which will be invoked on
each login. This will allow your crontab (and normal shell) to use your
ssh keys and bypass needing to punch in your password each time you need
SSH. This will also span across multiple sessions and shells.

```shell
# Use keychain to keep ssh-agent information available in a file
/usr/bin/keychain "$HOME/.ssh/id_rsa"
source "$HOME/.keychain/${HOSTNAME}-sh"
```

3) Finally, prepend the following to your cron job command to allow it
access to your new keychain:

```bash
source "$HOME/.keychain/${HOSTNAME}-sh"
```

Fuente: [Use Your SSH Agent in a Crontab](https://gist.github.com/Justintime50/297d0d36da40834b037a65998d2149ca)


## About ssh-agent and ssh-add in Unix

In Unix, **ssh-agent** is a background program that handles passwords
for SSH private keys. The ssh-add command prompts the user for a private
key password and adds it to the list maintained by ssh-agent. Once you
add a password to ssh-agent, you will not be prompted for it when using
SSH or scp to connect to hosts with your public key.

The public part of the key loaded into the agent must be put on the
target system in `~/.ssh/authorized_keys`; see Set up SSH public key
authentication to connect to a remote system.

To use `ssh-agent` and `ssh-add`, follow the steps below:

At the Unix prompt, enter:

```shell
eval `ssh-agent`
```

Make sure you use the backquote (`), located under the tilde (~), rather
than the single quote (').

Enter the command:

```shell
ssh-add
```

Enter your private key password.
When you log out, enter the command:

```shell
kill $SSH_AGENT_PID
```

To run this command automatically when you log out, place it in your
`.logout` file (if you are using csh or tcsh) or your `.bash_logout` file
(if you are using bash).

Fuente: [Indiana University - About ssh-agent and ssh-add in Unix](https://kb.iu.edu/d/aeww)

## Como verificar si un certificado X.509 sigue siendo válido

Un **[certificado X.509](https://en.wikipedia.org/wiki/X.509)** X.509 es
un estándar para infraestructuras de claves públicas.  Especifica, entre
otras cosas, formatos estándares para certificados de claves públicas y
un algoritmo de validación de la ruta de certificación.

#### Verificar la validez de un fichero de certificado usando openssl

Podemos usar la opcion `x509` de la utilidad `openssl`:

```shell
$ openssl x509 -in secureweb2025.crt -nocert -dates
notBefore=Feb 25 12:35:39 2025 GMT
notAfter=Feb 25 12:35:39 2028 GMT
```

Donde usamos el _flag_ `-in` para indicar el fichero de entrada, y
`-dates` para que nos muestre las fechas de inicio y fin de la validez.
El flag `-nocert` se usa para que no incluya en la salida el propio
certificado en formato `PEM`

También tenemos el flag `-checkend`, que nos permite saber si el
certificado seguirá siendo válido en algún momento del futuro. Indicamos
ese momento futuro con el número de segundos a partir de la fecha
actual. La respuesta nos dirá si el certificado es valido para ese
momento o no.  Esto puede ser util para verificaciones de tipo "¿Dentro
de tres meses, este certificado seguirá siendo válido?":

```
$ openssl x509 -in secureweb2025.crt -checkend 7862400
Certificate will not expire

$ openssl x509 -in secureweb2025.crt -checkend 252288000
Certificate will expire
```

El valor $7862400$ viende de 91 días: 

$$ 91 \times 24 \times 60 \times 60 =  7862400 $$ 

El significado del número $252288000$ se deja como ejercicio para el lector.


#### Verificar un fichero Usando

Para verificar las fechas de validez de un certificado x509 tienes 
que instalar la librería [cryptography](https://cryptography.io/en/latest/):

```shell
pip install cryptography
```

Y la forma de comprobar los datos del certificado podría ser:

```python
from cryptography import x509

with open('certificate.crt', 'rb') as f_in:
    pem_data = f_in.read()
cert = x509.load_pem_x509_certificate(pem_data)
print(f'Serial number: {cert.serial_number}')
print(f'No valid after: {cert.not_valid_after}')
print(f'Issuer: {cert.issuer}')
```

## Que son los ficheros PEM

Muchos estánadares de criptografía usan
[ASN.1](https://en.wikipedia.org/wiki/Abstract_Syntax_Notation_One) para
definir sus estructuras, y
[DER](https://en.wikipedia.org/wiki/X.690#DER_encoding) (_Distinguished
Encoding Rules_) para serializar dichas estructuras.  Como la salida de
DER es un conjunto de bytes, puede ser un problema a la hora de
transmitir el fichero por determinados sistemas electrónicos, que solo
soportan ASCII.

El formato PEM resuelve este problema codificando los datos binarios
usando base64. También se define un formato de cabecera compuesto de una
única línea, en la forma `-----BEGIN [label]-----`, y un formato de pie
equivalente, `-----END [label]-----`. El valor de `[label]` determina el
tipo de contenido almacenado. Valores habituales son `CERTIFICATE`,
`CERTIFICATE REQUEST`, `PRIVATE KEY` o `X509 CRL`:

Por Ejemplo:

```
    -----BEGIN PRIVATE KEY-----
    
    -----END PRIVATE KEY-----
```

Los ficheros `PEM`̀ se almacenan habitualmente con el sufijo `.pem`,
`.cer` o `crt` y, en los casos de claves públicas o privadas, el sufijo
`key`. La etiqueta de la cabecera es más fiable del tipo de contenido
que el sufijo, ya que se pueden almacenar diferentes tipos de contenido
usando `.crt`, por ejemplo.
