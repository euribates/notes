---
title: Notes on Vim
---

## Cómo hacer que Vim copie al portapapeles del sistema, ademas del interno

Este es el camino (Ponerlo en el fichero `.vimrc`):

```
set clipboard+=unnamedplus,unnamed
```

Referencia: `help: clipboard`

> When the `"unnamed"` string is included in the `clipboard` option, the unnamed
> register is the same as the `*` register.  Thus you can yank to and paste the
> selection without prepending `"*` to commands.


## Cómo incluir caracteres Unicode en Vim (Diagraphs)

| Keys                   | Meaning          | Symbol |
|------------------------|------------------|--------|
|++ctrl+shift+k++ `OK`   | OK               | ✓      |
|++ctrl+shift+k++ `XX`   | BALLOT X         | ✗      |
|++ctrl+shift+k++ `*1`   | BLACK STAR       | ☆      |
|++ctrl+shift+k++ `*2`   | WHITE STAR       | ★      |
|++ctrl+shift+k++ `AA`   | AND              | ∧      |
|++ctrl+shift+k++ `OR`   | OR               | ∨      |
|++ctrl+shift+k++ `-+`   | Más o menos      | ±      |
|++ctrl+shift+k++ `<<`   | Abre Comillas    | «      |
|++ctrl+shift+k++ `>>`   | Cierra comillas  | »      |
|++ctrl+shift+k++ `->`   | Flecha a derecha | →      |
|++ctrl+shift+k++ `*X`   | Multiplicación   | ×      |
|++ctrl+shift+k++ `?=`   | Aproximadamente  | ≅      |
|++ctrl+shift+k++ `?3`   | Equivalente      | ≡      |

Fuentes:

