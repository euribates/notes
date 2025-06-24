---
title: Notas sobre Stripe
---

## Cómo probar la API de Stripe?

Para realizar pruebas interactivas, usa el número de tarjeta `4242 4242 4242 4242`. 
Introduce el número de la tarjeta en el Dashboard o en cualquier forma de pago.

- Usa una fecha futura válida, como 12/34
- Usa cualquier CVC de tres dígitos (cuatro dígitos si usas una tarjeta American Express).
- Usa cualquier valor para los demás campos del formulario.



## ¿Qué es Stripe Checkout?

La API **Checkout** es la forma más rápida de empezar a usar Stripe. Checkout
crea un formulario seguro, alojado en los servidores de Stripe, que permite
empezar a recibir cobros rápidamente. Funciona en todos los dispositivos.
Algunas de las características más interesantes son:

1) Diseñado para reducir la fricción: Validación de la tarjeta en tiempo real
con mensajes de error integrados.

2) Preparado para móviles. Totalmente _responsive_ y funciona con _Apple Pay_ y
_Google Pay_.

3) Internacional, con soporte para mas de 25 idiomas y múltiples modos de
pago.

4) Configuración y adaptación estética, se pueden configurar los botones y los
colores de fondo.

5) Preparada para intentos de estafa, cumple las regulaciones [PCI](https://es.wikipedia.org/wiki/PCI_DSS), [SCA](https://stripe.com/en-gb-es/guides/strong-customer-authentication), incluye
códigos _CAPTCHA_ para minimizar los ataques.

6) Otras mejoras: Permite aplicar descuentos, acumular impuestos, enviar
facturas por correos, y más.

## Cómo aceptar un cobro con _Checkout_

### 1) Instalar la librería de Stripe para Python

```shell
pip install stripe
```

### 2) Crea una instancia de la clase `PaymentIntent`

Stripe usa un objeto de tipo `PaymentIntent` para representa la _intención_
de realizar un cobro de un cliente. Con este objeto podemos seguir el rastro
de toda la secuencia de pasos a realizar para poder completar el cobro.

Para crear una instancia de `PaymentIntent` en el servidor, tenemos que
pasar como mínimo dos datos: Una moneda (_Currency_) y una cantidad. Hay que
hacer notar que tanto si trabajamos con euros, libras esterlinas o dolares
americanos se trabajará con céntimos, peniques o centavos respectivamente, de
forma que la cantidad a pagar siempre es entera.

La decisión de cuanto cobrar debe realizarse **siempre en el lado del
servidor**, ya que es un entorno controlado y en el que podemos confiar, y
**nunca se debe realizar en el cliente**. De lo contrario, cabría la posibilidad
de que un cliente maliciosos fuera capaz de elegir el precio.

El siguiente código es un ejemplo de generación de la intención de pago en
Python:

```python
# server.py
#
# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys

import stripe

stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

intent = stripe.PaymentIntent.create(
    amount=1099,
    currency='usd',
    dscription='Item or service sold/rented',
    # Verify your integration in this guide by including this parameter
    metadata={
        'integration_check': 'accept_a_payment'
    },
)
```

En el objeto retornado (`intent` en el ejemplo) viene un valor que denominamos
**client secret**, que se usará en la parte cliente para poder completar el
pago **sin tener que pasarle el objeto intención completo**. La forma más fácil
para aplicaciones Django o Flask es usar el sistema de plantillas:

```html
# checkout.html

<input id="card-name" type="text">
<!-- placeholder for Elements -->
<div id="card-element"></div>
<button id="card-button" data-secret="{{ client_secret }}">
    Submit Payment
</button>
```

En el _backend_ podríamos tener este código:

```python
urls.py

    urlpatterns = [
        ...
        path("checkout", views.checkout),
        ...
    ]

views.py

def checkout(request):
    intent = # ... Fetch or create the PaymentIntent
    return render(request, 'checkout.html', {
        'client_secret': intent.client_secret,
    })
```

### 3) **Recopilar los datos de la tarjeta en el cliente**

Ya estamos preparados para aceptar los datos del pago del cliente.  Para eso
usaremos **Elements**, un conjunto de componente de interfaz de usuario
predefinidos para aceptar y validar datos como el número de la tarjeta, códigos
postales, fecha de expiración, etc...

El componente _Element_ se aloja en un _iframe_, y envía de forma segura la
información del pago usado una conexión `HTTPS`. La página que almacena este
_iframe_ **también tiene que servirse usando `HTTPS`**, de lo contrario la
integración no funcionará. En el modo de pruebas, no obstante, si que
funcionará aunque la página esté servido por `HTTP`, pero hay que habilitar
`HTTPS` un producción.


### 4) **Prepara el componente Stripe Elements en el cliente**.

