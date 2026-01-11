HTTPS
========================================================================

.. tags:: web

A eliminar, webfaction ya no existe.

Notes on HTTPS and webfaction
-----------------------------

Webfaction
----------

A website’s HTTPS setting is either on or off. Connections to the
website are over the specified protocol only.

If you want your site to be served over HTTPS exclusively, then create a
redirect from HTTP to HTTPS.

If you need your site to be available over both HTTP and HTTPS, then
create two website records, one HTTP and the other HTTPS, and ensure
that both sites are assigned to the same IP address.

An HTTPS website requires an SSL/TLS certificate. By default, HTTPS
websites will use WebFaction’s shared certificate. Alternately, you can
use our control panel to generate a free certificate using Let’s Encrypt
or even bring your own, issued by another SSL certificate issuer.

If you use WebFaction’s shared certificate, **most browsers will warn
that your domain doesn’t match the certificate** (though the connection
will still be encrypted). To set up your website to use HTTPS with
WebFaction’s certificate, see Use a Certificate with a Website.

If you want to automatically provision a a free SSL certificate, using
Let’s Encrypt as your Certificate Authority, you can select that option
when you add or edit an HTTPS enabled website, see Use a Certificate
with a Website. Our panel will renew such a certificate when it is near
its expiration date.
