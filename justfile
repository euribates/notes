# Servir los contenidos de la carpeta de notas via web

serve:
    mkdocs serve -a localhost:3456

SOURCEDIR := "source"
BUILDDIR := "build"

html:
    sphinx-build -M html {{SOURCEDIR}} {{BUILDDIR}}

hola:
    python -c "print('Hello from python!')"