La librería `Stripe.js` nos da acceso automáticamente a _Elements_. Debemos
incluir `Stripe.js` en nuestra página de cobro, preferentemente en
la cabecera. Además, `Stripe.js` debe cargarse siempre desde `js.stripe.com`
para cumplir con el estándar [PCI](https://es.wikipedia.org/wiki/PCI_DSS). No
se debe incluir nunca como parte de un _bundle_, ni cargarse desde una copia
almacenada en nuestro servidor.

```html
# checkout.html

<head>
    <title>Checkout</title>
    <script src="https://js.stripe.com/v3/"></script>
</head>
```

Podemos crear una instancia de _Elements_ con el siguiente código en
nuestra página de cobro:

```javascript
script.js

// Set your publishable key: remember to change this to your live publishable key in production
// See your keys here: https://dashboard.stripe.com/account/apikeys
var stripe = Stripe('pk_test_TYooMQauvdEDq54NiTphI7jx');
var elements = stripe.elements();
```

Ahora tenemos que añadir *Elements* a nuestra página de cobro, concretamente en
nuestro formulario de cobro. Para ello creamos un componente `DIV` vacío, con
un identificador único dentro de nuestro formulario, y le pasaremos su
identificador a la librería, como en el siguiente ejemplo::

```html
# checkout.html

<form id="payment-form">
    <div id="card-element">
        <!-- Elements will create input elements here -->
    </div>

    <!-- We'll put the error messages in this element -->
    <div id="card-errors" role="alert"></div>

    <button id="submit">Pay</button>
</form>
```

Cuando el formulario se haya cargado, creamos y montamos la instancia de
*Elements*:

```javascript
client.js
// Set up Stripe.js and Elements to use in checkout form

var elements = stripe.elements();
var style = {
    base: {
        color: "#32325d",
    }
};

var card = elements.create("card", { style: style });
card.mount("#card-element");
```

El elemento `card` simplifica el formulario y minimiza el número de campos
requeridos, insertando un componente único que recolecta toda la información
pertinente para el pago. Otra forma de hacerlo seria instanciar y montar
elementos individuales como `cardNumber`, `cardExpiry` y `cardCvc`, si
necesitáramos más control sobre el aspecto y composición de nuestro formulario.

!!! warning "Pedir siempre el código postal"
    
    Incluir el código postal facilita mucho el paso de verificación de la
    tarjeta y disminuye el riesgo de fraude.

    El componente `card` siempre pide el código postal. Si se ha optado por
    contruir el fomulairios usando los componentes básicos: `cardNumber`,
    `cardExpiry` y `cardCvc`, incluir un campo de entrada adicional para el
    código postal.

    Se pueden ver más ejemplos de formularios con Elemente aquí: [additional
    payment forms](https://stripe.com/payments/elements/examples). En
    [Stripe.js reference
    documentation](https://stripe.com/docs/js#elements_create) podemos
    consultar una relación completa de todos los componente soportados con
    Elements.


Los componentes _Elements_ **validan la entrada a medida que se
teclea**. Esto ayuda a los clientes a corregir errores. Podemos capturar
estos errores y mostrarlos en nuestra página, como en el siguiente ejemplo:

```javascript
card.on('change', ({error}) => {
    let displayError = document.getElementById('card-errors');
    if (error) {
        displayError.textContent = error.message;
    } else {
        displayError.textContent = '';
    }
});
```

La validación de los códigos postales depende de cada país. Hay unas tarjetas
de prueba para esto en [international test
cards](https://stripe.com/docs/testing#international-cards).


### 5) **Enviar la información de pago a Stripe**

Como se explicó antes, no enviamos el _front_ toda la información contenido en la
intención (El objeto de tipo `PaymentIntent` que creamos en el paso 2); solo
se envía el **código secreto** (No confundir con las claves secretas
de Stripe que tenemos como desarrolladores, este es un valor generado por
Stripe y es diferente para cada intención). Por razones de seguridad, es
el único dato que se pasa a la parte cliente.

Este código de cliente, aun así, debe manejarse con mucho cuidado, ya que
permite **completar el cobro**. Por lo tanto, no debemos **NUNCA**:

- Guardar este valor en un log.

- Incluirlo en una URL.

- Mostrarlo o hacerlo accesible a cualquier otro que no sea el cliente.

Para completar el pago cuando el usuario pulse el botón correspondiente,
llamamos al método `stripe.confirmCardPayment` con el código secreto del
cliente:

```javascript
/* client.js */

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                name: 'Jenny Rosen'
            }
        }
    }).then(function(result) {
        if (result.error) {
            // Show error to your customer (e.g., insufficient funds)
            console.log(result.error.message);
        } else {
            // The payment has been processed!
            if (result.paymentIntent.status === 'succeeded') {
                // Show a success message to your customer
                // There's a risk of the customer closing the window before callback
                // execution. Set up a webhook or plugin to listen for the
                // payment_intent.succeeded event that handles any business critical
                // post-payment actions.
            }
        }
    });
});
```

La referencia a `card` es el elemento DOM donde la librería de Stripe montó
el componente de _Elements_ (Esto se hizo en el paso 4).

!!! warning

    La llamada a `stripe.confirmCardPayment` puede demorarse varios
    segundos, por lo que es recomendable desabilitar el
    formulario completamente y mostrar algún tipo de indicador de actividad,
    como un icono animado. En caso de error, debemos entonces mostrarselo al
    cliente, reactivar el formulario y ocultar el indicador de actividad.

Si el cliente tuviera que autentificar la tarjeta, la librería `Stripe.js` se
encargaría de esto, mostrando un diálogo modal. Se puede ver un ejemplo de este
diálogo usando la tarjeta de prueba `4000 0025 0000 3155` con cualquier valor
de _CVC_, una fecha de expiración en el futuro, y un código postal.

Una vez que el pago se ha realizado con éxito, la propiedad `status` en la
intención cambiará a `succeeded`. Si el pago no se hubiera completado con
éxito, podemos inspeccionar la propiedad `error` para determinar la causa.

Estos valores se pueden consultar también desde el _Dashboard_.

### 5) **Cómo testear la integración y gestionar eventos después del pago**

Stripe envía un evento `payment_intent.succeeded` cuando el pago se completa.
Podemos usar el _Dashboard_, un _webhook_ propio o una solución de terceros para
recibir estos eventos y ejecutar acciones en consecuencia, como enviar un
correo electrónico de confirmación de pago, almacenar la venta en la base de
datos, comenzar un proceso de envío ...

Es preferible procesar estos eventos a esperar una llamada remota desde el
navegador: el ciente puede cerrar la ventana antes de que el _callback_ se
pueda realizar. Además, si nos preparamos para aceptar estos eventos asíncronos
se nos simplifica el aceptar más formas de pago en el futuro.

## Create subscriptions with Checkout

This guide explains how to integrate Stripe's hosted forms for managing
subscription payments:

- **Checkout**, for collecting payment and creating the subscription.

- **The customer portal**, for helping your customers manage their
  subscriptions

Here's what you'll do:

- Model a fixed-price subscription with Products and Prices.

- Configure the customer portal.

- Collect payment information and create the subscription with
  Checkout.

- Integrate the customer portal to allow customers to manage their
  billing settings.

!!! warning
    This guide shows how to accept only card payments


1) **Set up Stripe**. Install the Stripe client of your choice with the
usual pip invocation: `pip install stripe`.

Optionally install the **Stripe CLI**. The CLI provides webhook testing,
and you can run it to create your products and prices.

To install the Stripe CLI on Debian and Ubuntu-based distributions:

1.1) Add Bintray's GPG key to the apt sources keyring:

```shell
sudo apt-key adv --keyserver hkp://pool.sks-keyservers.net:80 --recv-keys 379CE192D401AB61
```

1.2) Add stripe-cli's apt repository to the apt sources list:

```shell
echo "deb https://dl.bintray.com/stripe/stripe-cli-deb stable main" | sudo tee -a /etc/apt/sources.list
```

1.3) Update the package list:

