---
title: Notas sobre oauth32
---

## what is OAuth? 

OAuth is a specification that allows users to delegate access to their data without sharing their
username and password with that service.

Lets assume our app wants to get data from your twitter account. Easy way is give the app
your login & password details. This is a bad idea because (among other things):

1) The user must trust you A LOT to give you this type of access

2) If the user changes his password, system is broken, you need to ask the user to give you
   the password again

3) User give your app full access; is all or nothing.

So like everything else on the web, everyone made their own way to redirect the user and return
access to the data. Microsoft had their own protocol. Yahoo had their own protocol, every company
had their own way of doing things, and it became an absolute nightmare to implement
third-party-delegated access because you had to learn the specific way that that platform does it.

## OAuth 1

So finally, OAuth 1 standard was created. This added very strong benefits for the developer
community. 

- A **smaller learning curve**. you only had to learn OAuth once in order to be able to log in and
  delegate access to several services.

- It's **more secure** because, as a standard, it's community-vetted.

- The best part is everyone started doing things the same way. **We could write libraries**

## oAuth 2

So how is OAuth 2 different from OAuth 1? There's a lot of little differences, but we're gonna stick
with the two major ones here. 

- OAuth 1 was designed with just traditional server-client web applications in mind. This is
  becoming a smaller and smaller portion of real-world web applications between single-page
  applications, IOT devices. There are just way too many different scenarios for OAuth 1 to be
  flexible enough to deal with. We'll talk about how OAuth 2 is a little more flexible in a little
  bit. We talk about client profiles.

- OAuth 1 required signed tokens and signatures in order for OAuth to complete. In OAuth 2, you,
  do not need signed tokens. You can just have barrier tokens. We'll talk about the difference
  of these things and why they are important.


