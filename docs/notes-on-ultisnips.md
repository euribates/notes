---
title: Notes on Ultisnips
tags:
  - vim
  - python
---

## UltiSnips y Python

Para usar **UltiSnips** hay que tener Python activo y usar vim desde la versión
7 en adelante. Para saber si Python está activo podemos usar:

```
:echo has("python")
```

o

```
:echo has("python3")
``` 

Alguno de los dos debería retornar un $1$. UltiSnips intenta determinar
automáticamente la versión de Python que debe usar, pero si por la que sea
queremos forsarla podemos hacer:

```
let g:UltiSnipsUsePythonVersion = 2   " or 3
```

## Cómo crear tus propios _snippets_

Puedes usar `:UltiSnipsEdit` para crear o editar un fichero
personalizado, basandose en el tipo de fichero que estés editando
en ese momento. Cuando salves el fichero de snippets, los cambios
estarán disponibles de inmediato.

Los _snippets_ personalizados se almacenan en la carpeta
`$HOME/.vim/UltiSnips`, con el nombre `{language}.snippets`, por ejemplo los
_snippets_ personales para javascript se encuentran en:

`$HOME/.vim/UltiSnips/javascript.snippets`


## Qué son los spippets

Los **Snippets** son pequeñas plantillas de texto que se pueden incluir en el
texto que estés editando usando solo un par de pulsaciones de teclas.

Vamos a escribir un pequeño _snippet_ para incluir mi firma de correo electrónico usando solo cuatro pulsaciones:

```
snippet sig "Email signature" b
Juan Ignacio Rodríguez de León

--
Saludos desde las Islas Canarias
email: menganito@invented-email.com
phone: xxx-xxx-xxx
endsnippet
```

El texto a ser insertado es todo lo incluido desde la palabra `snippet` hasta
`endsnipet`. La palabra clave inicial, `snippet`, tiene además tres parámetros:

1) El primero es lo que se conoce como el **disparador** o **trigger**, es la
secuencia de caracteres que provocarán la ejecución del _snippet_. En este caso
es la secuencia de caracteres `sig`, de forma que para activar la secuencia
escribiré `sig` y luego pulsare la tecla ++tab++.

Generalmente solo se usa una palabra como disparador, pero se pueden usar
varias separadas por espacios, pero en ese caso hay que entrecomillar todo el
disparador.

2) El segundo parámetro es simplemente una descripción textual del _snippet_.
Es opcional, pero resulta una buena práctica usar un texto corto pero
descriptivo que nos sirva para diferenciar los _snippets_ entre si. También
resulta muy útil si tenemos varios _snippets_ que comparte un mismo disparador;
en estos casos, Ultisnips nos mostrará una lista de los posibles _snippets_
disponibles, usando sus descripciones, para que el usuario pueda seleccionar el
que quiere usar.

Ejemplo: Escribir dos _snippets_ con el mismo _trigger_. Intentar dispararlo y
comprobar que te muestra las opciones disponibles.

```
snippet sig "Email personal" b
Juan Ignacio Rodríguez de León

--
Saludos desde las Islas Canarias
email: menganito@invented-email.com
phone: xxx-xxx-xxx
endsnippet

snippet sig "Email trabajo" b
D. Juan Ignacio Rodríguez de León
--
email: mira.que.serio@invented-email.com
web: http://megaempresa.com/
endsnippet
```

3) El tercer y último parámetro son las opciones. Se verán con más detalle en
otra sección, pero para este ejemplo, solo aclarar que la opción `b` (de
_begin_) significa que esta regla solo se disparará si el _snippet_ está
escrito **al principio de la línea**.


### Static and dinamic snippets

So, for the moment, we only can use this to include some static code.
but snippets could be more elaborated.


### Tab Stops and placeholders

Let\'s see another example. Imagine in your code you need to define
several times some `user` entries like this:

```
jileon = {
    "login": "fulanito",
    "uid": 115,
    "gid": 15,
    "email": "fulanito@invented-email.com",
}
```

We could make this snippet to help us:

```
snippet user "User python dict"
$1 = {
    "login": "$1",
    "uid": $2,
    "gid": $3,
    "email": "$1@invented-email.com",
}
endsnippet
```

This `$1`, `$2`, `$3`\... codes have a special meaning in UltiSnips,
they are called **TabStops**. We can trigger the snippets and start
filling this value:

```
jileon = {
    "login": "menganito",
    "uid": ,
    "gid": ,
    "email": "menganito@invented-email.com",
}
```