```shell
sudo apt-get update
```

1.4) Install the CLI:

```shell
sudo apt-get install stripe
```

To run the Stripe CLI, you must also pair it with your Stripe account.
Run `stripe login` and follow the prompts. For more information, see the
[Stripe CLI documentation page](https://stripe.com/docs/stripe-cli).

2) **Create the business model** using the Dashboard or Stripe CLI

A **product** represents the item your customer subscribes to. The
**price** represents how much and how often to charge for the product.

You create your products and their pricing options in the Dashboard or
with the Stripe CLI. A fixed-price service with two different options,
named Basic and Premium, needs a product and a price for each option.

In this sample, each product bills at **monthly intervals**. The price
for one product is **5 USD**, and the other is **15 USD**.

**Using the dashboard**:

Navigate to the *Create a product page*, and create two products. Add
one price for each product, each with a monthly billing interval:

-  Basic product

   - Price: 5.00 USD

-  Premium product
   
   - Price: 15.00 USD

After you create the prices, record the price IDs so they can be used in
subsequent steps. Each ID is displayed in the Pricing section of the
product.

The Copy to live mode button at the top right of the page lets you clone
your product from test mode to live mode when you're ready.

**Using the Stripe CLI**

Create the product objects:

```shell
# Premium product
stripe products create \
    --name="Billing Guide: Premium Service" \
    --description="Premium service with extra features"

# Basic product
stripe products create \
    --name="Billing Guide: Basic Service" \
    --description="Basic service with minimum features"
```

Record the **product ID** for each product. They look like this:

```json
{
    ...
    "id": "prod_H94k5odtwJXMtQ",
    ...
}
```

Use the product IDs to create a price for each product. Note that
`unit_amount` is **specified in cents**, so \$1500\$ = \$15\$ USD, for
example:

```shell
# Premium price
stripe prices create \
    -d product=prod_H94k5odtwJXMtQ \
    -d unit_amount=1500 \
    -d currency=usd \
    -d "recurring[interval]"=month

# Basic price
stripe prices create \
    -d product=prod_HGd6W1VUqqXGvr \
    -d unit_amount=500 \
    -d currency=usd \
    -d "recurring[interval]"=month
```

Record the **price ID** for each price so they can be used in subsequent
steps. They look like this:

```json
{
    ...
    "id": "price_HGd7M3DV3IMXkC",
    ...
}
```

3) **Configure the customer portal Dashboard**

You configure the portal in the Dashboard. At a minimum, make sure to
enable the functionality to allow customers to update their payment
methods. See Integrating the customer portal for information about other
settings you can configure.

4) **Create a Checkout Session Server**. On the backend of your
application, define an endpoint that creates the session for your
frontend to call. You need these values:

- The **price ID** of the subscription the customer is signing up for;
  this value is passed from your frontend.

- Your `success_url`, a page on your website that Checkout returns
  your customer to after they complete the payment.

- Your `cancel_url`, a page on your website that Checkout returns your
  customer to if they cancel the payment process

This is an example:

```python
# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = json.loads(request.data)

    try:
        # See https://stripe.com/docs/api/checkout/sessions/create
        # for additional parameters to pass.
        # {CHECKOUT_SESSION_ID} is a string literal; do not change it!
        # the actual Session ID is returned in the query parameter when your customer
        # is redirected to the success page.
        checkout_session = stripe.checkout.Session.create(
            success_url="https://example.com/success.html?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://example.com/canceled.html",
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": data['priceId'],
                    # For metered billing, do not pass quantity
                    "quantity": 1
                }
            ],
        )
        return jsonify({'sessionId': checkout_session['id']})
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400
```

