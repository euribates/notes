## Notes on migrating to Python 3

There are (at least) two approaches to migrate code from 2.x to 3.x. 

One is **forget the compatibility with python 2**, use a tool like `2to3` and
[modernize](https://python-modernize.readthedocs.io/en/latest/) to solve everything that can be
automatically solved, and then work with the rest of changes manually until all things works through
the python 3 interpreter. This can be a good option if you have a good battery of tests and good
coverage level.

The oher option is to **make the code working both in Python 2 and Python 3**. There are some
libraries that help with this, like [six](https://pypi.org/project/six/) and
[future](http://python-future.org/).

Both options has advantages and disadvantages.

Option 1 is simpler, because you don't have to worry about backward compatibility, and you can use
the new features of python 3. Biggest disadvantage is you need to make a hard break point: before
this date we run python 2 code, after this date we'll run python 3. Is the code base is not small,
this change probably will need more than a day, so you are going to maintain two code bases in
parallel for some time, until you can switch all to python 3.

Option 2 is more complex, and you can't use most of the new python 3 improvement (But several of
then are available via future imports, though). The main advantege is you have the option of 
going step after step, with just one common code base for both Python versions.

I thinks option 1 is appropiate only if your code base is small, and you are very confident your
tests batteries have a really good coverage. This is clearly not our case, so I suggest going
with the option 2.

### Roadmap of migrations

1) **Get rid off the async problem**

We have in our code a module called `async`. The problm is `async` is now a
reserved word in python 3, so we need to rename our module. This module is
used in a lot of files, so the biggest problem we face here (And we will
face in the future) is how to coordinate all the developers to get this patch
applied at the same time. My suggestion is to apply those changes on friday, in
the `develop` branch (After all tests pass, of course) and use it as a rule
for every developer to merge with `develop` as the first thing to do every monday.

See [CHOIC-6959 Rename asyc module](https://help.octopusgroup.com/browse/CHOIC-6959).


2) **Wrote more tests**

We must avoid to add new code without test, and it would be better if the new code
could be executed and tested both in python 2 and python 3.

3) **Solve simple issues**

- Replace `loging.warn` by `logging.warning`

- Replace `except Exception, e` by `except Exception as err`

- Uses of `StringIO` and other classes/functions afected by the rename of some
  modules in Python 3

4) Include in all files some futures to make python 2 internals to behave more line in Python 3,
specifically:

```python
    from __future__ import absolute_import
    from __future__ import division
    from __future__ import print_function
    from __future__ import unicode_literals
```

We can add every one of this lines in a separated teask, buy I think we can also add all the 4
lines, because the only one with a chance of giving us problems is the `unicode_literals`, in some
specific cases as network protocols or working with binary files.

5) **Issues with Third Party libraries**

For this we have to check each one. We have two options, update to the last branch
in case the library is active and has been migrated, of find a replacement in case of the library
not being actively documented.

There is a project where you can check if your dependencies are python-3 ready or not. It's called
[caniusepython3](https://pypi.org/project/caniusepython3/). Executed in this current day
(21/Oct/2019) we got this:

    Finding and checking dependencies ...

    You need 5 projects to transition to Python 3.
    Of those 5 projects, 5 have no direct dependencies blocking their transition:

    clonedigger
    gocardless-pro
    python-appengine
    smtpapi
    torndb

Anvar also detected we are using PyCrypto, that has been dead for years, and suggested
to switch to PyCryptoDone, as suggested here: https://github.com/dlitz/pycrypto/issues/238

One of the task we need to make here is also to split the requierementes in two sets, the 
ones we need for sure to run the project in production and the one listing the requiriments
for developing. We must priorize to update/find a replacement for the first ones.

6) **Our own subprojects and internal dependencies**

We have some internal code in other repositories, they are listed in the `requirements.txt` file:

- github.com/octopus-investments/octopus-amlkyc-api-client-python.git
- github.com/xhtml2pdf/xhtml2pdf.git
- github.com/octopus-investments/octopus-isatransfers-python-client.git

And the new apps:

- event-dispatcher
- event-logger
- event-observer
- moneyday-worker
- monitor

We need to migrate all this code to python 3 too.

7) **Changes Related to Googe App Engine**

The Python 3.7 runtime in the App Engine standard environment **does not use the App Engine SDK** to
provide access to service functionality, unlike the Python 2.7 runtime, which does. Instead when
using the Python 3.7 runtime, we should use the Google Cloud managed services and/or third party
services.

- The queue and async problems could be solved with RabbitMQ

- Memcache services can be replaced with Redis

- To send email, use a third-party provider such as SendGrid, Mailgun, or Mailjet


