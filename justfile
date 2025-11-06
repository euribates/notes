# Servir los contenidos de la carpeta de notas via web

serve:
    mkdocs serve -a localhost:3456

SOURCEDIR := "source"
BUILDDIR := "build"

html:
    sphinx-build -M html {{SOURCEDIR}} {{BUILDDIR}}

# Cliente de base de datos
dbshell:
    sqlite3 notes.db

# Genera el fichero de tags
tags:
    cd {{justfile_directory()}} && ctags -R --exclude=*.js --exclude=.venv .

