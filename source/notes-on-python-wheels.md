---
title: Notes on Python Wheels
---

## Python Wheels

### What is a .whl file

A Python `.whl` file is essentially a ZIP (`.zip`) archive with a
**specially crafted filename** that tells installers what Python
versions and platforms the wheel will support.

A wheel is a type of built distribution. In this case, built means that
the wheel comes in a **ready-to-install** format and allows you to skip
the build stage required with source distributions.

A wheel filename is broken down into parts separated by hyphens:

> `{dist}-{version}(-{build})?-{python}-{abi}-{platform}.whl`

Each section in {brackets} is a **taga**, or a component of the wheel
name that carries some meaning about what the wheel contains and where
the wheel will or will not work. Lets use as an example
`cryptography-2.9.2-cp35-abi3-macosx_10_9_x86_64.wh`.

- Tag `dist` is the package name, `cryptography` in this case.

- `version` is the package tag. A version is a PEP 440-compliant
  string such as `2.9.2`, `3.4`, or `3.9.0.a3`.

- The `Python` tag denotes the Python implementation and version that
  the wheel demands. The value `cp` stands for CPython, the reference
  implementation of Python, while `35` denotes Python 3.5. This wheel
  wouldn't be compatible with Jython, for instance.

- The `abi`, like `abi3` is the ABI tag. ABI stands for Application
  Binary Interface. You don't really need to worry about what it
  entails, but `abi3` is a separate version for the binary
  compatibility of the Python C API.

- The `platform` tag, something like `macosx_10_9_x86_64`, which
  happens to be quite a mouthful. In this case it can be broken down
  further into sub-parts:

  -   `macosx` is the macOS operating system.
  
  -   `10_9` is the macOS developer tools SDK version used to compile
      the Python that in turn built this wheel.
  
  -   `x86_64` is a reference to x86-64 instruction set architecture.

- The final component isn't technically a tag but rather the standard
  `.whl` file extension. Combined, the above components indicate the
  target machine that this cryptography wheel is designed for.

Le see another example: `chardet-3.0.4-py2.py3-none-any.whl`:

Yocan break this down into its tags:

- `chardet` is the package name.

- `3.0.4` is the package version of chardet.

- `py2.py3` is the Python tag, meaning the wheel supports Python 2
  and 3 with any Python implementation.

- `none` is the ABI tag, meaning the ABI isn't a factor.

- `any` is the platform. This wheel will work on virtually any
  platform.

### Benefits of wheels

Wheels **install faster** than source distributions for both pure-Python
packages and extension modules.

Wheels **are smaller** than source distributions. For example, the six
wheel is about one-third the size of the corresponding source
distribution. This differential becomes even more important when you
consider that a pip install for a single package may actually kick off
downloading a chain of dependencies.

Wheels **cut setup.py execution out of the equation**. Installing from a
source distribution runs whatever is contained in that project's
setup.py. As pointed out by PEP 427, this amounts to arbitrary code
execution. Wheels avoid this altogether.

There's **no need for a compiler** to install wheels that contain
compiled extension modules. The extension module comes included with the
wheel targeting a specific platform and Python version.

pip **automatically generates .pyc** files in the wheel that match the
right Python interpreter.

Wheels provide **consistency** by cutting many of the variables involved
in installing a package out of the equation.

You can use a project's Download files tab on PyPI to view the different
distributions that are available. For example, pandas distributes a wide
array of wheels.

!!! Caution: PyPI wheels don't work on Alpine Linux nor BusyBox.

    This is because Alpine uses [musl](https://wiki.musl-libc.org/) in place of
    the standard glibc. The musl libc library bills itself as "a new libc
    striving to be fast, simple, lightweight, free, and correct."
    Unfortunately, when it comes to wheels, glibc it is not.  :::

Fuentes:

- [What Are Python Wheels and Why Should You Care? – Real Python](https://realpython.com/python-wheels/)