The [google-cloud-python libraries](https://github.com/GoogleCloudPlatform/google-cloud-python) are
supported on this runtime. You must use these libraries to access Google Cloud Platform services
such as Cloud Pub/Sub, Cloud Datastore, Cloud Spanner and others.

Source: <https://cloud.google.com/appengine/docs/standard/python3/python-differences?hl=es-419#env>

### Changes on app.yaml

The behavior of some fields in your app.yaml configuration file has been modified.

| Field      | Change type  | Description                        |
+------------+--------------+------------------------------------|
| entrypoint | Added | Adopted from the App Engine flexible environment. You may, optionally use this field to specify the command that will run when your app starts. |
| threadsafe | Deprecated | All applications are presumed to be threadsafe. |
| api_version | Deprecated | No longer used in the Python 3 runtime. |
| builtins | Deprecated ||	
| libraries | Deprecated | Arbitrary third party dependencies can be installed using a requirements.txt metadata file. |
| handlers | Modified |	 The script field is optional and the only accepted value is auto. Use a web framework (for example, Flask or Django) with in-app routing to execute a script when a request hits a specific route |
+------------+--------------+------------------------------------|

Images
For manipulating and processing images, Imgix is recommended. Otherwise, use Rethumb if you prefer having a free tier.

Logging
Request logs are no longer automatically correlated but will still appear in Stackdriver Logging. You can use the Stackdriver Logging client libraries to implement your desired logging behavior.

Mail

To send email, use a third-party mail provider such as SendGrid, Mailgun, or Mailjet. All of these services offer APIs to send emails from applications.
- Memcache
To build an application cache, create a Cloud Memorystore instance and connect it to your app using Serverless VPC Access.

- Modules

Use a combination of environment variables and the App Engine Admin API to obtain information and modify your application's running services:

 - Current service name	GAE_SERVICE environment variable
 - Current service version	GAE_VERSION environment variable
 - Current instance ID	GAE_INSTANCE environment variable
 - Default hostname	Admin API apps.get method
 - List of services	Admin API apps.services.list method
 - List of versions for a service	Admin API apps.services.versions.list method
 - Default version for a service, including any traffic splits	Admin API apps.services.get method
 - List of running instances for a version	Admin API apps.services.versions.instances.list method

### Task queue

Queue tasks for asynchronous code execution using the [Cloud Tasks REST
API](https://cloud.google.com/tasks/docs/), RPC API, or the Google Cloud Client library, and use a
Python 3.7 App Engine standard service as a Push target. For more information, see [Migrating from
Task Queues to Cloud Tasks](https://cloud.google.com/tasks/docs/migrating).

In many cases where you might use pull queues, such as queuing up tasks or messages that will be
pulled and processed by separate workers, Cloud Pub/Sub can be a good alternative as it offers
similar functionality and delivery guarantees.

### Users

For an alternative to the Users API, use any HTTP-based authentication mechanism such as:

 - OAuth 2.0 and OpenID Connect which provide federated identity from the provider of your choice.
   Google is an OpenID Connect identity provider. There are also several other providers available.

 - Firebase Authentication, which provides authentication using username/password and federated
   identity using Google, Facebook, Twitter, and more.

 - Google Identity Platform, which provides many options for authentication and authorization of
   Google user accounts.

 - Auth0, which provides authentication with various identity providers and single sign-on features.

### Local development

In general we recommend that you use a testing approach that is idiomatic to Python rather than being dependent on dev_appserver. For example, you might use venv to create an isolated local Python 3.7 environment. Any standard Python testing framework can be used to write your unit, integration, and system tests. You might also consider setting up development versions of your services or use the local emulators that are available for many Google Cloud products.

As an optional feature for those who do choose to use it, we are offering an alpha version of an updated dev_appserver which supports Python 3. Please see Using the Local Development Server for more information on this option.

### Project-related libraries not ported to Python 3

- **AMLKYC** 

  https://github.com/octopus-investments/octopus-amlkyc-api-client-python

- **Isa-transfers**

  https://github.com/octopus-investments/octopus-isatransfers-python-client


### Third-party Libraries not ported to Python 3

- **analytics** 

  Last update on 2013


### Rules

#### If it uses suds

Uninstall suds and install suds-py3

```shell
pip uninstall suds
pip install suds-py3
```

Source: [Stackoverflow: How use suds.client library in python 3.6.2?](https://stackoverflow.com/questions/46043345/)


#### If it uses StringIO

Change `import StringIO` or `from StringIO import StringIO` to:

    ```Python
    from six import StringIO
    ```

Now, if code imported the module `StringIO`, you have to change every occurerence
of `StringIO.StringIO` with `StringIO`. If code imported the class `StringIO`, then you
need no further changes.


#### If it uses httplib

This library changed his named, and also functionality split in varios submodules,
`http.client` and `http.server`. Six makes an alias called `http_client` that is
`httplib` in Python 2 and `http.client` in Python 3.

Change:

    ```
    from httplib import HTTPException, UNAUTHORIZED, FORBIDDEN, NOT_FOUND
    ```

To:

    ```Python
    from six.moves.http_client import HTTPException, UNAUTHORIZED, FORBIDDEN, NOT_FOUND
    ```

#### It if uses ConfigParser

Change from `import ConfigParser` to `from six.moves import configparser`. Change every occurrence
of `ConfigParser` bt `configparser` to be ready to migrate to pure python3


#### If it uses `urllib`, `urllib2` or `urlparse`

The `urllib`, `urllib2`, and `urlparse` modules have been combined in the `urllib` package in Python 3. The
`six.moves.urllib` package is a version-independent location for this functionality; its structure
mimics the structure of the Python 3 `urllib` package.

- Change `urllib.parse` to `urllib.parse.urlencode`
- Change `urllib2.Request` to `urllib.request.Request`
- Change `urllib2.urlopen` to `urllib.request.urlopen`
- Change `urllib2.HTTPError` to `urllib.error.HTTPError`
- Change `urlparse.urlparse` to `urllib.parse.urlparse`
- Change `urlparse.urlsplit` to `urllib.parse.urlsplit`
- Change `urlparse.parse_qs` to `urllib.parse.parse_qs`
- Change `urlparse.urlunsplit` to `urllib.parse.urlunsplit`


## Installation in Macs

### Installing pycrypto

pip can't find gmp.h when compiling pycrypto. The solution is to install gmp via homebrew and export
custom cflags.

    brew install gmp
    export "CFLAGS=-I/usr/local/include -L/usr/local/lib"
    pip install pycrypto