The response object includes an id value you need in subsequent calls to
the Checkout Sessions endpoint. In this example, the success\_url is
customized by appending the Session ID. For more information about this
approach, see the documentation on [how to Customize your success
page](https://stripe.com/docs/payments/checkout/custom-success-page).

5) **Send customers to the Checkout form Client**. On the frontend of
your application, add a button that takes your customer to Checkout to
complete their payment. You also need to include `Stripe.js`:

```html
<head>
    <title>Checkout</title>
    <script src="https://js.stripe.com/v3/"></script>
</head>
<body>
    <button id="checkout">Subscribe</button>
</body>
```

Pass the price ID of your customer's selection to the backend endpoint
that creates the Checkout Session:

```javascript
script.js

var createCheckoutSession = function(priceId) {
    return fetch("/create-checkout-session", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            priceId: priceId
        })
    }).then(function(result) {
        return result.json();
    });
};
```

Add an event handler to the button to redirect to Checkout, calling
`redirectToCheckout` and passing the Checkout Session ID:

```javascript
document
    .getElementById("checkout")
    .addEventListener("click", function(evt) {
        createCheckoutSession(PriceId).then(function(data) {
            // Call Stripe.js method to redirect to the new Checkout page
            stripe.redirectToCheckout({
                sessionId: data.sessionId
            })
            .then(handleResult);
    });
});
```

After the subscription signup succeeds, the customer is returned to your
website at the `success_url` and a `checkout.session.completed` event is
sent. You can check for this event in the Dashboard or with a webhook
endpoint and the Stripe CLI.

6)  **Send customers to the Billing portal Client**. On your frontend,
    add a button to the page at the success\_url that provides a link to
    the customer portal:

```html
    <!-- success.html -->
    <head>
        <script src="./success.js" defer></script>
    </head>
    <body>
        <form id="manage-billing-form">
        <button>Manage Billing</button>
        </form>
    </body>
```

Pass the Checkout Session ID to a backend endpoint that retrieves the
Checkout Session and gets the customer ID from the response:

```js
/* success.js */

const urlParams = new URLSearchParams(window.location.search);
const sessionId = urlParams.get("session_id")
let customerId;

if (sessionId) {
    fetch("/checkout-session?sessionId=" + sessionId)
    .then(function(result){
        return result.json()
    })
    .then(function(session){
        // We store the customer ID here so that we can pass to the
        // server and redirect to customer portal. Note that, in practice
        // this ID should be stored in your database when you receive
        // the checkout.session.completed event. This demo does not have
        // a database, so this is the workaround. This is *not* secure.
        // You should use the Stripe Customer ID from the authenticated
        // user on the server.
        customerId = session.customer;

        var sessionJSON = JSON.stringify(session, null, 2);
        document.querySelector("pre").textContent = sessionJSON;
    })
    .catch(function(err){
        console.log('Error when fetching Checkout session', err);
    });
```

Add an event handler to the button to redirect to the portal, passing
the customer ID:

```js
/* success.js */
// In production, this should check CSRF, and not pass the session ID.
// The customer ID for the portal should be pulled from the
// authenticated user on the server.
const manageBillingForm = document.querySelector('#manage-billing-form');
manageBillingForm.addEventListener('submit', function(e) {
    e.preventDefault();
    fetch('/customer-portal', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sessionId: sessionId
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        window.location.href = data.url;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
```

7) **Create a portal Session Server**

On the backend, define the endpoint that retrieves the Checkout session
for your frontend to call. The response object includes the customer ID
that you pass to the portal session:

```python
# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

@app.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    return jsonify(checkout_session)
```

!!! warning
    You can also create the Stripe Customer object separately and pass the
    customer ID to the initial call to the Checkout Session endpoint.

Define the endpoint that creates the customer portal session for your frontend
to call, passing the customer ID from the frontend. You can also pass an
optional `return_url` value for the page on your site where your customer is
redirected after they finish managing their subscription:

```python
# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

@app.route('/customer-portal', methods=['POST'])
def customer_portal():
    data = json.loads(request.data)
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
    # Typically this is stored alongside the authenticated user in your database.
    checkout_session_id = data['sessionId']
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    return_url = os.getenv("DOMAIN")

    session = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=return_url)
    return jsonify({'url': session.url})
```

8) **Provision and monitor subscriptions Server**. When your customer
completes the Checkout form and you receive a checkout.session.completed
event, you should provision the subscription. Continue to provision each
month (for the case of this sample, which bills monthly) as you receive
invoice.paid events. If you receive an invoice.payment\_failed event,
notify your customer and send them to the customer portal to update
their payment method.

For testing purposes, you can monitor events in the Dashboard, but for
production you should set up a webhook endpoint and subscribe to
appropriate event types:

```python
# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

@app.route('/webhook', methods=['POST'])
def webhook_received():
    webhook_secret = {{'STRIPE_WEBHOOK_SECRET'}}
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'checkout.session.completed':
    # Payment is successful and the subscription is created.
    # You should provision the subscription.
        print(data)
    elif event_type == 'invoice.paid':
    # Continue to provision the subscription as payments continue to be made.
    # Store the status in your database and check when a user accesses your service.
    # This approach helps you avoid hitting rate limits.
        print(data)
    elif event_type == 'invoice.payment_failed':
    # The payment failed or the customer does not have a valid payment method.
    # The subscription becomes past_due. Notify your customer and send them to the
    # customer portal to update their payment information.
        print(data)
    else:
        print('Unhandled event type {}'.format(event.type))

    return jsonify({'status': 'success'})
```

