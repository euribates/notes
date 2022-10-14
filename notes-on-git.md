---
title: Notes on Git / GitHub
---

### How to learn GIT

- [Learn Git brnaching](https://learngitbranching.js.org/)

- [Julia Evans: Oh shit, git!](https://wizardzines.com/zines/oh-shit-git/)

- [CISCO: Introduction to Version Control – Git and GitHub](https://learningnetwork.cisco.com/s/article/introduction-to-version-control-git-and-github)

- [OH my git! An open source game about learning Git!](https://ohmygit.org/)


### How to Configure Git to handle line endings

Every time you press return on your keyboard you insert an invisible
character called a line ending. Different operating systems handle line
endings differently. When you're collaborating on projects with Git and
GitHub, Git might produce unexpected results if, for example, you're
working on a Windows machine, and your collaborator has made a change in
OS X.

You can configure Git to handle line endings automatically so you can
collaborate effectively with people who use different operating systems.

The `git config core.autocrlf` command is used to change how Git handles
line endings. It takes a single argument.

On Linux, you simply pass `input` to the configuration. For example:

```shell
$ git config --global core.autocrlf input
# Configure Git to ensure line endings in files you checkout are correct for Linux
```

!!! warning

    **Refreshing a repository after changing line endings**

    When you set the `core.autocrlf` option or commit a `.gitattributes`
    file, you may find that Git reports changes to files that you have not
    modified. Git has changed line endings to match your new configuration.

    To ensure that all the line endings in your repository match your new
    configuration, backup your files with Git, delete all files in your
    repository (except the .git directory), then restore the files all at
    once.


- Source: [Configurinf git to handle line encodings](https://docs.github.com/en/github/using-git/configuring-git-to-handle-line-endings)


### How to show differences

- `git diff` shows unstaged changes.

- `git diff --cached` shows staged changes.

- `git diff HEAD` shows all changes (both staged and unstaged).


### Hot to draw a clear log graph, showing branchs

This is the way:

```shell
git log --oneline --all --graph --decorate=full
```

- Source: [Git branch name - case sensitive or insensitive?](https://stackoverflow.com/questions/38493543/git-branch-name-case-sensitive-or-insensitive)

### Delete a local and a remote GIT branch

To delete a remote branch you can use the following command:

```shell
git push <remote_name> --delete <branch_name>
```

To delete the local GIT branch we can try one of the following commands:

```shell
git branch -d branch_name
```

Using `-d` only will delete the branch if there are no reference to a
remote, so delete the remote first.

If you just want to delete the local branch but still maintain the
branch in source, use `-D` instead.

### Special Files (mark some files as binary files)

You may need to mark certain files as binary files so that git knows to
ignore them and **doesn't produce lengthy diffs**. Git has a
`.gitattributes` file for just this purpose. In a _Javascript_ project,
you may want to add your `yarn-lock.json` or `package-lock.json` so that
Git doesn't try to diff them every time you make a change.

### Checkout by date (Get code as it was in a point of time)

You can checkout a commit by a specific date using `rev-parse` like
this:

```shell
git checkout 'master@{1979-02-26 18:30:00}'
```

More details on the available options can be found in the
[git-rev-parse](http://linux.die.net/man/1/git-rev-parse/) page.

As noted in the comments this method uses the reflog to find the commit
in your history. By default **these entries expire after 90 days**.
Although the syntax for using the reflog is less verbose you can only go
back 90 days.

### Checkout out by date using rev-list

The other option, which doesn't use the reflog, is to use `rev-list` to
get the commit at a particular point in time with:

```shell
git checkout `git rev-list -n 1 --first-parent --before="2009-07-27 13:37" master`
```

Note the `--first-parent` if you want only your history and not versions
brought in by a merge. That's what you usually want.

### How to get a list of the deleted files

This is the way:

```shell
git log --diff-filter=D --summary | grep delete
```

If you are looking for a particular file:

```shell
git log --diff-filter=D --summary | grep delete | grep <filename>
```

### How to find a deleted file in the project commit history

If you do not know the exact path you may use:

```shell
git log --all --full-history -- **/thefile.*
```

If you know the path the file was at, you can do this:

```shell
git log --all --full-history -- <path-to-file>
```

This should show a list of commits in all branches which touched that
file. Then, you can find the version of the file you want, and display
it with:

```shell
git show <SHA> -- <path-to-file>
```

Or restore it into your working copy with:

```shell
git checkout <SHA>^ -- <path-to-file>
```

!!! warning

    **Note the caret symbol (\^)**, which gets the checkout **prior to the one
    identified**, because at the moment of commit the file is deleted, we need
    to look at the previous commit to get the deleted file's contents.

### Make Git branch command do NOT behaves like 'less' (Do not paginate results)

This is a default behavior change introduced in Git 2.16.

You can turn paged output for git branch back off by default with the
`pager.branch` `config` setting:

```shell
git config --global pager.branch false
```

### Cómo revisar de forma interactiva los cambios antes de ser confirmados 

COn el comando `git add -p` podemos revisar los cambios producidos antes de cada
fichero, y aprovar o no la incorporación de los mismos al _commit_ actual.


### Some useful commands

- `git commit -a` Stages files automatically.

- `git log -p` Produces patch text.

- `git show` Shows various objects.

- `git diff` Is similar to the Linux `diff` command, and can show the
  differences in various commits.

- `git diff --staged` An alias to --cached, this will show all staged
  files compared to the named commit.

- `git mv` Similar to the Linux `mv` command, this moves a file.

- `git rm` Similar to the Linux `rm` command, this deletes, or removes
  a file.

- `git remote` Lists remote repos.

- `git remote -v` List remote repos verbously.

- `git remote show <name>` Describes a single remote repo.

- `git remote update` Fetches the most up-to-date objects.

- `git fetch` Downloads specific objects.

- `git branch -r` Lists remote branches; can be combined with other
  branch arguments to manage remote branches

### How to rename a branch in Git

If you have named a branch incorrectly **AND** pushed this to the remote
repository, follow these steps before any other developers get a chance to jump
on you and give you shit for not correctly following naming conventions.

#### Step 1. Rename your local branch.

If you are on the branch you want to rename:

```shell
git branch -m new-name
```

If you are on a different branch:

```shell
git branch -m old-name new-name
```

#### Step 2. Delete the old-name remote branch / push the new-name local branch

```shell
git push origin :old-name new-name
```

#### Step 3. Reset the upstream branch for the new-name local branch.

Switch to the branch and then:

```shell
git push origin -u new-name
```

Or you as a fast way to do that, you can use these 3 steps: command in
your terminal:

```shell
git branch -m old_branch new_branch         # Rename branch locally    
git push origin :old_branch                 # Delete the old branch    
git push --set-upstream origin new_branch   # Push the new branch, set local branch to track the new remote
```

### Get changes from master into branch in Git

You should be able to just git merge origin/master when you are on your
aq branch:

```shell
git checkout sandbox
git merge origin/develop
```

### List git branches that can safely be deleted

This is the way:

```shell
git checkout master # or whatever branch you might compare against
git branch --no-merged
git branch --merged
```

From git branch documentation:

> With `--merged`, only branches merged into the named commit (i.e. the
> branches whose tip commits are reachable from the named commit) will
> be listed. With `--no-merged`, only branches not merged into the named
> commit will be listed. If the argument is missing it defaults to HEAD
> (i.e. the tip of the current branch).

### Stashing

Often, when you've been working on part of your project, things are in a
messy state and you want to switch branches for a bit to work on
something else. The problem is, you don't want to do a commit of
half-done work just so you can get back to this point later. The answer
to this issue is the git stash command.

Stashing takes the dirty state of your working directory -that is, your
modified tracked files and staged changes- and saves it on a stack of
unfinished changes that you can reapply at any time.

### Forget the local changes and get the last repository version of file

It depends if you have made commit or not:

**Unstaged local changes (before you commit)**

When a change is made, but it is not added to the staged tree, Git
itself proposes a solution to discard changes to certain file.

Suppose you edited a file to change the content using your favorite
editor: Since you did not `git add <file>` to staging, it should be
under unstaged files (or untracked if file was created). You can confirm
that with:

```shell
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes not staged for commit:
(use "git add <file>..." to update what will be committed)
(use "git checkout -- <file>..." to discard changes in working directory)

modified:   <file>
no changes added to commit (use "git add" and/or "git commit -a")
```

At this point there are 3 options to undo the local changes you have:

**Discard all local changes, but save them** for possible re-use later:

```shell
git stash
```

**Discarding local changes (permanently) to a file**:

```shell
git checkout -- <filename
```

**Discard all local changes to all files permanently**:

```shell
git reset --hard
```

Before executing `git reset --hard`, keep in mind that there is also a
way to just temporary store the changes without committing them using
`git stash`. This command resets the changes to all files, but it also
saves them in case you would like to apply them at some later time.

### Make git diff with previous version of a file

This is the way:

```shell
git diff HEAD@{1} <filename>
```

The `@{1}` means \"the previous position of the ref I've specified\", so
that evaluates to what you had checked out previously - just before the
pull. You can tack `HEAD` on the end there if you also have some changes
in your work tree and you don't want to see the diffs for them.

!!! warning

    There are all kinds of wonderful ways to specify commits

    See the [specifying
    revisions](http://www.kernel.org/pub/software/scm/git/docs/git-rev-parse.html#_specifying_revisions)
    section of `man git-rev-parse` for more details.

- Source: [StackOverflow - git: How to diff changed files versus previous
  versions after a pull?]https://stackoverflow.com/questions/2428270/git-how-to-diff-changed-files-versus-previous-versions-after-a-pull)

### How to delete branches in Git

- Deleting local branches in Git:

    ```shell
    git branch -d feature/login
    ```

    Using the `-d` flag, you tell \"git branch\" which item you want to
    delete. Note that you might also need the `-f` flag if you're trying
    to delete a branch that contains unmerged changes. Use this option
    with care because it makes losing data very easy.

-   Deleting remote branches in Git:

    To delete a remote branch, we do not use the `git branch` command
    -but instead `git push` with the `--delete` flag:

    ```shell
        git push origin –delete feature/login
    ```

### To learn more about code review

- [GitHub style guide](http://google.github.io/styleguide/)
- [About Pull Request
  Reviews](https://help.github.com/en/articles/about-pull-request-reviews)
- [The perfect code review
  process](https://medium.com/osedea/the-perfect-code-review-process-845e6ba5c31)
- [What is code
  review](https://smartbear.com/learn/code-review/what-is-code-review/)
- <https://arp242.net/diy.html>
- <https://help.github.com/en/articles/closing-issues-using-keywords>
- <https://help.github.com/en/articles/setting-guidelines-for-repository-contributors>

### To learn about CI/CD

Check out the following links for more information:

- <https://www.infoworld.com/article/3271126/what-is-cicd-continuous-integration-and-continuous-delivery-explained.html>
- <https://stackify.com/what-is-cicd-whats-important-and-how-to-get-it-right/>
- <https://docs.travis-ci.com/user/tutorial/>
- <https://docs.travis-ci.com/user/build-stages/>

### Working with tags

Like most VCSs, Git has the ability to tag specific points in a
repository's history as being important. Typically, people use this
functionality to mark release points (`v1.0`, `v2.0` and so on).

Listing the existing tags in Git is straightforward. Just type `git tag`
(with optional `-l` or `--list`):

```shell
$ git tag
v1.0
v2.0
```

This command lists the tags in alphabetical order; the order in which
they are displayed has no real importance. You can also search for tags
that match a particular pattern. The Git source repo, for instance,
contains more than 500 tags. If you're interested only in looking at the
1.8.5 series, you can run this:

```shell
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
```

!!! warning

    Listing tag wildcards requires `-l` or `--list` option

    If you want just the entire list of tags, running the command git tag
    implicitly assumes you want a listing and provides one; the use of `-l` or
    `--list` in this case is optional.

    If, however, you're supplying a wildcard pattern to match tag names, the
    use of `-l` or `--list is mandatory`.  :::

#### Creating Tags

Git supports two types of tags: **lightweight** and **annotated**.

A lightweight tag is very much like a branch that doesn't
change --- it's just a pointer to a specific commit.

**Annotated tags**

Annotated tags, however, are stored as **full objects** in the Git
database. They're checksummed; contain the tagger name, email, and date;
have a tagging message; and can be signed and verified with GNU Privacy
Guard (GPG). It's generally recommended that you create annotated tags
so you can have all this information; but if you want a temporary tag or
for some reason don't want to keep the other information, lightweight
tags are available too.

Creating an annotated tag in Git is simple. The easiest way is to
specify `-a` when you run the tag command:

```shell
$ git tag -a v1.4 -m "my version 1.4"
$ git tag
v0.1
v1.3
v1.4
```

The `-m` specifies a tagging message, which is stored with the tag. If
you don't specify a message for an annotated tag, Git launches your
editor so you can type it in.

You can see the tag data along with the commit that was tagged by using
the git show command:

```shell
$ git show v1.4
tag v1.4
Tagger: Ben Straub <ben@straub.cc>
Date:   Sat May 3 20:19:12 2014 -0700

my version 1.4

commit ca82a6dff817ec66f44342007202690a93763949
Author: Scott Chacon <schacon@gee-mail.com>
Date:   Mon Mar 17 21:52:11 2008 -0700

Change version number
```

That shows the tagger information, the date the commit was tagged, and
the annotation message before showing the commit information.

**Lightweigh tags**

Another way to tag commits is with a lightweight tag. This is basically
the commit checksum stored in a file --- no other information is kept.
To create a lightweight tag, don't supply any of the -a, -s, or -m
options, just provide a tag name:

```shell
$ git tag v1.4-lw
$ git tag
v0.1
v1.3
v1.4
v1.4-lw
v1.5
```

This time, if you run `git show` on the tag, you don't see the extra tag
information. The command just shows the commit:

```shell
$ git show v1.4-lw
commit ca82a6dff817ec66f44342007202690a93763949
Author: Scott Chacon <schacon@gee-mail.com>
Date:   Mon Mar 17 21:52:11 2008 -0700

    Change version number
```

By default, the git push command **doesn't transfer tags to remote
servers**. You will have to explicitly push tags to a shared server
after you have created them. This process is just like sharing remote
branches --- you can run `git push origin <tagname>`:

```shell
$ git push origin v1.5
Counting objects: 14, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (12/12), done.
Writing objects: 100% (14/14), 2.05 KiB | 0 bytes/s, done.
Total 14 (delta 3), reused 0 (delta 0)
To git@github.com:schacon/simplegit.git
* [new tag]         v1.5 -> v1.5
```

To delete a tag on your local repository, you can use
`git tag -d <tagname>`. For example, we could remove our lightweight tag
above as follows:

```shell
$ git tag -d v1.4-lw
Deleted tag 'v1.4-lw' (was e7d5add)
```

Note that this **does not remove the tag from any remote servers**.
There are two common variations for deleting a tag from a remote server.

The first variation is `git push <remote> :refs/tags/<tagname>`:

```shell
$ git push origin :refs/tags/v1.4-lw
To /git@github.com:schacon/simplegit.git
- [deleted]         v1.4-lw
```

The way to interpret the above is to read it as the null value before
the colon is being pushed to the remote tag name, effectively deleting
it.

The second (and more intuitive) way to delete a remote tag is with:

```shell
$ git push origin --delete <tagname>
```

Source: [Git Basics - Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)


### Resources and more information

- [Pro Git](https://git-scm.com/book/en/v2): This book (available
  online and in print) covers all the fundamentals of how Git works
  and how to use it. Refer to it if you want to learn more about the
  subjects that we cover throughout the course.

- [Git tutorial](https://git-scm.com/docs/gittutorial): This tutorial
  includes a very brief reference of all Git commands available. You
  can use it to quickly review the commands that you need to use.

- [Five useful tips for a better commit message](https://robots.thoughtbot.com/5-useful-tips-for-a-better-commit-message):
  5 Useful Tips For A Better Commit Message.