La marca `$1` se ha usado en varios sitios. La primera ocurrencia marca el sitio
donde se posiciona el cursor para empezar a escribir. El resto de las
ocurrencias se llaman **espejos** o **Mirrors** porque reflejan los cambios
realizados en la primera marca.

Lets look at another, more interesting example. Lets write a snippet to
turn any URL as a HTML a tag, like this:

> \<a href=\"<http://www.python.org/>\"\><http://www.python.org>\<a\>

Si this is a \<a href=\"htt\"\>htt\</a\>

!!! note 'Asociación de los snippets por tipo de fichero`

    `UltiSnipsEdit` opens or creates your private snippet definition file for
    the current filetype. You can easily open them manually of course, this is
    just a shortcut. There is also a variable called: `g:UltiSnipsEditSplit`
    which can be set to `normal` (default), `horizontal` or `vertical` that
    defines if a new window should be opened.

### The options part

The options control the behavior of the snippet. Options are indicated
by single characters. The options characters for a snippet are combined
into a word without spaces.

Las opciones actualmente soportadas son:

- `b`: Beginning of line - A snippet with this option is expanded only if the
  tab trigger is the first word on the line. In other words, **expend only if
  whitespace precedes the tab trigger**. The default is to expand snippets at
  any position regardless of the preceding non-whitespace characters.

- `i`: In-word expansion - By default a snippet is expanded only if the tab
  trigger is the first word on the line or is preceded by one or more
  whitespace characters. A snippet with this option is expanded regardless of
  the preceding character. In other words, **the snippet can be triggered in
  the middle of a word**.

- `w`: Word boundary - With this option, the snippet is expanded if both tab
  trigger start and end matches a word boundary.  In other words the tab
  trigger must be **preceded and followed by non-word characters**. Word
  characters are defined by the \'iskeyword\' setting. Use this option, for
  example, to permit expansion where the tab trigger follows punctuation
  without expanding suffixes of larger words.

- `r`: Regular expression - Wih this option, the tab trigger is expected to be
  **a python regular expression**. The snippet is expanded if the recently
  typed characters match the regular expression. Note: The regular expression
  **MUST** be quoted (or surrounded with another character) like a multi-word tab
  trigger (see above) whether it has spaces or not. A resulting match is passed
  to any python code blocks in the snippet definition as the local variable
  \"match\".

- `t`: Do not expand tabs - If a snippet definition includes leading tab
  characters, by default UltiSnips expands the tab characters honoring the Vim
  `shiftwidth`, `softtabstop`, `expandtab` and `tabstop` indentation settings.
  (For example, if `expandtab` is set, the tab is replaced with spaces.) If
  this option is set, UltiSnips will ignore the Vim settings and insert the tab
  characters as is. This option is useful for snippets involved with tab
  delimited formats.

- `s`: **Remove whitespace immediately before the cursor at the end of a line
  before jumping to the next tabstop**. This is useful if there is a tabstop
  with optional text at the end of a line.

- `m`: **Trim all whitespaces from right side of snippet lines**. Useful when
  snippet contains empty lines which should remain empty after expanding.
  Without this option empty lines in snippets definition will have indentation
  too.

- `e`: Custom context snippet - With this option expansion of snippet can be
  controlled not only by previous characters in line, but by any given python
  expression. This option can be specified along with other options, like
  `b`. See `UltiSnips-custom-context-snippets` in help for more info.

- `A`: Snippet will be triggered automatically, when condition matches. See
  `UltiSnips-autotrigger` for more info.


## Fuentes e información adicional

-   Silver\'s Castle UltiSnips screencast
    -   [UltiSnips Screencast Episode
        1](https://www.sirver.net/blog/2011/12/30/first-episode-of-ultisnips-screencast/):
        What are snippets and I do needed it?
    -   [UltiSnips Screencast Episode
        2](https://www.sirver.net/blog/2012/01/08/second-episode-of-ultisnips-screencast/):
        The most common features of UltiSnips
-   [How I\'m able to take notes in mathematics lectures using LaTeX and
    Vim](https://castel.dev/post/lecture-notes-1/)
-   [A modern vim plugin for editing LaTeX
    files](https://github.com/lervag/vimtex)
-   [UltiSnippets
    screencast](https://www.youtube.com/watch?v=f_WQxYgK0Pk)) in YouTube
-   [Using selected text in UltiSnips
    snippets](http://vimcasts.org/episodes/ultisnips-visual-placeholder/)
    in VIM Casts