The minimum event types to monitor

| Event name | Description |
|------------|-------------|
| `checkout.session.completed` | Sent when a customer clicks the Pay or Subscribe button in Checkout, informing you of a new purchase. |
| `invoice.paid`               | Sent each billing interval when a payment succeeds. |
| `invoice.payment_failed`     | Sent each billing interval if there is an issue with your customer's payment method. |

If you configure the customer portal to allow more actions, such as canceling a
subscription, see Integrating the customer portal for events to monitor.

For even more events to monitor, see Subscription webhooks.

Source: <https://stripe.com/docs/billing/subscriptions/checkout>

## Payment Intents API

-  New way to build dynamic payment flows.

-  Tracks the lifecycle of a customer checkout flow

-  Triggers additional authentication steps when required by regulatory
   mandates, custom Radar fraud rules, or redirect-based payment

Note: The Payment Intents API is SCA-ready

> In September 2019, new European regulation will begin requiring Strong
> Customer Authentication (SCA) for many online payments from European
> customers to European businesses. Impacted businesses will need to
> provide an extra layer of authentication at checkout to help keep
> their customers safe. The Payment Intents API fully supports
> SCA---including exemption logic---and ensure that you only ask
> customers to provide additional authentication when strictly
> necessary.

### The basis

A `PaymentIntent` object tracks the state of the payment through the
`status` attribute. When the payment is successful, the status of the
PaymentIntent changes to `succeeded` and you can confidently fulfill the
order.

The Payment Intents API centers around two actions:

- **Create**: Creating a PaymentIntent at the beginning of a checkout
  flow lets you track all the attempts to pay for an order.

- **Confirm**: Confirming a PaymentIntent will attempt to take the
  payment through the entire payment process.

You can confirm a `PaymentIntent` either on your server with `confirm`
API or on the client with `Stripe.js` and the mobile SDKs.

See how it works for a one-time payment like an e-commerce order or
donation:

### Step 1. Create a PaymentIntent

Create a PaymentIntent on your server, specifying the intended amount,
currency, and supported payment methods. best practice is to **create
the PaymentIntent as soon as the customer arrives on your checkout
flow** so Stripe can record all the attempted payments.

```python
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

intent = stripe.PaymentIntent.create(
    amount=1299,
    currency='gbp',
)
```

### Step 2. Collect Payment details

