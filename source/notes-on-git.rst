git
========================================================================


Cómo aprender Git. Recursos e información adicional
---------------------------------------------------

-  `Learn Git branching <https://learngitbranching.js.org/>`__

-  `Julia Evans: Oh shit,
git! <https://wizardzines.com/zines/oh-shit-git/>`__

-  `CISCO: Introduction to Version Control – Git and
GitHub <https://learningnetwork.cisco.com/s/article/introduction-to-version-control-git-and-github>`__

-  `OH my git! An open source game about learning
Git! <https://ohmygit.org/>`__

-  `Pro Git <https://git-scm.com/book/en/v2>`__: This book (available
online and in print) covers all the fundamentals of how Git works and
how to use it. Refer to it if you want to learn more about the
subjects that we cover throughout the course.

-  `Git tutorial <https://git-scm.com/docs/gittutorial>`__: This
tutorial includes a very brief reference of all Git commands
available. You can use it to quickly review the commands that you
need to use.

-  `Five useful tips for a better commit
message <https://robots.thoughtbot.com/5-useful-tips-for-a-better-commit-message>`__:
5 Useful Tips For A Better Commit Message.

Cómo actualizar una rama, tanto en local como en remoto
-------------------------------------------------------

Para actualizar una etiqueta en el repositorio local, primero tenemos
que localizar el nuevo *commit* al que queremos que apunte. Para esto es
muy útil el comando ``git log --oneline`` que mostrará el *hash code* de
cada *commit* y las etiquetas que hubiera.

Cuando hayamos localizado el *commit*, haremos:

.. code:: shell

git tag -f <tag_name_to_update> <hash_code_new_commit>

Para actualizar la rama remota:

.. code:: shell

git push origin <tag> -f

La opción ``-f`` fuerza a redefinir el *tag* en el origin, si ya
estuviera definido.

Fuente: `Toolsqs - Git Delete Tag and Git Update
Tag <https://www.toolsqa.com/git/git-delete-tag/>`__

How to Configure Git to handle line endings
-------------------------------------------

Every time you press return on your keyboard you insert an invisible
character called a line ending. Different operating systems handle line
endings differently. When you’re collaborating on projects with Git and
GitHub, Git might produce unexpected results if, for example, you’re
working on a Windows machine, and your collaborator has made a change in
OS X.

You can configure Git to handle line endings automatically so you can
collaborate effectively with people who use different operating systems.

The ``git config core.autocrlf`` command is used to change how Git
handles line endings. It takes a single argument.

On Linux, you simply pass ``input`` to the configuration. For example:

.. code:: shell

$ git config --global core.autocrlf input
# Configure Git to ensure line endings in files you checkout are correct for Linux

!!! warning

::

**Refreshing a repository after changing line endings**

When you set the `core.autocrlf` option or commit a `.gitattributes`
file, you may find that Git reports changes to files that you have not
modified. Git has changed line endings to match your new configuration.

To ensure that all the line endings in your repository match your new
configuration, backup your files with Git, delete all files in your
repository (except the .git directory), then restore the files all at
once.

-  Source: `Configurinf git to handle line
encodings <https://docs.github.com/en/github/using-git/configuring-git-to-handle-line-endings>`__

Cómo mostrar diferencias entre ficheros locales, el repo o el *stage*
---------------------------------------------------------------------

-  ``git diff`` muestra las diferencias entre los ficheros locales y lo
que haya en el *stage*.

-  ``git diff --cached`` muestra las diferencias entres los ficheros en
el *stage* y la versión previa en el repositorio.

-  ``git diff HEAD`` muestra todas las diferencias, tanto de ficheros
modificados como de ficheros en el *stage*.

Cómo mostrar una versión gráfica del log que visualize las ramas
----------------------------------------------------------------

Este es el camino:

.. code:: shell

git log --oneline --all --graph --decorate=full

-  Fuente: `Git branch name - case sensitive or
insensitive? <https://stackoverflow.com/questions/38493543/git-branch-name-case-sensitive-or-insensitive>`__

Special Files (mark some files as binary files)
-----------------------------------------------

