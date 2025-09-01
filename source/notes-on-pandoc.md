---
title: Notas sobre Pandoc
tags:
    - python
    - documentation
    - pandoc
---

# Notas sobre Pandoc

## Qué es PanDoc

**[Pandoc](https://pandoc.org/)** es un conversor de documentos libre y
de código abierto, mayormente usado como una herramienta de escritura
(especialmente por académicos), y es una base para la publicación de
flujos de trabajo. Fue creado originalmente por John MacFarlane, un
profesor de Filosofía en la Universidad de California, Berkeley.

## Cómo convertir de MarkDown a Reestructured Text

Para pasar de MarkDown a Rest, esta es la forma:

```shell
pandoc --from=markdown --to=rst --output=index.rst index.md
```

Para hacer la operación inversa, convertir de Reestructured Text a
MarkDown:

```shell
pandoc --from=rst --to=markdown --output=README.md README.rst
```

La sintaxis general es:

```shell
pandoc --from={type} --to={type} --output={filename} {input-filename}
```

Se puede usar una sintaxis más sencilla si se han usado las extensiones de los
nombres de archivo adecuadasÑ

```shell
pandoc -s README.md -o README.rst
```

Donde `-s` simboliza _source_ y `-o`, _output_.

Fuente: [pandoc - Convert markdown to reStructuredtest? - Stack Overflow](https://stackoverflow.com/questions/30952995/convert-markdown-to-restructuredtest)
