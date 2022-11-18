---
title: Notas sobre el formato ePub
---

## Sobre Epub

## Cómo crear un ePub desde cero

Un epub es simplemente un fichero zip, con otra extensión, `epub`, que
contienen un pequeño website. La matoria de los ficheros, como los
`.xhtml` y `.css` son equivalentes a los que encontramos en un site web.

### El fichero container.xml

El archivo **`container.xml`** tiene dos responsabilidades: En primer lugar,
informa al lector de _ebooks_ donde encontrar el archivo `OPF`, que es el corazón
del _ebook_. En segundo lugar, informa sobre la ubicación del resto de
ficheros, el orden en que debe mostrarlos, y que papel juega cada uno de ellos
(por ejemplo, el fichero de tipo imagen que contiene la portada del libro, el
índice o tabla de contenidos, etc...)

Este es un ejemplo de un archivo `container.xml`.

```xml
<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles>
 <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
</rootfiles>
</container>
```


### El fichero `toc.ncx`

El fichero **`toc.ncx`** es un fichero especializado en la navegación por el
libro; contiene la información que el _ereader_ muestra cuando se pulsa el botón
de _contenidos_ o _capítulos_.

El siguiente ejemplo contiene dos elementos en la tabla de contenidos o índice.
Hay que añadir más entradas con la etiqueta `navPoint` para añadir secciones, y
rellenar los siguientes valores:

- En los meta:

 - `dtb:depth`
 - `dbt:generator`
 - `dbt:totalPageCount`
 - `dbt:maxPageNumber`

- Como contenido en las etiquetas:

 - `docTitle` : El título del libro

- Cada `navPoint` tiene que contener la siguiente información:

  - Un atributo de identificacion llamado `id`

  - Un atribuo `playOrder` que especifia el orden de lectura

  - Una etiqueta `navLabel`, que contendrá otra etiqueta `text`
    con el título de la sección  o capítulo

  - Una etiqueta `content` que enlaza con el fichero xhml donde
    está el contenido del capítulo o sección.

```xml
<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="eng">
<head>
<meta content="0c159d12-f5fe-4323-8194-f5c652b89f5c" name="dtb:uid"/>
<meta content="2" name="dtb:depth"/>
<meta content="calibre (0.8.68)" name="dtb:generator"/>
<meta content="0" name="dtb:totalPageCount"/>
<meta content="0" name="dtb:maxPageNumber"/>
</head>
<docTitle>
<text>How to Build a Website</text>
</docTitle>
<navMap>
<navPoint id="a1" playOrder="0">
<navLabel>
<text>Hosting</text>
</navLabel>
<content src="build_website.html#step1"/>
</navPoint>
<navPoint id="a2" playOrder="1">
<navLabel>
<text>Do You Need a Domain Name?</text>
</navLabel>
<content src="build_website.html#step2"/>
</navPoint>
</navMap></ncx>
```

- Your cover image should be a JPG file no more than 64KB. The smaller you can
  make it the better, but keep it good looking. Small images can be very hard
  to read, and the cover is where you do your marketing of your book.

### MIME Type file

Create a MIME Type File. In your text editor, open a new document and type:

```
application/epub+zip
```

Save the file as `mimetype` without any extension. Place that file in the
folder with your XHTML files.


### Hojas de estilo

Add your style sheets. You should create two style sheets for your book one
for the pages called `pages.css`:

```
@page {
    margin-bottom: 5pt;
    margin-top: 5pt;
} 
```

And one for the book styles called `book.css`. You can give them other names,
you'll just need to remember what they are. Save these files in the same
directory with your XHTML and mimetype files.


### Página de título

Build your title page. You don't have to use the cover image as your title
page, but most people do. To add your title page, create an XHTML file called
`titlepage.xhtml`. Here is an example of a title page using SVG for the image.
Change the highlighted part to point to your cover image:

```xml
<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<title>Cover</title>
<style type="text/css" title="override_css">
@page {padding: 0pt; margin:0pt}
body { text-align: center; padding:0pt; margin: 0pt; }
</style>
</head>
<body>
<div>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="100%" height="100%" viewBox="0 0 425 616" preserveAspectRatio="none">
<image width="425" height="616" xlink:href="cover.jpeg"/>
</svg>
</div>
</body></html> 
```

### Crear el fichero .OPF

El fichero de contenidos (`content.opf` en nuestro ejemplo) es el que
explica o define el libro en si. Incluye una serie de metadatos, como
el autor, la fecha de publicación, genero... El ejemplo siguiente
vale como patrón, realizando los cambios oportunos:

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="uuid_id">
    <metadata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:language>en</dc:language>
    <dc:title>How to Build a Website</dc:title>
    <dc:creator opf:file-as="Kyrnin, Jennifer" opf:role="aut">Jennifer Kyrnin</dc:creator>
    <meta name="cover" content="cover"/>
    <dc:date>0101-01-01T00:00:00+00:00</dc:date>
    <dc:contributor opf:role="bkp"></dc:contributor>
    <dc:identifier id="uuid_id" opf:scheme="uuid">0c159d12-f5fe-4323-8194-f5c652b89f5c</dc:identifier>
    </metadata>
    <manifest>
    <item href="cover.jpeg" id="cover" media-type="image/jpeg"/>
    <item href="build_website.html" id="id1" media-type="application/xhtml+xml"/>
    <item href="page_styles.css" id="page_css" media-type="text/css"/>
    <item href="stylesheet.css" id="css" media-type="text/css"/>
    <item href="titlepage.xhtml" id="titlepage" media-type="application/xhtml+xml"/>
    <item href="toc.ncx" media-type="application/x-dtbncx+xml" id="ncx"/>
    </manifest>
    <spine toc="ncx">
    <itemref idref="titlepage"/>
    <itemref idref="id1"/>
    </spine>
    <guide>
    <reference href="titlepage.xhtml" type="cover" title="Cover"/>
    </guide></package> 
```

That's all the files you need, they should all be in a directory together
(except for container.xml, which goes in a sub-directory `META-INF`). We like to
then go to the container directory and make sure it has a name that reflects
the title and author names.  

Once you have the directory of files named how you want it you should use a Zip
archive program to zip the directory. My sample directory ends up as a zip file
named "How to Build a Website - Jennifer Kyrnin.zip".

Finally, change the file name extension from `.zip` to `.epub`. Your operating
system may protest, but go ahead with it. You want this to have an epub
extension.

Lastly, test your book. It's hard to get the epub format correct on the first
try, so you should always test your file. Open it in an epub reader like
Calibre. And if it doesn't display correctly, you can use Calibre to correct
problems.