You may need to mark certain files as binary files so that git knows to
ignore them and **doesn’t produce lengthy diffs**. Git has a
``.gitattributes`` file for just this purpose. In a *Javascript*
project, you may want to add your ``yarn-lock.json`` or
``package-lock.json`` so that Git doesn’t try to diff them every time
you make a change.

Obtener una versión del histórico basándose en la fecha:
--------------------------------------------------------

Hay dos métodos:

Checkout por fecha usando *reflog*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se puede hacer un *checkout* a un *commit* específico en un momento
determinado usando este formato, usando ``rev_parse``:

.. code:: shell

git checkout 'master@{2021-02-26 13:37:00}'

Más detalles en
`git-rev-parse <http://linux.die.net/man/1/git-rev-parse/>`__.

!!! Solo para cambios enteriores a 90 días

::

Esta operación usa el método _reflog_ para encontrar el commit que cumpla
la condicion en la historia local del repositorio. Pero por defecto estas
entradas caducan a los **90 días**, asi que está técnica solo puede
retroceder ese tiempo.

Checkout por fecha usando *rev-list*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La otra opción, que no usa *reflog* y por tanto no tiene la limitación
de los 90 días, es ``rev-list``, que es un poco más prolija:

.. code:: shell

git checkout `git rev-list -n 1 --first-parent --before="2021-02-26 13:37" master`

Atención al flag ``--first-parent``, que trabajara solo con tu historial
sin prestar atención a otras versiones incorporadas por ``merge``; esto
es normalmente lo que se quiere.

Cómo obtener un listado de ficheros borrados
--------------------------------------------

Este es el camino:

.. code:: shell

git log --diff-filter=D --summary | grep delete

Si estás buscando un fichero en concreto:

.. code:: shell

git log --diff-filter=D --summary | grep delete | grep <filename>

How to find a deleted file in the project commit history
--------------------------------------------------------

If you do not know the exact path you may use:

.. code:: shell

git log --all --full-history -- **/thefile.*

If you know the path the file was at, you can do this:

.. code:: shell

git log --all --full-history -- <path-to-file>

This should show a list of commits in all branches which touched that
file. Then, you can find the version of the file you want, and display
it with:

.. code:: shell

git show <SHA> -- <path-to-file>

Or restore it into your working copy with:

.. code:: shell

git checkout <SHA>^ -- <path-to-file>

!!! warning

::

**Note the caret symbol (\^)**, which gets the checkout **prior to the one
identified**, because at the moment of commit the file is deleted, we need
to look at the previous commit to get the deleted file's contents.

Make Git branch command do NOT behaves like ‘less’ (Do not paginate results)
----------------------------------------------------------------------------

This is a default behavior change introduced in Git 2.16.

You can turn paged output for git branch back off by default with the
``pager.branch`` ``config`` setting:

.. code:: shell

git config --global pager.branch false

Cómo revisar de forma interactiva los cambios antes de ser confirmados
----------------------------------------------------------------------

Con el comando ``git add -p`` podemos revisar los cambios producidos
antes de cada fichero, y aprobar o no la incorporación de los mismos al
*commit* actual.

Algunos comandos git útiles
---------------------------

-  ``git commit -a`` Stages files automatically.

-  ``git log -p`` Produces patch text.

-  ``git show`` Shows various objects.

-  ``git diff`` Is similar to the Linux ``diff`` command, and can show
the differences in various commits.

-  ``git diff --staged`` An alias to –cached, this will show all staged
files compared to the named commit.

-  ``git mv`` Similar to the Linux ``mv`` command, this moves a file.

-  ``git rm`` Similar to the Linux ``rm`` command, this deletes, or
removes a file.

-  ``git remote`` lista los repositorios remotos

-  ``git remote -v`` lista los repositorios remotos con información
adicional

-  ``git remote show <name>`` Describes a single remote repo.

-  ``git remote update`` Fetches the most up-to-date objects.

-  ``git fetch`` Downloads specific objects.

-  ``git branch -r`` Lists remote branches; can be combined with other
branch arguments to manage remote branches

Cómo renombrar una rama en Git
------------------------------

