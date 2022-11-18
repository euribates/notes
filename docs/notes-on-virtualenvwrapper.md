---
title: Notas sobre VirtuelEnvWrapper
tags:
  - python
---

## Sobre virtualenv wrapper

## How to set the project dir of a virtual env

Use the command `setvirtualenvproject`. It needs two parameters, first
one the location of the virtualenv, usually something like
`~/.virtualenvs/<name>` and second the path to use a default for the
project. You can use `$(pwd)` if it's the current path:

```bash
cd /workarea/octopus/octopus-cash
setvirtualenvproject ~/.virtualenvs/cash/ $(pwd)
```
