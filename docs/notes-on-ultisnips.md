---
title: Notes on Ultisnips
---

## UltiSnips

To use **UltiSnips**, you need a python enabled Vim version 7 or
greater. You have python if either `:echo has("python")` or
`:echo has("python3")` yields `1`. Recent versions have been tested with
python 2.7 and python 3.2, theoretically, UltiSnips should work with all
versions \>= python 2.6.

UltiSnips tries to autodetect which Vim Python command to use (there are
two: :py and :py3). Unfortunately, some Vim versions choke when you test
for both versions. In this case you have to tell UltiSnips which version
to use:

```
let g:UltiSnipsUsePythonVersion = 2   " or 3
```

You can use the order `:UltiSnipsEdit` to create or edit a custom
UltiSnips file for the file type being currently edited. When you seve
the snippets file, the conntent is automcatically updated.

This will create a directory [\$HOME/.vim/UltiSnips]{.title-ref}. You
can create this directory manually, if you want. (Be careful **DO NOT**
create a directory named [snippets]{.title-ref}, this name is used
internally on the source code of UltiSnips).


## What are snippets

**Snippets** are portions of text you can include in your editor using only
a few kwystrokes

Lets write a snippet to include my email signature with only four
keystroks:

```
    snippet sig "Email signature" b
    Juan Ignacio Rodríguez de León

    --
    Saludos desde las Islas Canarias
    email: menganito@invented-email.com
    phone: xxx-xxx-xxx
    endsnippet
```

The text to be inserted is all the text included betwwen `snippet` and
`endsnippet`. The initial `snippet` has also three parameters:

1) First one is the **trigger**, the sequece of caracters that will
execute the snippet. In this example it is `sig`, so I can activate this
triggers just writting `sig` followed by the `tab` key.

Generally a single word is used but the trigger can include spaces. If
you wish to include spaces, you must wrap the tab trigger in quotes.

2) The second argument is just a text that describes the trigger. Is
optional but is a good practice to put something here that could help us
to tell apart one snippet from others. Also it would be used to
distinguishing it from other snippets with the same tab trigger. When a
snippet is activated and more than one tab trigger match, UltiSnips
displays a list of the matching snippets with their descriptions. The
user then selects the snippet they want.

3) Third and last parameter is the options. We will see the options
later, but for this simple example, the `b` option means this trigger
will only be activated if it is written at the *begining* of the line.

Exercise: Write your own signature trigger. Check it only works at the
beginign of a sentence.


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