Use Stripe Elements to easily collect payment details that are safely sent to
Stripe's servers. Simply initialize a card element with Stripe.js. You can
customize the look and feel of Elements to fit your checkout page. [See some
examples](https://stripe.github.io/elements-examples/).

Each PaymentIntent typically correlates with a single "cart" or customer
session in your application. You can create the PaymentIntent during checkout
and store its ID on the user's cart in your application's data model,
retrieving it again as necessary.

### Step 3: Collect payment method details on the client

The Payment Intents API is fully integrated with Stripe.js, using
Elements to securely collect payment information on the client side and
submitting it to Stripe to create a charge. To get started with
Elements, include the following script on your pages. **This script must
always load directly from js.stripe.com in order to remain PCI
compliant**. You can't include it in a bundle or host a copy of it
yourself.

```html
<script src="https://js.stripe.com/v3/"></script>
```

To best leverage Stripe's advanced fraud functionality, **include this
script on every page on your site, not just the checkout page**.
Including the script on every page allows Stripe to detect anomalous
behavior that may be indicative of fraud as users browse your website.

To ensure that your integration is SCA-ready, be sure to always provide
the customer's **name, email, billing address, and shipping address**
(if available) to the stripe.handleCardPayment call.

3.  Call `handleCardPayment()`

With one call to Stripe from your client, you can handle authenticating,
authorizing, and capturing the payment. Stripe does the work. Behind the
scenes, Stripe checks fraud models and SCA requirements to dynamically
determine which payment actions to present.

4.  Let Stripe handle the UI

Stripe triggers 3D Secure when it is required to complete the payment,
walking the customer through the necessary steps before returning them
to your application. status = `required_action`

5.  Complete the payment flow

If authentication is successful and payment goes through, the PaymentIntent
creates a charge ([See
API](https://stripe.com/docs/api#payment_intent_object-charges%5Dthat)) is
stored in the charges field. Set up **webhooks** to be notified when the
PaymentIntent succeeds.

## How to use Webhooks

Use webhooks to be notified about events that happen in a Stripe
account.

Stripe can send webhook events that notify your application any time an
event happens on your account. This is especially useful for
events---like disputed charges and recurring billing events---that are
not triggered by a direct API request. This mechanism is also useful for
services that are not directly responsible for making an API request,
but still need to know the response from that request.

## When to use webhooks

Webhooks are necessary only for behind-the-scenes transactions. Most
Stripe requests (e.g., creating charges or refunds) generate results
that are reported synchronously to your code. These don't require
webhooks for verification.

However, the Payment Intents API with automatic confirmation and most
payment methods using Sources require using webhooks, so that your
integration can be notified about asynchronous changes to the status of
PaymentIntent and Source objects.

You might also use webhooks as the basis to:

- Update a customer's membership record in your database when a
  subscription payment succeeds

- Email a customer when a subscription payment fails

- Examine the Dashboard if you see that a dispute was filed

- Make adjustments to an invoice when it's created (but before it's
  been paid)

- Log an accounting entry when a transfer is paid

## Monitoring a PaymentIntent with webhooks

Stripe can send webhook events to your server to notify you when the
status of a PaymentIntent changes. This is useful for purposes like
determining when to fulfill the goods and services purchased by the
customer when using automatic confirmation.

Your integration should not attempt to handle order fulfillment on the
client side because it is possible for customers to leave the page after
payment is complete but before the fulfillment process initiates.
Instead, we strongly recommend using webhooks to monitor the
`payment_intent.succeeded` event and handle its completion asynchronously
instead of attempting to initiate fulfillment on the client side.

It is technically possible to use polling instead of webhooks to monitor
for changes caused by asynchronous operations---repeatedly retrieving a
PaymentIntent so that you can check its status---but this is markedly
less reliable and may pose challenges if used at scale. Stripe enforces
rate limiting on API requests, so exercise caution should you decide to
use polling.

To handle a webhook event, create a route on your server and configure a
corresponding webhook endpoint in the Dashboard. Stripe sends the
`payment_intent.succeeded` event when payment is successful and the
`payment_intent.payment_failed` event when payment isn't successful.

The webhook payload includes the PaymentIntent object. The following
example shows how to handle both events:

Python example:

```python
# You can find your endpoint's secret in your webhook settings
endpoint_secret = 'whsec_...'

@app.route("/webhook", methods=['POST'])
def webhook():
    payload = request.get_data()
    sig_header = request.headers.get('STRIPE_SIGNATURE')
    event = None

    try:
    event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )
    except ValueError as e:
    # invalid payload
    return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
    # invalid signature
    return "Invalid signature", 400

    event_dict = event.to_dict()
    if event_dict['type'] == "payment_intent.succeeded":
    intent = event_dict['data']['object']
    print "Succeeded: ", intent['id']
    # Fulfill the customer's purchase
    elif event_dict['type'] == "payment_intent.payment_failed":
    intent = event_dict['data']['object']
    error_message = intent['last_payment_error']['message'] if intent.get('last_payment_error') else None
    print "Failed: ", intent['id'], error_message
    # Notify the customer that payment failed

    return "OK", 200
```

When payment is unsuccessful, you can find more details by inspecting the
PaymentIntent's `last_payment_error property`. You can notify the customer that
their payment didn't complete and encourage them to try again with a different
payment method. Reuse the same PaymentIntent to continue tracking the
customer's purchase.

## Handling specific webhook events

The following list describes how to handle webhook events:

| EVENT | WHAT HAPPENED | EXPECTED INTEGRATION |
|-------|---------------|----------------------|
| `succeeded` | Customer's payment succeeded | Fulfill the goods or services purchased by the customer |
| `amount_capturable_updated` | Customer's payment is authorized and ready for capture | Capture the funds that are available for payment |
| `payment_failed` | Customer's payment was declined by card network or otherwise expire | Reach out to your customer via email or push notification and prompt them to provide another payment method |

## How to identify charges on a PaymentIntent

When a PaymentIntent attempts to collect payment from a customer, it creates a
charge object. You can inspect a PaymentIntent's [charges
property](https://stripe.com/docs/api/payment_intents/object#payment_intent_object-charges)
to obtain its complete list of attempted charges:

Python example:

```python
# Set your secret key: remember to change this to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

intent = stripe.PaymentIntent.retrieve('pi_Aabcxyz01aDfoo')
charges = intent['charges']['data']
```

The charges are listed in reverse chronological order, so the most recent
charge is first in the array. Note that the array includes any unsuccessful
charges created during the payment process in addition to the final successful
charge.

## Handling next actions

Some payment methods require additional steps, such as authentication, in order
to complete the payment process. The Stripe.js handleCardPayment function
handles these automatically, but some advanced integrations may wish to handle
these manually.

The PaymentIntent's `next_action` property exposes the next step that your
integration must handle in order to complete the payment. The type of possible
next actions can differ between various payment methods.

The following is a list of next action types and the payment methods that may
require them:

| TYPE | PAYMENT METHODS | WHAT IT MEANS / HOW TO HANDLE |
|------|-----------------|-------------------------------|
| `redirect_to_url` | Cards with 3DS | The customer needs to be sent to the provided URL to authenticate the payment. `top.location = intent.redirect_to_url.url ` |

You can refer to the documentation for individual payment methods for more
details about how to handle their required next actions.

## Manually handling 3D Secure authentication with redirect

A common action of interest is authenticating the customer's payment with 3D
Secure, as required by upcoming Strong Customer Authentication rules. There are
several possible ways to handle this in an integration.  The recommended way is
to use the handleCardPayment or handleCardAction functions in Stripe.js, which
assumes responsibility for ushering customers through that process and any
other actions that may be required.

To handle 3D Secure authentication manually, you can redirect the customer.
This approach is used when you manually confirm the PaymentIntent and provide a
`return_url` destination to indicate where the customer should be sent once
authentication is complete. Manual PaymentIntent confirmation can be performed
on the server or on the client with Stripe.js.

After confirmation, if the PaymentIntent has a status of `requires_action`,
inspect the PaymentIntent's next\_action, determine if it is `redirect_to_url`,
and redirect the customer to complete authentication. When applicable, the
PaymentIntent's `next_action` is populated with an object that has the
following shape:

```json
next_action: {
    type: 'redirect_to_url',
    redirect_to_url: {
        url: 'https://hooks.stripe.com/...',
        return_url: 'https://mysite.com'
    }
}
```

Use the following code in the browser to redirect the customer to the
address provided by the next\_action property:

```javascript
var action = intent.next_action;
if (action && action.type === 'redirect_to_url') {
    window.location = action.redirect_to_url.url;
}
```

When the customer finishes the authentication process, they are sent back to
the destination that you specified with the `return_url` property when you
created the PaymentIntent. The redirect also adds `payment_intent` and
`payment_intent_client_secret` URL query parameters that your application can
use to identify the PaymentIntent associated with the customer's purchase.

## How to test the integration

You can use the test cards in test mode to validate your integration
when 3D Secure scenarios: required, required and the payment is
declined, and not required. Use these card numbers with any expiration
date in the future and any three digit CVC code.

| CARD NUMBER | 3D SECURE USAGE | DESCRIPTION |
|-------------|-----------------|-------------|
| `4000000000003220` | Required | This test card requires 3D Secure 2 on all transactions and will trigger 3D Secure 2 in test mode |
| `4000008400001629` | Required | This test card requires 3D Secure 2 but payments will be declined with a card\_declined failure code after authentication |
| `4000000000003055` | Supported | This test card supports but does not require 3D Secure 2 and will not require additional authentication steps in test mode |

## Work with customers

Customer objects allow you to perform recurring charges, and to track multiple
charges, that are associated with the same customer. The API allows you to
create, delete, and update your customers. You can retrieve individual
customers as well as a list of all your customers.

## Setting the Subscription Billing Cycle Date

A subscription's billing date is determined by two factors:

- The **billing cycle anchor**: This defaults to when the subscription
  was created---or, if a trial period is used, to the trial end. It
  can also be explicitly set at the subscription's creation.

- The **billing interval** of its plan or plans.

For example, a customer subscribed to a **monthly plan** (This is the billing
interval) set to cycle on **the 2nd of the month** (This is the anchor) will
always be billed on the 2nd. A different customer, subscribed to that same plan
starting on the 15th, will always be billed on the 15th (Same plant, different
anchor).

Note: If a month does not have the anchor day, the subscription will be
billed on the last day of the month For example, a subscription starting
on January 31 bills on February 28 (or February 29 in a leap year), then
March 31, April 30, and so on.

## Specifying the billing cycle anchor when creating new subscriptions

When creating new subscriptions, you can set the billing cycle anchor to
whatever value you want. The anchor is a
[POSIX](https://en.wikipedia.org/wiki/Unix_time) timestamp, that is, the
number of seconds that have elapsed since 00:00:00 Thursday, 1 January
1970, UTC. In the next example, `1562228482` stand for 4 July 2019:

```Python
stripe.api_key = 'sk_test_2raYjNBqlE50fzN1O4vObiN8'

subscription = stripe.Subscription.create(
    customer='cus_4fdAW5ftNQow1a',
    items=[{'plan': 'plan_CBb6IXqvTLXp3f'}],
    billing_cycle_anchor=1562228482,
)
```

There are two ways to change when an existing subscription is billed:

- Reset the anchor to the current time using `billing_cycle_anchor='now'`. Be
  aware that this results in the customer being invoiced immediately. This can
  be done through the API.

- Introducing a [trial](https://stripe.com/docs/billing/subscriptions/trials)
  results in setting the anchor to the end of the trial. Trials are typically
  used at the start of a subscription. Applying them during a subscription is
  allowed. You can change a subscription's billing cycle using a trial via the
  API or the Dashboard.

We probably want to use the second one, if the costumer wants to change just
the date. For example, if she wants to get billed at 1th of the month, instead
at the 23th, and we are in May 15, we can introduce a trial period until June
1st. If we do this, we achieve two things:

- The customer will not be billed on May 23.

- The customer will be billed next on June 1, then on July 1, and so on.

Like in this example:

    stripe.Subscription.modify('sub_49ty4767H20z6a',
        trial_end=1561976345,
        prorate=False,
        )

::: {.note}
::: {.admonition-title}
Note
:::

⚠ Beware!

-   Always check the trial\_end is set in the future
-   Always set `prorate` to `False`, to prevent Stripe of calculating
    and charging the prorated amount
:::

## How to add classes and styles to card component

All Elements accept a common set of options, and then some
Element-specific options.

- `classes` (dict) Set custom class names on the container DOM element
  when the Stripe Element is in a particular state.
- `base` (String) The base class applied to the container. Defaults to
  `StripeElement`.
- `complete` (string) The class name to apply when the Element is
  complete. Defaults to StripeElement--complete.
- `empty` (string) The class name to apply when the Element is empty.
  Defaults to StripeElement--empty.
- `focus` (string) The class name to apply when the Element is
  focused. Defaults to StripeElement--focus.
- `invalid` (string) The class name to apply when the Element is
  invalid. Defaults to StripeElement--invalid.
- webkitAutofill (string) The class name to apply when the Element has
  its value autofilled by the browser (only on Chrome and Safari).
  Defaults to StripeElement--webkit-autofill.
- style:

  Customize appearance using CSS properties. Style is specified as an
  object for any of the variants below.

  - base, base style---all other variants inherit from this style
  - complete, applied when the Element has valid input
  - empty, applied when the Element has no customer input
  - invalid, applied when the Element has invalid input

For each of the above, the properties below can be customized.

- `color`
- `fontFamily`
- `fontSize`
- `fontSmoothing`
- `fontStyle`
- `fontVariant`
- `fontWeight`
- `iconColor`
- `lineHeight`, to avoid cursors being rendered inconsistently
  across browsers, consider using a padding on the Element\'s
  container instead.
- `letterSpacing`
- `textAlign`, available for the `cardNumber`, `cardExpiry`, and
  `cardCvc` Elements.
- `padding`, available for the idealBank Element.
- `textDecoration`
- `textShadow`
- `textTransform`

The following pseudo-classes and pseudo-elements can also be styled with
the above properties, as a nested object inside the variant.

- `:hover`
- `:focus`
- `::placeholder`
- `::selection`
- `:-webkit-autofill`
- `:disabled`, available for all Elements except the
  paymentRequestButton Element.
- `::-ms-clear`, available for the `cardNumber`, `cardExpiry`, and
  `cardCvc` Elements. Inside the `::-ms-clear` selector, the display
  property can be customized.

The paymentRequestButton Element supports a single variant:
`paymentRequestButton`. The properties below are customizable for this
variant.

- `type`, one of `default`, `donate`, or `buy`. The default is
  `default`.

- `theme`: Puede ser `dark`, `light` o `light-outline`. Por defecto es `dark`.

- `height`

Example:

    var style = {
        base: {
            color: '#303238',
            fontSize: '16px',
            color: "#32325d",
            fontSmoothing: 'antialiased',
            '::placeholder': {
                color: '#ccc',
            },
        },
        invalid: {
            color: '#e5424d',
            ':focus': {
                color: '#303238',
            },
        },
    };
    var cardElement = elements.create('card', {style: style})


## How to make Off-session Payments with Payment Intents

how to save a customer's payment information and create a payment later
when the customer is not available to complete authentication steps such
as 3D Secure.

To collect off-session payments with the Payment Intents API, perform
the following steps:

1.  Collect payment information and attach it to a customer
2.  At a later time, create a `PaymentIntent` and attach a payment
    method
3.  Check the `PaymentIntent` status
4.  Notify customer to complete payment if needed

Let's see step by step

### Step 1: Collect payment information and attach it to a customer

Start by securely collecting the customer's payment information with
Stripe.js Elements or the mobile SDKs. Once you have payment
information, **create a Customer** and **attach the payment method** to
him/her:

    stripe.api_key = 'your-stripe-api-key-here'

    # Create a Customer:
    customer = stripe.Customer.create(
        email='paying.user@example.com',
        )

    # Attach payment method to the customer:
    stripe.PaymentMethod.attach('pm_123456789', customer=customer.id)

    # YOUR CODE: Save the customer ID and other info in a database for later.

### Step 2: At a later time, create a PaymentIntent with a payment method

When creating a `PaymentIntent`, specify both the ID of the Customer and
the ID of the previously saved Card, Source, or PaymentMethod. You
should also set the value of the PaymentIntent's confirm property to
true, which causes confirmation to occur immediately when the
PaymentIntent is created. Note that you can also programmatically
confirm a PaymentIntent that has already been created.

The following code example demonstrates how to create and confirm a
PaymentIntent with a customer and payment\_method:

    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    stripe.api_key = 'your-stripe-api-key-here'

    stripe.PaymentIntent.create(
        amount=1099,
        currency='eur',
        payment_method_types=['card'],
        customer='{{CUSTOMER_ID}}',
        payment_method='{{PAYMENT_METHOD_ID}}',
        off_session='one_off',
        confirm=True,
    )

::: {.note}
::: {.admonition-title}
Note
:::

**Note**: If this is a payment within a set of recurring payments (i.e.,
a subscription), set off\_session to `recurring`. This gives us more
information about the context of your off-session payment so that we can
help you optimize your payment success rate. If you require more
complicated subscription logic with multiple plans, usage ba:q sed
reporting, or complicated tax logic, the Subscriptions API may be better
suited to your needs.
:::

### Step 3: Check the PaymentIntent status

Inspect the `status` property of the PaymentIntent to confirm that the
payment completed successfully.

If the payment attempt failed, the request will fail with a 402 HTTP
status code.

### Step 4: Notify customer to complete payment if needed

When a payment fails (`requires_payment_method`), you should notify your
customer to return to your application to complete the payment. You can
check the `last_payment_error` on the PaymentIntent to inspect why the
payment failed off-session. If the payment failed due to an
authentication\_required decline code, you can give the customer the
option to try paying again on-session with the same payment method
(last\_payment\_error.payment\_method). We recommend that you **create a
web page or mobile app screen with a payment form that you can send your
customer to in these cases**.

On this page, make the PaymentIntent's client secret available and use
the Stripe.js or the mobile SDKs to display authentication.

While testing, you can use our 3D Secure required test card number
(`4000000000003063`) to force this flow. Using the 3D Secure not
required card (`4242424242424242`) will skip this part of the flow and
complete at Step 3 because it does not require authentication.

## Documentation and more information

- [Choice - SCA integration via
  Stripe](https://docs.google.com/document/d/1GApRA52doNrfadbJP9i2yQWXbLiWR_ATfONtB2jYUVs/edit)
- [SCA Labs - Cheat
  Sheet](https://docs.google.com/document/d/1xceLFPt3CTNISJ17-sFKcfCzoVnOW0ZXCAdj5tK1ak4/edit#)
- [SCA Labs Off-session payments
  integration](https://docs.google.com/document/d/1xxCWVN7teSoerEDCr0e2g0FCiHEKV3VSmNpEF52bkZU/edit#)
- [Stripe decline
    codes](https://docs.google.com/spreadsheets/d/161iFI64ydexQq-oduJznTnA_AdTN9CqxSHW72IS1eu8/edit)
