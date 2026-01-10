ctags
========================================================================


`Ctags <https://ctags.sourceforge.net/>`__ es una herramienta para
programadores que genera un índice (un fichero llamado ``tags``) con los
nombres encontrados en el código fuente de los programas. `Exuberant
Ctags entiende varios tipos de
lenguajes <https://ctags.sourceforge.net/languages.html>`__ (41 en la
actualidad, 13/sep/2024) incluyendo C, C++, C#, Python, Eiffel, Java,
JavaScript, PHP, Ruby, o *Shell scripts* (Bourne/Korn/Z).

Dependiendo del lenguaje, se indexarán nombres de variables, funciones,
clases, métodos, macros, etc. De esta forma, `otros programas, sobre
todo editores diferentes (vim, Emacs, …), son capaces de usar
ctags <https://ctags.sourceforge.net/tools.html>`__ para proporcionar
acceso rápido a las definiciones.

Qué lenguajes puede procesar ctags, y como sabe que lenguaje es?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A menos que se especifique (con la opción ``--lenguage-force``), ctags
determinara la naturaleza de los ficheros utilizando las extensiones
habituales de cada lenguaje. Así, ``.py`` se entiende como Python,
``cpp`` como C++, ``bas`` como Basic, etc.

El mapa entre extensiones y lenguajes se puede consultar con la opción
de línea de comandos ``list-maps``:

.. code:: shell

$ ctags --list-maps
Ant      *.build.xml
Asm      *.asm *.ASM *.s *.S *.A51 *.29[kK] *.[68][68][kKsSxX] *.[xX][68][68]
Asp      *.asp *.asa
Awk      *.awk *.gawk *.mawk
Basic    *.bas *.bi *.bb *.pb
BETA     *.bet
C        *.c
C++      *.c++ *.cc *.cp *.cpp *.cxx *.h *.h++ *.hh *.hp *.hpp *.hxx *.C *.H
C#       *.cs
Cobol    *.cbl *.cob *.CBL *.COB
DosBatch *.bat *.cmd
Eiffel   *.e
Erlang   *.erl *.ERL *.hrl *.HRL
Flex     *.as *.mxml
Fortran  *.f *.for *.ftn *.f77 *.f90 *.f95 *.F *.FOR *.FTN *.F77 *.F90 *.F95
Go       *.go
HTML     *.htm *.html
Java     *.java
JavaScript *.js
Lisp     *.cl *.clisp *.el *.l *.lisp *.lsp
Lua      *.lua
Make     *.mak *.mk [Mm]akefile GNUmakefile
MatLab   *.m
ObjectiveC *.m *.h
OCaml    *.ml *.mli
Pascal   *.p *.pas
Perl     *.pl *.pm *.plx *.perl
PHP      *.php *.php3 *.phtml
Python   *.py *.pyx *.pxd *.pxi *.scons
REXX     *.cmd *.rexx *.rx
Ruby     *.rb *.ruby
Scheme   *.SCM *.SM *.sch *.scheme *.scm *.sm
Sh       *.sh *.SH *.bsh *.bash *.ksh *.zsh
SLang    *.sl
SML      *.sml *.sig
SQL      *.sql
Tcl      *.tcl *.tk *.wish *.itcl
Tex      *.tex
Vera     *.vr *.vri *.vrh
Verilog  *.v
VHDL     *.vhdl *.vhd
Vim      *.vim
YACC     *.y