- [List of Unicode useful symbols](https://en.wikibooks.org/wiki/Unicode/List_of_useful_symbols)
- [RFC 1345 - Character Mnemonics and Character Sets](https://datatracker.ietf.org/doc/html/rfc1345)
- [Deep dive into Digraph - Part 1](https://hjkl.substack.com/p/deep-dive-into-digraph-part-1?s=r)


## Cómo resolver las búsquedas
	
Cuando buscamos, podemos resaltar los textos encontrados con:

```
:set hlsearch
```

Para desactivar el resaltado usar el siguiente comando (Ojo, es un comando no
una opción, no lleva `set`):

```
:nohlsearch
```

Fuentes:

- [Highlight all search pattern matches | Vim Tips Wiki](https://vim.fandom.com/wiki/Highlight_all_search_pattern_matches)


## Cuál es la diferencia entre `remap`, `noremap`, `nnoremap` y `vnoremap`

Note: `remap` es una opción que hace que los mapeos funcionen recursivamente.
Está activo por defecto y se recomienda dejarlo así. El resto son comandos que
funcionan así:

- `:map` y `:noremap` son las versiones **recursivas** y **no recursivas** de los
  diferentes comandos de mapeo. Por ejemplo, si ejecutamos:

```
:map j gg           (moves cursor to first line)
:map Q j            (moves cursor to first line)
:noremap W j        (moves cursor down one line)
```

Entonces:

- `j` se mapea a `gg`.

- `Q` también se mapea `gg`, porque `j` será expendido ya que se aplica
  recursividad.

- `W` se mapea a `j` (u no a `gg`) porque `j` no será expandido, ya que
se ha hecho un mapeo no recursivo.

Es importante recordar que Vim es un editor **modal**; tiene un modo
**normal**, un modo **visual**, entre otros. Hay un mapeo que funciona en los
modos normal, visual, selección y operador (`:map` y `:noremap`), uno que
funciona solo en modo normal (`:nmap` y `:nnoremap`), uno que funciona solo en
modo visual (`:vmap` t `:vnoremap`), etc.

Para más información sobre este tema:

- `:help :map`
- `:help :noremap`
- `:help recursive_mapping`
- `:help :map-modes`

Fuentes:

 - [StackOverflow - What is the difference between the remap, noremap, 
   nnoremap and vnoremap mapping commands in Vim?](https://stackoverflow.com/questions/3776117/what-is-the-difference-between-the-remap-noremap-nnoremap-and-vnoremap-mapping)

 - [Mapping keys in Vim - Tutorial (Part 1)](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1))


## Cómo reutilizar una selección visual

Often when editing code, I'll select a block in visual mode and do a search and
replace over the block. After I make the changes, however, it leaves visual
mode. How do you do a new find and replace over the same selection?

You may re-select the last selected visual area with `gv`.

Fuentes: 

- [StackOverflow - How do you reuse a visual mode selection?](https://superuser.com/questions/220666/how-do-you-reuse-a-visual-mode-selection)


## Dónde puedo obtener resumenes/chuletas sobre Vim

- [Vim Diff cheatshhet](https://devhints.io/vim-diff)
- [Vim Cheatshhet](https://vim.rtorr.com/)

## Plantillas automáticas por tipo de fichero (_skeletons_)

Vim has a built-in concept called **skeleton files** which allow you to
automatically populate a new file with a given template. Learn about it
with `:help skeleton`. The general idea of skeleton files is that you
configure your Vim to read a template from disk every time you open a
new, empty buffer with a filename that matches a given pattern.

Configuring these templates in your `.vimrc` is simple:

```
autocmd BufNewFile readme.md 0r ~/skeletons/readme.md
autocmd BufNewFile *.sh 0r ~/skeletons/bash.sh
```

-   `autocmd` -- run this automatically on some event
-   `BufNewFile` -- this is Vim's new file event
-   `readme.md` -- this is the pattern you want the new file to match
-   `0r` -- read into the buffer starting at line 0, the first line
-   `~/skeletons/readme.md` -- the file to read in

Tags: skeleton, snippets, templates, vim

Fuentes:

- [Automated file templates](https://vimtricks.com/p/automated-file-templates/)


## Cómo posicionar el cursor despues de una búsqueda

Se puede hacer de la siguiente manera:

```
/Fish/e
```

La `/e` del final posiciona el cursor al final del texto encontrado, en lugar
de posicionarse al principio, que es el comportamiento por defecto. Además se
puede añadir  `-n` o `+n` para posicionar el cursor `n` posiciones antes o
después de la posición final.

También se puede usar `/s[+|-]<num>` para posicionarse a partir del principo.
Usando `/Fish/s+2` te posiciona en la letra `s`.

Fuente: [StackOverflow - Is there a command in Vim/Vi to move the cursor to the end of a search highlight?](https://stackoverflow.com/questions/10707626/is-there-a-command-in-vim-vi-to-move-the-cursor-to-the-end-of-a-search-highlight)


## Como indentar/desindentar en modo de inserción.

Si estás en modo inserción, la combinación ++ctrl+t++ sirven para _indentar_ la
línea actual, mientras que ++ctrl+d++ sirve para _desindentar_. No importa en
que posición de la línea esté el cursor. Si escribes `0` y pulsas ++ctrl+d++,
la línea se _indentará_ al principio y el `0` que escribimos se borra. 

Fuente: [VimWorkgruop - Insert mode Ctrl-d](https://github.com/VimWorkgroup/workproducts/blob/master/examples/commands/i_Ctrl-d.md)


## Como activar/desactivar el corrector de sintaxis

Para habilitar o inhabilitar el corrector.

- `:set spell` activa el corrector. Yo por defecto no tengo habilitado
  el corrector ortográfico. Lo activo cuando voy a redactar un
  documento, pero cuando estoy escribiendo código, me incomoda mucho.

- `:set nospell` desactiva el corrector

Si queremos activar el corrector en español:

```vim
setlocal spell spelllang=es
```

Para navegar entre errores:

- `]s` te lleva hasta la siguiente palabra errónea. Si precedes esta
  combinación de teclas con un número, saltará tantas palabras
  erróneas como hayas indicado.

- `[s` te lleva a la palabra errónea anterior. Igual que en el caso
  anterior, anteponiendo un número, realizará la misma operación.

- `]S` funciona igual que `\]` pero no tiene en cuenta las palabras
  erróneas de otra región.

- `[S` igual que el anterior pero hacia atrás.

Para añadir o eliminar palabras al diccionario

- `zg` añade la palabra incorrecta sobre la que está el cursor al
  archivo definido en el parámetro de la configuración `spellfile`.

- `zG` funciona exactamente igual que `zg` pero añade la palabra a la
  lista de palabras interna.

- `zw` en este caso en lugar de guardar la palabra como correcta, la
  guarda como incorrecta. Así, en el caso de que se encuentre en el
  archivo `spellfile` la comentará.

- `zW` igual que en el caso anterior, pero en este caso la añade al
  listado interno, tal y como has visto en el caso anterior con `zg` y
  `zG`.

- `zug` y `zuw` deshacen las acciones de `zg` y `zw`. Lo mismo sucede
  con `zuG` y `zuW`, pero de nuevo en el caso de los listados
  internos.

También es posible realizar estas operaciones utilizando comandos:

- `[count]spellgood <palabra>` se comporta como `zg`

- `spellgood! <palabra>` funciona como `zG`

- `[count]spellwrong <palabra>` se comporta como `zw`

- `spellwrong! <palabra>` funciona como `zW`

Una vez estés sobre una palabra que tienes que corregir, simplemente
tienes que encontrar el reemplazo más adecuado para esa palabra. Para
ello, tienes que utilizar `z=`. Si estás sobre una palabra incorrecta,
te mostrará un listado de alternativas o posibilidades correctas para
reemplazar la palabra que tienes que corregir.

Fuentes: 

  - [El corrector ortográfico en Vim](https://atareao.es/tutorial/vim/el-corrector-ortografico-en-vim/)
  - [Using Spell Check in Vim](https://thejakeharding.com/using-spell-check-in-vim)


## Cómo activar el modo Django para plantillas

Usa `:setfiletype htmldjango` en Vim para seleccionar resaltado de sintaxis de
plantillas Django. Si queremos activar el resaltado de sintaxis solo para
Django y no para HTML, podemos usar `:setfiletype django` .

Etiquetas: #django


## Cómo integrar Vim con el porta papeles del sistema.

En los sistemas Unix/Linux hay **dos** porta papeles, independientes entre
si.

- **PRIMARY** - Este porta papeles copia el contenido solo con seleccionarlo.
  Podemos pegarlo normalmente con el botón intermedio del ratón (A veces, la
  rueda de _scroll_ que actúa también como botón).

- **CLIPBOARD** - Este porta papeles solo copia lo seleccionado con una
  combinación de tecla, normalmente ++ctrl+c++, y se pega con ++ctrl+v++, igual
  que en Windows.

En Mac/Windows, solo hay un porta papeles.

En los sistemas Linux/Unix, hay numerosas utilidades que modifican la forma
en que se sincronizan los porta papeles; si los dos se comportan como si solo
hubiera un porta papales, es probable que haya alguno de estos programas
funcionando.

Vim define dos registros para estos porta papeles:

- `*` usa el **PRIMARY**; mnemotécnico: e**S**trella para copia el **S**eleccionar.

- `+` usa el **CLIPBOARD**; mnemotécnico: Porque hay que seleccionar **+**
  combinación de teclas

En Windows/MAC, ambos registros se refieren al mismo, ya que solo hay un
porta papeles.

Estos registros se usan como cualquier otro registro, por ejemplo, para cortar
(`y`) y pegar (`p`) usando el registro PRIMARY:

```
"*yy
"*p
```

Estos atajos de teclado pueden ser útiles:

```
noremap <Leader>y "*y
noremap <Leader>p "*p
noremap <Leader>Y "+y
noremap <Leader>P "+p
```

Se puede configurar Vim para que usa por defecto el parta papeles del sistema
`CLIPBOARD` en vez del interno, que es el usado por defecto, usando la variable
`clipboard`:

- Con el valor `unnamed` usa `*` (`PRIMARY`)

- Con el valor `unnamedplus` usa `+` (`CLIPBOARD`)

Con estos valores, al copiar con `yy` o pegar con `p` se estará trabajando con
el porta papeles indicado.

Estos registros también se pueden usar con `let`:

```
:let @+=42
:let @*=42
```

Al usar **gVim**, se puede activar el comportamiento de "copia al seleccionar"
usado:

`:set guioptions+=a`. 

Normalmente esta opción está activa por defecto para GVim, usando el porta
papales `PRIMARY`, si estamos en Linux/Mac, pero no en Windows o MAC.
Con `:help 'clipboard'` podemos ver más opciones de configuaración.

Fuentes:

- [Stack Overflow - How can I copy text to the system clipboard from
Vim?](https://vi.stackexchange.com/questions/84/how-can-i-copy-text-to-the-system-clipboard-from-vim)


## Cómo activar/desactivar los números de línea en Vim

Para activar la numeración, `:set nu` o `set number` y pulsamos ++enter+. Para
desactivar, `:set nu!` o `:set number!`.


## Cómo usar el sistema integrado de ayuda

Está información está disponible con `:h help-summary`, `:h howdoi`, `:h quickref`.

If you're really stuck there's `:h index`, `:h option-list`,
`:h vim-variable` and `:h functions`, and if you are really stuck
there is `:h :helpgrep` or searching `:h help-tags` by hand.

Press `Ctrl-]` to follow the link (jump to the quickref topic).


## Cómo ajustar el directorio de trabajo al del fichero actual

Podemos ver el directorio actual con:

```
:pwd
```

Para cambiarlo al directorio del fichero actual:

```
:cd %:p:h
```

También se puede cambiar el directorio solo para la ventana actual. Cada
ventana maniene un directorio actual local, que puede ser diferentes del
directorio actual global:

```
:lcd %:p:h
```

En estas ordenes, `%` es el nombre del fichero actual, `%:p` es el fichero con
el _path_ completo, y `%:p:h` nos da el directorio, (la `h` significa la cabeza
o _head_ de la ruta completa.

!!! note "Cambiar automáticamente al directorio del fichero en edición"

    Para mantener siempre como directorio activo el del directorio que estemos
    editando, podemos poner en el fichero `.vimrc`:

    ```
    set autochdir
    ```


## Cómo abrir una terminal dentro de Vim

Desde Vim 8.0, hay una oredn `:term` que abre una terminal en una ventana
nueva. Para salir de la terminal, usa el comando `exit` o simplemente cerrar la
ventana con ++ctrl+shift+w++ y `:q`.

Fuentes:

- [How do I run a terminal inside of Vim? - Stack Overflow](https://stackoverflow.com/questions/1236563/how-do-i-run-a-terminal-inside-of-vim)


## Cómo desactivar Syntastic

Para desactivas Syntactic de la sesión actual:

```
:SyntasticToggleMode
```

Pare desactivarlo para un lenguanje específico, se puede definir una lista
vacía en la variable correspondiente, en el fichero `.vimrc`. Por ejemplo, para
desactivar el chequeo de HTML, se podría usar:

```
let g:syntastic_html_checkers = []
```

## Cómo usar un porgrama externo como un filtro dentro de Vim

El siguiente ejemplo es un _script_ en python para ordenar las
palabras de un contenido que se le pasa mediante la entrada
estándar:

```python
import sys

for line in sys.stdin:
    print(' '.join(sorted(line.split())))
```

POr ejemplo, si estamos editando el siguiente texto:
 
```
this is a line with some words
words on each line will be sorted
fried banana and cream
```

Podemos usar nuestro programa como un filtro así:

- Plsar `V` en la primera línea, luego `jj` para seleccionar las tres líneas.
- Escribir `!python sortwords.py` y pulsar ++enter++.

Debería producir el siuiente resultado:

```
a is line some this with words
be each line on sorted will words
and banana cream fried
```

Fuentes:

- [Use filter commands to process text](https://vim.fandom.com/wiki/Use_filter_commands_to_process_text/)


## Cómo salir rápidamente de Vim

In order to make quick saves in ViM I think the following is the
quickest trip there:

```
nmap <Leader>w :update<CR>
```

So just hitting the leader key, ++comma++ in my case, followed by the ++w++
key will save the changes, if there was any (update is line write, but
only if there is changes in the text).

Fuentes:

- [Coderwall: Quick save in vim](https://coderwall.com/p/0tmfjw/quick-save-in-vim)

## Cómo usar la calculadora del registro

Vim's expression register is a temporary register that can be used to
run snippets of Vim script. We can use this for a variety of things,
anytime we want to evaluate Vim script. One helpful use case for this is
to perform math calculations right inside Vim, inserting the result into
our document. To use the expression register, press `<ctrl-r>` `=` from
insert mode:

Type some simple calculation like `1 + 2` and press `<enter>` and `3`
will be inserted into your document. Think of the expression register as
a little Vim command line that evaluates whatever you put into it and
inserts the results into your document.

Fuentes:

- [VimTricks - Performing calculations](https://vimtricks.com/p/performing-calculations/)

If you want to search for `logging` or `logger` you can do:

```
:/logging\|logger
```

## Caracteres Unicode usados para crear diagramas y cajas

Este es el conjunto de caracteres definido
en el [Box Drawing Blocl](https://en.wikipedia.org/wiki/Box_Drawing).

``` 
      0 1 2 3 4 5 6 7 8 9 A B C D E F
      
250x  ─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋ ┌ ┍ ┎ ┏
251x  ┐ ┑ ┒ ┓ └ ┕ ┖ ┗ ┘ ┙ ┚ ┛ ├ ┝ ┞ ┟
252x  ┠ ┡ ┢ ┣ ┤ ┥ ┦ ┧ ┨ ┩ ┪ ┫ ┬ ┭ ┮ ┯
253x  ┰ ┱ ┲ ┳ ┴ ┵ ┶ ┷ ┸ ┹ ┺ ┻ ┼ ┽ ┾ ┿
254x  ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋ ╌ ╍ ╎ ╏
255x  ═ ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙ ╚ ╛ ╜ ╝ ╞ ╟
256x  ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬ ╭ ╮ ╯
257x  ╰ ╱ ╲ ╳ ╴ ╵ ╶ ╷ ╸ ╹ ╺ ╻ ╼ ╽ ╾ ╿
```

Un ejemplo de uso:

```
┌──┬┐  ╔══╦╗  ╓──╥╖  ╒══╤╕  ╭──┬╮  ┏━━┳┓  ┌──┬┒
│  ││  ║  ║║  ║  ║║  │  ││  │  ││  ┃  ┃┃  │  │┃
├──┼┤  ╠══╬╣  ╟──╫╢  ╞══╪╡  ├──┼┤  ┣━━╋┫  ├──┼┨
└──┴┘  ╚══╩╝  ╙──╨╜  ╘══╧╛  ╰──┴╯  ┗━━┻┛  ┕━━┷┛
```

Fuentes:

- [Box-drawing character - Wikipedia](https://en.wikipedia.org/wiki/Box-drawing_character)


## Definir el área para buscar/reemplazar

Estos son las expresiones definir el área donde se realizarán las operaciones
de búsqueda/sustitución:

| Expresión     | Descripción                                               |
|---------------|-----------------------------------------------------------|
| *number*      | En la linea indicada                                      |
| `.`           | En la línea actual                                        |
| `$`           | La última línea                                           |
| `%`           | Todo el contenido del fichero. Equivale a `1,$`           |
| `'t`          | En la posicion incicada por la marca `t`                  |
| `/pattern[/]` | La siguiente línea que case con el patrón `pattern`       |
| `?pattern[?]` | La línea anterior que case con `pattern`                  |
| `\/`          | La línea siguiente a la usada en la busqueda anterior     |
| `\?`          | La línea anterior a la usada en la busqueda anterior      |
| `\&`          | La siguiente línea que case con el patrón anterior        |


### Quantifiers, Greedy and Non-Greedy.

Using quantifiers you can set how many times certain part of you pattern
should repeat by putting the following after your pattern:

  Quantifier   Description
  ------------ ----------------------------------------------------------------
  `*`          Matches 0 or more of the preceding characters
  `\+`         Matches 1 or more of the preceding characters...
  `\=`         Matches 0 or 1 more of the preceding characters...
  `\{n,m}`     Matches from n to m of the preceding characters...
  `\{n}`       Matches exactly n times of the preceding characters...
  `\{,m}`      Matches at most m (from 0 to m) of the preceding characters...
  `\{n,}`      Matches at least n of of the preceding characters

### Options at the end

  letter   meaning
  -------- --------------------------------------------------------------
  c        Confirm every operation
  g        Replace all occurrences in the line (without g - only first)
  i        Ignore case for the pattern
  I        Don't ignore case for the pattern

### Escaped characters or metacharacters

So far our pattern strings were constructed from normal or literal text
characters. The power of regexps is in the use of metacharacters. These
are types of characters which have special meaning inside the search
pattern. With a few exceptions these metacharacters are distinguished by
a "magic" backslash in front of them. The table below lists some common
VIM metacharacters.

  \#     Matching
  ------ -----------------------------------------------------
  `.`    any character except new line
  `\s`   Whitespace character
  `\S`   Non-whitespace character
  `\d`   Digit
  `\D`   Non-digit
  `\x`   Hex digit
  `\X`   Non-hex digit
  `\o`   Octal digit
  `\O`   Non-octal digit
  `\h`   Head of word character (a,b,c...z,A,B,C...Z and \_)
  `\H`   Non-head of word character
  `\p`   Printable character
  `\P`   Like `\p`, but excluding digits
  `\w`   Word character
  `\W`   Non-word character
  `\a`   Alphabetic character
  `\A`   Non-alphabetic character
  `\l`   Lowercase character
  `\L`   Non-lowercase character
  `\u`   Uppercase character
  `\U`   Non-uppercase character

Fuentes:
- [Vim Regex](http://vimregex.com/)


### Cómo eliminar los espacios al final de las líneas en un fichero

**tl/dr**: Usar la siguiente orden:

```
:%s/\s\+$//e
```

Explicación: El comando busca en todo el contenido del archivo (`%`), por el
patrón «Uno o más espacios, antes del final de la línea» (`\s\+$`).  `\s`
encuentra espacios en blanco, espacios o tabuladores, y `\+` significa, la
expresión regular anterior, repetida una o más veces, y `$` es el final de la
línea. Si los encuentras, cambialos por una cadena vacía (No hay nada en la
segunda parte, `//`)/. Como hemos incluido el modificador final `e`, no se
muestra mensaje de error aunque no hubiera ninguna línea que cumpla el
criterio.


### How to Undo and Redo in Vim

To undo recent changes, from normal mode use the undo command:

- ++u++ undo last change (can be repeated to undo preceding commands)

- ++ctrl+r++ Redo changes which were undone (undo the undos).

- ++shift+u++ return the last line which was modified to its original state

- ++colon++   (reverse all changes in last modified line)

In Vim 7.0, a new feature has been included which allows a user to jump
back or forward to any point of editing. For example, I am editing a
document and after a couple of minutes (say 10 min), I realise that I
have made a mistake. I can easily take the document to a point 10
minutes back by using the command:

```
:earlier 10m
```

Or for that matter, move to a point 5 seconds ahead by using the
command:

```
:later 5s
```

You can use the command `:undolist` to see a list of undo branches
existing in the buffer. And each branch will have a number associated
with it and it is possible to move to the undo level by using the
command: `:undo`.

### Using viewports

A really useful feature in Vim is the ability to split the viewable area
between one or more files, or just to split the window to view two bits
of the same file more easily. The Vim documentation refers to this as a
**viewport** or **window**, interchangeably.

Vim viewport keybinding quick reference

- `:sp` will split the Vim window horizontally. Can be written out
  entirely as `:split`.
- `:vsp` will split the Vim window vertically. Can be written out as
  `:vsplit`.
- `Ctrl-w Ctrl-w` moves between Vim viewports.
- ++ctrl+w++ ++j++ moves one viewport down.
- ++ctrl+w++ ++k++ moves one viewport up.
- ++ctrl+w++ ++h++ moves one viewport to the left.
- ++ctrl+w++ ++l++ moves one viewport to the right.
- ++ctrl+w++ ++equal++ tells Vim to resize viewports to be of equal size.
- ++ctrl+w++ ++minus++ reduce active viewport by one line.
- ++ctrl+w++ ++plus++ increase active viewport by one line.
- ++ctrl+w++ ++q++ will close the active window.
- ++ctrl+w++ ++r++ will rotate windows to the right.
- ++ctrl+w++ ++shift+r++ will rotate windows to the left.

The `:sp` command will divvy up the viewport into two equal viewports
for the file that you have open. If you'd like to work on two files
simultaneously, no problem -- just follow the command with the filename
you'd like to use, like this:

```
:sp filename
```

let's say you want to open a reference file in the top viewport, but
want the majority of the viewport available for the file you're actually
editing. No problem. Just prepend a number to the `sp` command, and the
new viewport will fill that number of lines:

```
:10 sp filename
```

To move between the viewports while working, use ++ctrl+w++ ++j++ to move down,
and ++ctrl+w++ ++k++ to move up. This should prove easy to remember --
++ctrl+w++ for "window" commands, and the normal vi movement commands ++j++ for
down and ++k++ for up. You can also cycle between viewports by using ++ctrl+w++
++ctrl+w++.

Fuentes:

- [Vim Tipos: Using viewports](https://www.linux.com/learn/vim-tips-using-viewports)


## Cómo usar sesiones

Seguimos los siguientes pasos:

- Open any number of tabs you wish to work with

- From any tab, press ++esc++ and enter the command mode. Type

```
:mksession header-files-work.vim
```

y pulsa ++enter++.

La configuración de pestañas y buffers de la sesión actual se almacenará en el fichero indicado.

To see restore in action, close all tabs and Vim. Either start vim with
your session using: `vim -S header-files-work.vim` or open vim with
any other file and enter command mode to type
`:source header-files-work.vim` and BOOM! All your tabs are opened for
you just the way you saved it! If you change any session tabs
(close/open new), you can save that back using `:mks!` while you are in
the session


## Cómo plegar/desplegar secciones de texto manualmente

Hay que posicionarse al principio del bloque que queremos plegar, por ejemplo,
al inicio de la definición de una una fución, y pulsar `mb`, para poner la
marca `b` (O cualquier otra marca que queramos). Luego nos movemos al final y
escribimos `zf'b`

Con `zd` podemos borrar el plegado. El texto no se borra, solo el plegado. Las
ordenes `zo` y `zc` abren y cierran un plegado respectivamente. PUede ser más
fácil usar La orden `za` que alterna (_toogle_) entra ambos estados. 

Fuentes:

- [Folding | Vim Tips Wiki | Fandom](https://vim.fandom.com/wiki/Folding)

## Vim tab-pages

- `:tabedit file` , will open a new tab and take you to edit file

- To navigate between these tabs, you can be in normal mode and type :
  `gt` or `gT` to go to next tab or previous tab respectively. You can
  also navigate to a particular index tab (indexed from 1) using
  `{i}gt` where, i is the index of your tab. Example: `2gt` takes you
  to 2nd tab

- To directly move to first tab or last tab, you can enter the
  following in command mode: `:tabfirst` or `:tablast` for first or
  last tab respectively.

- To move back and forth `:tabn` for next tab and `:tabp` for previous
  tab

- You can list all the open tabs using `:tabs`

- To open multiple files in tabs: `$ vim -p source.c source.h`

- To open multiple files using find `$ vim -p $(find ...)`

- To close a single tab `:tabclose` and to close all other tabs except
  the current one `:tabonly`

- Use the suffix `!` to override changes of unsaved files

## Cómo usar ctags con Vim

Ejecutar `ctags` en modo recursivo en el directorio que nos interese:

```shell
ctags -R *
```

Para localizar un _tag_ determinado y abrir Vim con el fichero que
contienen la definición del mismo, usar:

```shell
vim -t <tag>
```

O, si estamos dentro de Vim, podemos usar los siguienes comandos:

| Keyboard | command                                        |
|----------|------------------------------------------------|
| `Ctrl-]` | Jump to the tag underneath the cursor          |
| `Ctrl-t` | Jump back up in the tag stack                  |
| `:ts`    | Search for a particular tag                    |
| `:tag`   | Locate a particular tag                        |
| `:tn`    | Go to the next definition for the last tag     |
| `:tp`    | Go to the previous definition for the last tag |
| `:ts`    | List all of the definitions of the last tag    |

El primer comando es seguramente el más usado: ++ctrl+bracket-right++ salta
a la definición de la etiqueta que esta bajo el cursor (Nombres de funciones,
clases, métodos, etc.).

La segunda orden, ++ctrl+t++ se usa para regresar, recorriendo el camino hacia
atras de las busqyedas que hayamos hechjo con el primero.

Los siguientes comandos `:tag`, `:tn`, `:tp` and `:ts` pueden ser usados para
buscar cualquier etiqueta, independientemente del fichero donde pueda estar
definida. Si hubiera múltiples candidatos para la definición, con las ordenes
`tn` y `tp` podemos ir recorriendolas de una en una, hacia adelante o hacia
atras, o también podemos usar `ts` para seleccionar desde una lista la
definiión que nos interesa.

Fuentes:

 - [Weicode - Configuring ctags for Python and Vim](https://weicode.wordpress.com/2018/05/01/configuring-ctags-for-python-and-vim/comment-page-1/)


## Wrap Existing Text at N Characters in Vim

Set the `textwidth` variable:

```vim
:set textwidth=80
```

You might want this setting to apply automatically within certain file
types like Markdown:

```
au BufRead,BufNewFile *.md setlocal textwidth=80
```

Source:
<https://thoughtbot.com/blog/wrap-existing-text-at-80-characters-in-vim>

## How to setup a line length marker in vim/gvim

Just execute this:

```
:set colorcolumn=72
```

You can also prefix the argument with `-` or `+` to put the marker that many
columns to the left or right of `textwidth` (Ver sección previa), and it
accepts a comma-separated list of columns. I think the colorcolumn option is
only in Vim 7.3

- Source: [Super User - How to setup a line length marker in vim/gvim?](https://superuser.com/questions/249779/how-to-setup-a-line-length-marker-in-vim-gvim)

### How to Remove duplicated lines

The following command will sort all lines and remove duplicates (keeping
unique lines):

```vim
:sort u
```

Source: [Uniq - Removing duplicate
lines](https://vim.fandom.com/wiki/Uniq_-_Removing_duplicate_lines)

## Basic vi Commands

The following sections explain the following categories of vi commands.

### Moving around in a file

| Keyboard | Command                                                  |
-----------|----------------------------------------------------------|
| `Ctrl-b` | Move back one full screen (Remenmber b for backwards)    |
| `Ctrl-f` | Move forward one full screen (Remenmber f for fordwards) |
| `Ctrl-d` | Move forward 1/2 screen (Remenmber d for down)           |
| `Ctrl-u` | Move back (up) 1/2 screen (Remember u for up)            |

Moving the Cursor When you start vi, the cursor is in the upper left corner of
the vi screen. In command mode, you can move the cursor with a number of
keyboard commands. Certain letter keys, the arrow keys, and the Return key,
Back Space (or Delete) key, and the Space Bar can all be used to move the
cursor when you're in command mode.

!!! note "La mayoría de las ordenes de Vi distinguen mayúsculas y minusculas"

    La misma letra en mayúsculas o en minúsculas pueden tener efectos
    diferentes.

If your machine is equipped with arrow keys, try these now. You should be able
to move the cursor freely about the screen by using combinations of the up,
down, right, and left arrow keys. Notice that you can only move the cursor
across already existing text or input spaces.

If you're using vi from a remote terminal, the arrow keys might not work
correctly. The arrow key behavior depends on your terminal emulator. If the
arrow keys don't work for you, you can use the following substitutes:

-   To move left, press `h`
-   To move right, press `l`
-   To move down, press `j`
-   To move up, press `k`
-   Press `w` ("word") to move the cursor to the right one word at a
    time.
-   Press `b` ("back") to move the cursor to the left one word at a
    time.
-   Press `W` or `B` to move the cursor past the adjacent punctuation to
    the next or previous blank space.
-   Press `e` ("end") to move the cursor to the last character of the
    current word.
-   Press `^` to move the cursor to the start of the current line.
-   Press `$` to move the cursor to the end of the current line.
-   Press the Return key to move the cursor to the beginning of the next
    line down.
-   Press the Back Space key to move the cursor one character to the
    left.
-   Press the Space Bar to move the cursor one character to the right.
-   Press `H` ("high") to move the cursor to the top of the screen.
-   Press `M` ("middle") to move the cursor to the middle of the screen.
-   Press `L` ("low") to move the cursor to the bottom of the screen.
-   press `Ctrl-F` for page forward one screen
-   press `Ctrl-D` to scroll forward One-Half Screen

Page Backward One Screen To scroll backward (that is., move up) one
screenful, press Ctrl-B.

Scroll Backward One-Half Screen To scroll backward one half of a screen,
press Ctrl-U.

### Inserting Text

vi provides many commands for inserting text. This section introduces
you to the most useful of these commands. Note that each of these
commands places vi in entry mode. To use any of these commands, you must
first be in command mode. Remember to press Esc to make sure you are in
command mode.

Append Type `a` (append) to insert text to the right of the cursor.
Experiment by moving the cursor anywhere on a line and typing a,
followed by the text you want to add. Press Esc when you're finished.

Type ++shift+a++ to add text to the end of a line. To see how this command
works, position the cursor anywhere on a text line and type `A`. The
cursor moves to the end of the line, where you can type your additions.
Press Esc when you are finished.

Insert text to the left of the cursor by typing ++i++ from command
mode.

Type ++shift+i++ to insert text at the beginning of a line. The command moves
the cursor from any position on that line. Press ++esc++ to return to
command mode after you type the desired text.

### Open Lines

Use these commands to open new lines, either above or below
the current cursor position.

Type `o` to open a line below the current cursor position. To
experiment, type `o` followed by a bit of text. You can type several
lines of text if you like. Press `Esc` when you are finished.

Type `O` to open a line above the current cursor position.

Changing Text Changing text involves the substitution of one section of
text for another. vi has several ways to do this, depending on
circumstances.

Changing a Word To replace a word, position the cursor at the beginning
of the word to be replaced. Type `cw`, followed by the new word. To
finish, press `Esc`.

To change part of a word, place the cursor on the word, to the right of
the portion to be saved. Type `cw`, type the correction, and press
`Esc`.

Changing a Line To replace a line, position the cursor anywhere on the
line and type `cc`. The line disappears, leaving a blank line for your
new text (which can be of any length). Press `Esc` to finish.

Substituting Character(s) To substitute one or more characters for the
character under the cursor, type `s`, followed by the new text. Press
`Esc` to return to command mode.

Replacing One Character Use this command to replace the character
highlighted by the cursor with another character. Position the cursor
over the character and type `r`, followed by just one replacement
character. After the substitution, vi automatically returns to command
mode (you do not need to press Esc).

### Deleting Text

These commands delete the character, word, or line you indicate. vi
stays in command mode, so any subsequent text insertions must be
preceded by additional commands to enter entry mode.

Deleting One Character: position the cursor over the character to be
deleted and type `x`.

The `x` command also deletes the space the character occupied---when a
letter is removed from the middle of a word, the remaining letters will
close up, leaving no gap. You can also delete blank spaces in a line
with the `x` command.

To delete one character before (to the left of) the cursor, type `X`
(uppercase).

Deleting a Word or Part of a Word To delete a word, position the cursor
at the beginning of the word and type `dw`. The word and the space it
occupied are removed.

To delete part of a word, position the cursor on the word to the right
of the part to be saved. Type `dw` to delete the rest of the word.

Deleting a Line To delete a line, position the cursor anywhere on the
line and type `dd`. The line and the space it occupied are removed.

Copying and Moving Text --- Yank, Delete, and Put Many word processors
allow you to "copy and paste" and "cut and paste" lines of text. The vi
editor also includes these features. The vi command-mode equivalent of
"copy and paste" is yank and put. The equivalent of "cut and paste" is
delete and put.

The methods for copying or moving small blocks of text in vi involves
the use of a combination of the yank, delete, and put commands.

Copying Lines Copying a line requires two commands: `yy` or `Y` ("yank")
and either `p` ("put below") or `P` ("put above"). Note that `Y` does
the same thing as `yy`.

The `yy` command works well with a count: to yank 11 lines, for example,
type `11yy`. Eleven lines, counting down from the cursor, are yanked,
and vi indicates this with a message at the bottom of the screen: 11
lines yanked.

You can also use the `P` or `p` commands immediately after any of the
deletion commands discussed earlier. This action puts the text you
deleted above or below the cursor, respectively.

Fuente: [Basic vi Commands](https://docs.oracle.com/cd/E19683-01/806-7612/6jgfmsvqf/index.html)


## Mapping keys in Vim

Key mapping refers to creating a shortcut for repeating a sequence of keys or commands.
Vim supports several editing modes - `normal`, `insert`, `replace`, `visual`, `select`, `command-line` and `operator-pending`. You can map a key to work in all or some of these modes.

The general syntax of a map command is:

```
{cmd} {attr} {lhs} {rhs}
```

where:

- `{cmd}` is one of `:map`, `:map!`, `:nmap`, `:vmap`, `:imap`, `:cmap`,
  `:smap`, `:xmap`, `:omap`, `:lmap`, etc.

- `{attr}` is optional and one or more of the following: `<buffer>`,
  `<silent>`, `<expr> <script>`, `<unique>` and `<special>`. More than one
  attribute can be specified to a map.

- `{lhs}`  left hand side, is a sequence of one or more keys that you will use
       in your new shortcut.

- `{rhs}`  right hand side, is the sequence of keys that the {lhs} shortcut keys
       will execute when entered.

Note that you **cannot map** the ++shift++ or ++alt++ or ++ctrl++ keys alone as
they are key modifiers. You have to combine these key modifiers with other keys
to create a map.

The first step in creating a map is to **decide the sequence of keys** the
mapping will run. When you invoke a map, Vim will execute the sequence of keys
as though you entered it from the keyboard. You can test the keys for your
mapping by manually entering the key sequence and verifying that it performs
the desired operation.

The second step is to **decide the editing mode** (insert mode, visual mode,
command-line mode, normal mode, etc.) in which the map should work. Instead of
creating a map that works in all the modes, it is better to define the map that
works only in selected modes.

The third step is to **find an unused key sequence** that can be used to invoke
the map. You can invoke a map using either a single key or a sequence of keys.
:help map-which-keys 


Sources:

- [Mapping Keys in Vim (Part 1)](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1))
- [Mapping Keys in Vim (Part 2)](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_2))
- [Mapping Keys in Vim (Part 3)](https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_3))


## Vim help and keywordprg

As you might have heard by now - the best resource for learning Vim is still
the integrated Vim help. Just type `:help` or `:h` followed by a help tag and
hit the enter key.  For example `:h :s<CR>` to read and learn about the
substitute command.

But sometimes you don't know the exact keywords you can use. There are 2
built-in solutions I know of that I constantly use. First is to use the `TAB`
key to auto-complete the help tags. For example `:h sub<TAB>` and this should
give you a matching list you can iterate with further TAB key presses. Select
one and hit enter.

The second method is to use the `:helpgrep` or `:lhelpgrep` command followed by a
keyword. For example `:lhelpgrep substitute<CR>` and this gives you a location
list (or quickfix list in case `:helpgrep`) showing all occurrences of the given
keyword. Use `:lopen` or `:copen` to show these lists. I suggest here only to learn
about that and to maybe setup some mappings for faster list navigation/usage.

Vim can also show the manuals of the plugins you have installed. I don't know
if a plugin manager handles that automatically (because I don't use one) but I
have to update my help tags manually. For that I run `:helptags
path/to/doc/folder<CR>` for example `:helptags ~/.vim/doc<CR>` and now the help
tags can be accessed with the `:help` command.

The last but very useful tip is the usage of the `K` command. When you have the
Vim help open or when you write a Vim script then you can put your cursor on
help tags or Vim commands and press `K`. This will bring you directly to the help
of the keyword under the cursor. With that you can navigate quickly in the Vim
help. Use `Ctrl-o` to jump back on the jump list. The `K` command makes use of the
keywordprg setting and on some systems this is set up for manpages instead of
the Vim help. So maybe you have to put set `keywordprg=:help` in your vimrc. But
manpages can be very useful too for example when writing Bash scripts. So maybe
you want to be able to toggle between the Vim help and manpages. You could put
the following in your vimrc for toggling (replace <yourkey> with a keystroke
you like) ...

	
```vim
nnoremap <yourkey> :if &keywordprg == ":help" <BAR> set keywordprg=man <BAR>
else <BAR> set keywordprg=:help <BAR> endif <BAR> set keywordprg?<CR>
```

Fuente: [Reddit - Vim help and keyworddprg](https://www.reddit.com/r/vimdailytips/comments/iruu9s/vim_help_and_keywordprg/)

## Como salvar un fichero protegido si no lo hemos editado como root

**TL/DR**: Hay que hacer:

```
:w !sudo tee %
```

**Explicación**: La orden `:w !sudo tee %` pasará el contenido del _buffer_
actual al comando `sudo tee %s`, donde `%` es el nombre del fichero actual.
Obviamente, nos pedirá la contraseña para poder ejecutar el comando `sudo`.

Para entender `tee`, podemos pensar en este comando como un una unión de
tubería con una entrada y dos salidas. Todo lo que se le pasa a la entrada
estándar de `tee` se escribe en el fichero que se le pasa como parámetro y
**también** en la salida estándar, lo que permite seguir procesando los datos
con otro comando.

Por ejemplo, la orden `ps -ax | tee processes.txt | grep 'foo'` lista los
procesos, los escribe en el fichero `processes.txt` y luego los filtra usando
`grep`:

```
 ╭───────────╮      ╭────────────╮     ╭─────────────╮
 │           └──────┘            └─────┘             │
 │  ps -ax   ┌──────┐  tee       ┌─────┐  grep 'foo' │
 │           │      │            │     │             │
 ╰───────────╯      ╰─────┐ ┌────╯     ╰─────────────╯
                          │ │
                   ╒══════╛ ╘══════╕
                   │               │
                   │ processes.txt │
                   │             ┌─┤
                   └─────────────┴─╯ 
```

En esta situación, sin embargo, ignoramos la mitad de lo que hace `tee`, ya que
descartamos la salida estándar final. Solo usamos `tee` para poder ejecuarlo con
`sudo` y que pueda sobreescribir el fichero original. La ventaja es que si nos
equivocamos con la contraseña, `sudo` fallará y el siguiente comando en el
_pipeline_ nunca se ejecutará, impidiendo así que borremos el contenido del
fichero.

Fuentes: 

- [How does the vim &quot;write with sudo&quot; trick work? - Stack Overflow](https://stackoverflow.com/questions/2600783/how-does-the-vim-write-with-sudo-trick-work/7078429)

## How to change in gvim GTK file browser the default file mask wildcard (glob)

The `browsefilter` variable is a convenient way to add custom glob like filters
for the graphical :browse dialog and select only the relevant filetypes for
display.

For MS-Windows and GTK, you can modify the filters that are used in the browse
dialog.  By setting the `g:browsefilter` or `b:browsefilter` variables, you can
change the filters globally or locally to the buffer.  The variable is set to
a string in the format `"{filter label}\t{pattern};{pattern}\n"` where `{filter
label}` is the text that appears in the "Files of Type" comboBox, and
`{pattern}` is the pattern which filters the filenames.  Several patterns can be given,
separated by `';'`.

For example, to have only Vim files in the dialog, you could use the following
command:

```
let g:browsefilter = "Vim Scripts\t*.vim\nVim Startup Files\t*vimrc\n"
```

You can override the filter setting on a per-buffer basis by setting the
`b:browsefilter` variable.  You would most likely set `b:browsefilter` in a
**filetype plugin**, so that the browse dialog would contain entries related to
the type of file you are currently editing.  Disadvantage: This makes it
difficult to start editing a file of a different type.  To overcome this, you
may want to add "All Files\t*.*\n" as the final filter, so that the user can
still access any desired file.

To avoid setting browsefilter when Vim does not actually support it, you can
use has("browsefilter"):

```
if has("browsefilter")
    let g:browsefilter = "whatever"
endif
```

Fuente: [StackExchange](https://vi.stackexchange.com/questions/22905/how-to-change-in-gvim-gtk-file-browser-the-default-file-mask-wildcard-glob)