If you have named a branch incorrectly **AND** pushed this to the remote
repository, follow these steps before any other developers get a chance
to jump on you and give you shit for not correctly following naming
conventions.

Step 1. Rename your local branch.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are on the branch you want to rename:

.. code:: shell

git branch -m new-name

If you are on a different branch:

.. code:: shell

git branch -m old-name new-name

Step 2. Delete the old-name remote branch / push the new-name local branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: shell

git push origin :old-name new-name

Step 3. Reset the upstream branch for the new-name local branch.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Switch to the branch and then:

.. code:: shell

git push origin -u new-name

Or you as a fast way to do that, you can use these 3 steps: command in
your terminal:

.. code:: shell

git branch -m old_branch new_branch         # Rename branch locally
git push origin :old_branch                 # Delete the old branch
git push --set-upstream origin new_branch   # Push the new branch, set local branch to track the new remote

Cómo incorporar cambios realizados en otra rama (Por ejemplo, ``master`` a ``dev``)
-----------------------------------------------------------------------------------

La forma más sencilla es cambiarse a la rama de destino y realizar un
merge con la rama que tiene los cambios que queremos incorporar:

.. code:: shell

git switch develop
git merge origin/master

Cómo listar las ramas que se pueden borrar de forma segura
----------------------------------------------------------

Este es el camino:

.. code:: shell

git checkout master # or whatever branch you might compare against
git branch --no-merged
git branch --merged

De la documentaión de Git sobre ramas:

With ``--merged``, only branches merged into the named commit
(i.e. the branches whose tip commits are reachable from the named
commit) will be listed. With ``--no-merged``, only branches not
merged into the named commit will be listed. If the argument is
missing it defaults to HEAD (i.e. the tip of the current branch).

Stashing
--------

Often, when you’ve been working on part of your project, things are in a
messy state and you want to switch branches for a bit to work on
something else. The problem is, you don’t want to do a commit of
half-done work just so you can get back to this point later. The answer
to this issue is the git stash command.

Stashing takes the dirty state of your working directory -that is, your
modified tracked files and staged changes- and saves it on a stack of
unfinished changes that you can reapply at any time.

Forget the local changes and get the last repository version of file
--------------------------------------------------------------------

It depends if you have made commit or not:

**Unstaged local changes (before you commit)**

When a change is made, but it is not added to the staged tree, Git
itself proposes a solution to discard changes to certain file.

Suppose you edited a file to change the content using your favorite
editor: Since you did not ``git add <file>`` to staging, it should be
under unstaged files (or untracked if file was created). You can confirm
that with:

.. code:: shell

$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes not staged for commit:
(use "git add <file>..." to update what will be committed)
(use "git checkout -- <file>..." to discard changes in working directory)

modified:   <file>
no changes added to commit (use "git add" and/or "git commit -a")

At this point there are 3 options to undo the local changes you have:

**Discard all local changes, but save them** for possible re-use later:

.. code:: shell

git stash

**Discarding local changes (permanently) to a file**:

.. code:: shell

git checkout -- <filename

**Discard all local changes to all files permanently**:

.. code:: shell

git reset --hard

Before executing ``git reset --hard``, keep in mind that there is also a
way to just temporary store the changes without committing them using
``git stash``. This command resets the changes to all files, but it also
saves them in case you would like to apply them at some later time.

Make git diff with previous version of a file
---------------------------------------------

This is the way:

.. code:: shell

git diff HEAD@{1} <filename>

The ``@{1}`` means "the previous position of the ref I’ve specified", so
that evaluates to what you had checked out previously - just before the
pull. You can tack ``HEAD`` on the end there if you also have some
changes in your work tree and you don’t want to see the diffs for them.

!!! warning

::

There are all kinds of wonderful ways to specify commits

