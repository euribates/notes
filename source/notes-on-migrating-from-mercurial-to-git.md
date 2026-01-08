---
title: Notas sobre miugrar desde mercurial a Git
tags:
    - development
    - git
    - mercurial
    - development
---

## Cómo migrar desde Mercurial a Git

Add to the system paython the hg-git extensions:

    pip install hg-git

And add it in the global mercurial config in `~/.hgrc`. The `extensions` part
must show something like this:

    [extensions]
    hgext.bookmarks =
    hggit = 


Clone the mercurial repo to migrate

    hg clone 

Create a bare git repo to convert into


Convert Mercurial project to Git - from bitbucket to gitlab

This post describe the steps for converting hg (mercurial) repository (on bitbucket) to git repository with all history.

    cd ~
    Clone your Mercurial repository you want to convert
    Clone the convert tool : git clone https://github.com/frej/fast-export.git
    git init new-git-repo
    cd new_git_rep
    Run the convert tool: ~/fast-export/hg-fast-export.sh -r /path/to/old/mercurial-repo
    git checkout HEAD
    In gitlab create new project which will contain the new-git-repo
    Add the remote which you just created step before and push:
        git remote add origin url-to-new-repo-in-gitlab
        git push -u origin -–all
        git push -u origin –-tags



git remote add origin git@bitbucket.org:euribates/expobot-git.git

