# Servir los contenidos de la carpeta de notas via web
serve:
    mkdocs serve -a localhost:3456

SOURCEDIR := "docs"
BUILDDIR := "build"

html:
    sphinx-build -M html {{SOURCEDIR}} {{BUILDDIR}}

hola:
    #!/usr/bin/env python3
    print('Hello from python!')