See the [specifying
revisions](http://www.kernel.org/pub/software/scm/git/docs/git-rev-parse.html#_specifying_revisions)
section of `man git-rev-parse` for more details.

-  Source: [StackOverflow - git: How to diff changed files versus
previous versions after a
pull?]https://stackoverflow.com/questions/2428270/git-how-to-diff-changed-files-versus-previous-versions-after-a-pull)

Cómo borrar ramas en Git
------------------------

Cómo borrar una rama local
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: shell

git branch -d pruebas

Con el indicador ``-d`` indicamos el nombre de la rama a borrar. Si la
rama tuviera ficheros modificas no nos dejará borrarla, a no ser que lo
forzemos con el indicador ``-f``. Onbiamente esto hay que hacerlo con
cuidado porque implica la posibilidad de perder información.

Tampoco nos dejará borrarla si existe referencias a ella, por lo que si
la rama también existe en el remoto, es recomendable borrarla primero en
el remoto y luego borrar la local con ``-d``. Si por lo que fuera se
quiere mantener la rama remota pero borrar la local, se puede hacer
usando el flag ``-D``.

Cómo borrar una rama remota
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para borrar una rama remota se usa el comando *push* con el indicador
``--delete``:

.. code:: shell

git push origin –delete pruebas

To learn more about code review
-------------------------------

-  `GitHub style guide <http://google.github.io/styleguide/>`__
-  `About Pull Request
Reviews <https://help.github.com/en/articles/about-pull-request-reviews>`__
-  `The perfect code review
process <https://medium.com/osedea/the-perfect-code-review-process-845e6ba5c31>`__
-  `What is code
review <https://smartbear.com/learn/code-review/what-is-code-review/>`__
-  https://arp242.net/diy.html
-  https://help.github.com/en/articles/closing-issues-using-keywords
-  https://help.github.com/en/articles/setting-guidelines-for-repository-contributors

How to learn about CI/CD
------------------------

Check out the following links for more information:

-  https://www.infoworld.com/article/3271126/what-is-cicd-continuous-integration-and-continuous-delivery-explained.html
-  https://stackify.com/what-is-cicd-whats-important-and-how-to-get-it-right/
-  https://docs.travis-ci.com/user/tutorial/
-  https://docs.travis-ci.com/user/build-stages/

Como usar las etiquetas en Git
------------------------------

Like most VCSs, Git has the ability to tag specific points in a
repository’s history as being important. Typically, people use this
functionality to mark release points (``v1.0``, ``v2.0`` and so on).

Listing the existing tags in Git is straightforward. Just type
``git tag`` (with optional ``-l`` or ``--list``):

.. code:: shell

$ git tag
v1.0
v2.0

This command lists the tags in alphabetical order; the order in which
they are displayed has no real importance. You can also search for tags
that match a particular pattern. The Git source repo, for instance,
contains more than 500 tags. If you’re interested only in looking at the
1.8.5 series, you can run this:

.. code:: shell

$ git tag -l "v1.8.5*"
v1.8.5
v1.8.5-rc0
v1.8.5-rc1
v1.8.5-rc2
v1.8.5-rc3
v1.8.5.1
v1.8.5.2
v1.8.5.3
v1.8.5.4
v1.8.5.5

!!! warning

::

Listing tag wildcards requires `-l` or `--list` option

If you want just the entire list of tags, running the command git tag
implicitly assumes you want a listing and provides one; the use of `-l` or
`--list` in this case is optional.

If, however, you're supplying a wildcard pattern to match tag names, the
use of `-l` or `--list is mandatory`.  :::

Cómo crear etiquetas en Git
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Git supports two types of tags: **lightweight** and **annotated**.

A lightweight tag is very much like a branch that doesn’t change — it’s
just a pointer to a specific commit.

**Annotated tags**

Annotated tags, however, are stored as **full objects** in the Git
database. They’re checksummed; contain the tagger name, email, and date;
have a tagging message; and can be signed and verified with GNU Privacy
Guard (GPG). It’s generally recommended that you create annotated tags
so you can have all this information; but if you want a temporary tag or
for some reason don’t want to keep the other information, lightweight
tags are available too.

Creating an annotated tag in Git is simple. The easiest way is to
specify ``-a`` when you run the tag command:

.. code:: shell

$ git tag -a v1.4 -m "my version 1.4"
$ git tag
v0.1
v1.3
v1.4

The ``-m`` specifies a tagging message, which is stored with the tag. If
you don’t specify a message for an annotated tag, Git launches your
editor so you can type it in.

You can see the tag data along with the commit that was tagged by using
the git show command:

.. code:: shell

$ git show v1.4
tag v1.4
Tagger: Menganito <menganito@invent-email.com>
Date:   Sat May 3 20:19:12 2014 -0700

my version 1.4

commit ca82a6dff817ec66f44342007202690a93763949
Author: Fulanito <fulanito@invent-email.com>
Date:   Mon Mar 17 21:52:11 2008 -0700

Change version number

That shows the tagger information, the date the commit was tagged, and
the annotation message before showing the commit information.

**Lightweigh tags**

Another way to tag commits is with a lightweight tag. This is basically
the commit checksum stored in a file — no other information is kept. To
create a lightweight tag, don’t supply any of the -a, -s, or -m options,
just provide a tag name:

.. code:: shell

$ git tag v1.4-lw
$ git tag
v0.1
v1.3
v1.4
v1.4-lw
v1.5

This time, if you run ``git show`` on the tag, you don’t see the extra
tag information. The command just shows the commit:

.. code:: shell

$ git show v1.4-lw
commit ca82a6dff817ec66f44342007202690a93763949
Author: Scott Chacon <schacon@gee-mail.com>
Date:   Mon Mar 17 21:52:11 2008 -0700

Change version number

By default, the git push command **doesn’t transfer tags to remote
servers**. You will have to explicitly push tags to a shared server
after you have created them. This process is just like sharing remote
branches — you can run ``git push origin <tagname>``:

.. code:: shell

$ git push origin v1.5
Counting objects: 14, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (12/12), done.
Writing objects: 100% (14/14), 2.05 KiB | 0 bytes/s, done.
Total 14 (delta 3), reused 0 (delta 0)
To git@github.com:schacon/simplegit.git
* [new tag]         v1.5 -> v1.5

To delete a tag on your local repository, you can use
``git tag -d <tagname>``. For example, we could remove our lightweight
tag above as follows:

.. code:: shell

$ git tag -d v1.4-lw
Deleted tag 'v1.4-lw' (was e7d5add)

Note that this **does not remove the tag from any remote servers**.
There are two common variations for deleting a tag from a remote server.

The first variation is ``git push <remote> :refs/tags/<tagname>``:

.. code:: shell

$ git push origin :refs/tags/v1.4-lw
To /git@github.com:schacon/simplegit.git
- [deleted]         v1.4-lw

The way to interpret the above is to read it as the null value before
the colon is being pushed to the remote tag name, effectively deleting
it.

No obstante, la forma más sencilla e intuitiva de borrar un *tag* remoto
es:

.. code:: shell

$ git push origin --delete <tagname>

Source: `Git Basics -
Tagging <https://git-scm.com/book/en/v2/Git-Basics-Tagging>`__

Ver un fichero tal y como está en otra rama
-------------------------------------------

Git puede mostrar la versión de un fichero que está en otra rama, sin
necesidad de cambiar a esa rama, usando el comando ``show``. Se le pasa
como parámetro el nonbre de la rama, dos puntos y la ruta del fichero:

.. code:: shell

git show main:src/program.py

También podemos especificar un *commit* o referencia, en vez del nombre
de la rama. El siguiente ejemplo muestra la versión del fichero en el
*commit* anterior:

.. code:: shell

git show HEAD~1:src/program.py

-  Fuente: `7 tips for improving your productivity with Git - DEV
Community <https://dev.to/dgenezini/7-tips-for-improving-your-productivity-with-git-ajg>`__

Cual es la diferencia entre un repositorio *bare* y otro normal
---------------------------------------------------------------

Cuando clonamos o creamos un proyecto, Git normalmente crea un
directorio de primer nivel para los ficheros del proyecto en si, y los
ficheros de administración del repositorio se ponen en otra carpeta,
dentro de la principal, normalmente llamada ``.git``. Tenemos tanto el
repositorio como el árbol de trabajo, es decir, una copia de todas las
carpetas y ficheros del proyecto.

Si creamos una repositorio *bare*, ya sea con ``git init --bare`` o
``git clone --bare``, el directorio que se crea es directamente el
directorio del repositorio, es decir, no se crea el directorio donde
normalmente se generan los ficheros del proyecto. Usar ``--bare``
incluye implícitamente la opción ``--no-checkout``, ya que no existe
directorio alguno donde desplegar el árbol de trabajo del proyecto.
Además, las ramas del repositorio remoto se crean como ramas locales
equivalentes, vinculadas directamente con las ramas remotas.

La distinción entre estos dos tipos de repositorios es un poco
inconsistente, y puede llevar a confusión, ya que el árbol de trabajo
del proyecto no tienen que incluir obligatoriamente el repositorio, y un
repositorio no tiene que incluir obligatoriamente una árbol de trabajo
de los ficheros del proyecto.

La variable de entorno ``$GIT_DIR`` enlaza el árbol de trabajo con el
repositorio que lo originó. Normalmente no tiene valor, y en este caso
Git busca en el directorio actual una carpeta llamada ``.git``. Si no lo
encuentra, va subiendo por el árbol de trabajo hasta que lo encuentre o
hasta que llegue al directorio ``$HOME`` del usuario. Sin embargo, en el
caso de usar un repositorio *bare*, lo más probable es que tengamos que
definir esta variable de entorno para indicar donde está el repositorio.

Fuentes:

-  `Git - git clone
documentation <https://git-scm.com/docs/git-clone>`__
-  `Stack Overflow - What’s the practical difference between a Bare and
non-Bare
repository? <https://stackoverflow.com/questions/5540883/whats-the-practical-difference-between-a-bare-and-non-bare-repository>`__

¿Cómo copio una versión de un fichero de una rama de git a otra?
----------------------------------------------------------------

Debes hacer:

.. code:: shell

git checkout mi_otra_rama fichero.txt

Donde ``mi_otra_rama`` es la rama de donde quieres traer el fichero
``fichero.txt``.

Otras posbilidades:

.. code:: shell

git checkout <commit_hash> <ruta_relativa_al_fichero_o_directorio>
git checkout <remote_name>/<branch_name> <fichero_o_directorio>

Algunas notas:

-  Usando el *commit_hash* puedes traer ficheros de cualquier commit.

-  Funciona tanto para ficheros como para directorios.

-  se sobrescribira el fichero fichero.txt.

-  No funcionan los wildcards, pero sí las rutas relativas.

-  Puedes indicar múltiples rutas.

Otra alternativa:

.. code:: shell

git show commit_id:path/to/file > path/to/file

Fuente: `Stack Overflow en
español <https://es.stackoverflow.com/questions/243064/cdocs/notes-on-git.mdC3docs/notes-on-git.mdB3mo-copio-una-versidocs/notes-on-git.mdC3docs/notes-on-git.mdB3n-de-un-fichero-de-una-rama-de-git-a-otra>`__

Cómo crear alias para los subcomandos de Git
--------------------------------------------

Usando ``git config`` podemos almacenar alias, en el ámbito que desemos.
Para definir en el ámbito blobal, usamos el *flag* ``--global``. Estos
son los álias que suelo usar:

.. code:: shell

git config --global alias.co checkout
git config --global alias.sw switch
git config --global alias.st status

Fuente: `Git - Git
Aliases <https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases>`__

Cómo retroceder HEAD a un *commit* anterior
-------------------------------------------

Antes que nada, ¿Qué es ``HEAD``? Es simplemente una referencia al
*commit* actual (es decir, el último) en la rama actual. Solo puede
haber **un ``HEAD``** en un momento dado (Excluyendo ``git worktree``).
El contenido de ``HEAD`` se almacena en ``.git/HEAD`` y consiste en los
40 bytes del *hash* del *commit*.

¿Que significa *detached HEAD*? Que ``HEAD`` no está apuntando al último
\_commit-, sino a uno anterior en la historia.

Si queremos configurar **a lo bruto** ``HEAD`` para que apunte a un
commit específico:

.. code:: shell

git reset --hard <hash>
