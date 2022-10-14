---
title: Notes on black
---

## Notes on black formatter

### Black configuration

In the file `pyproyect.toml`

Command-line options have defaults that you can see with `--help`. A `pyproject.toml` can
override those defaults. Finally, options provided by the user on the command line override
both.

Black will only ever use one pyproject.toml file during an entire run. It doesn’t look for
multiple files, and doesn’t compose configuration from different levels of the file
hierarchy.

Example pyproject.toml

```
[tool.black]
line-length = 94
target-version = ['py38']
```

Sources:

- [Black documentation](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html)

### Use black in GitHub (As a GitHub action)

You can use Black within a GitHub Actions workflow without setting your own Python environment. Great for enforcing that your code matches the Black code style. This action installs Black with the colorama extra so the --color flag should work fine.


Create a file named `.github/workflows/black.yml` inside your repository with:

```
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: psf/black@stable
```
