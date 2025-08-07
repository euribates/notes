---
title: Notas sobre Google Flex Environment
tags:
  - google
  - cloud
---

## Sobre Google Flex Environemnt


## Similarities and key differences

Both environments provide you with App Engine’s deployment, serving, and scaling infrastructure. The
key differences are :

- The way the environment executes your application

- How your application accesses external services

- How you run your application locally

- How your application scales.

## Application execution

In the standard environment, your application runs on a lightweight instance inside of a sandbox.
This sandbox restricts what your application can do. For example, your application can **not write
to disk** or **use non-whitelisted binary libraries**. The standard environment also **limits the
amount of CPU and memory** options available to your application. Because of these restrictions,
most App Engine standard applications tend to be stateless web applications that respond to HTTP
requests quickly.

In contrast, the flexible environment **runs your application in Docker containers** on Google Compute
Engine virtual machines (VMs), which have fewer restrictions. For example, you can use any
programming language of your choice, write to disk, use any library you'd like, and even run
multiple processes. The flexible environment also allows you to choose any Compute Engine machine
type for your instances so that your application has access to more memory and CPU.

## Accessing external services

In the standard environment, your application typically accesses services such as Cloud Datastore
via the built-in google.appengine APIs. However, in the flexible environment, these APIs are no
longer available. Instead, use the Google Cloud client libraries. These client libraries work
everywhere, which means that your application is more portable. If needed, applications that run in
the flexible environment can usually run on Google Kubernetes Engine or Compute Engine without heavy
modification.

## Local development

In the standard environment, you typically run your application locally using the App Engine SDK.
The SDK handles running your application and emulates the App Engine services. In the flexible
environment, the SDK is no longer used to run your application. Instead, applications written for
the flexible environment should be written like standard web applications that can run anywhere.

As mentioned, the flexible environment just runs your application in a Docker container. This means
that to test the application locally, you just run the application directly. For example, to run a
Python application using Django, you would just run python manage.py runserver.

Another key difference is that flexible environment applications running locally use actual Cloud
Platform services, such as Cloud Datastore. Use a separate project for testing locally and when
available, use emulators.

## Scaling characteristics

While both environments use App Engine’s automatic scaling infrastructure, the way in which they
scale is different. The standard environment can scale from zero instances up to thousands very
quickly. In contrast, the flexible environment must have at least one instance of your application
running and can take longer to scale up in response to traffic.

Standard environment uses a custom-designed autoscaling algorithm. Flexible environment uses the
Compute Engine Autoscaler. Note that flexible environment does not support all of the autoscaling
options that are available to Compute Engine. Developers should test their application behavior
under a range of conditions. For example, you should verify how autoscaling responds when a
CPU-bound application becomes I/O-bound during periods when calls to remote services have elevated
latency.

## Health checks

Standard environment does not use health checks to determine whether or not to send traffic to an
instance. Flexible environment permits application developers to write their own health check
handlers

## Maximum request timeout

The standard environment imposes a 60 second request deadline for versions that use automatic
scaling. Flexible environment does not impose a deadline. Application programmers should
ensure calls to external services specify a timeout in order to avoid
requests hanging indefinitely.


