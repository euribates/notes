---
title: Notas sobre JWT
---

## Notes on JWT

## TOKEN BASED AUTHENTICATION

A **token** is a piece of data that has no meaning or use on its own, but
combined with the correct tokenization system, becomes a vital player in
securing your application. Token based authentication works by ensuring that
each request to a server is accompanied by a signed token which the server
verifies for authenticity and only then responds to the request.

JSON Web Token (JWT) is an open standard (RFC 7519) that defines a compact and
self-contained method for securely transmitting information between parties
encoded as a JSON object. JWT has gained mass popularity due to its compact size
which allows tokens to be easily transmitted via query strings, header
attributes and within the body of a POST request.
