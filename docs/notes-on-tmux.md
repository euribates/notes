---
title: Notes on Tmux
---

## Sobre TMux

## How to rename sessions

Use the Key Combination: ++ctrl+b++ y `$`.

Source: 

## How to split, switch and resize panes

Here is a list of a few basic tmux commands:

- `Ctrl+b` : split pane horizontally.
- `Ctrl+b %` : split pane vertically.
- `Ctrl+b arrow key` : switch pane.
- Hold `Ctrl+b`, don’t release it and hold one of the arrow keys to **resize pane**.
- `Ctrl+b c` : (c)reate a new window.
- `Ctrl+b n` : move to the (n)ext window.
- `Ctrl+b p` : move to the (p)revious window.

Other thing worth knowing is that **scrolling is enabled** by pressing `Ctrl+b
PgUp/PgDown`. In fact, it enables the copy mode, which can also be done by
pressing `Ctrl+b [`. When in copy mode, you can use `PgUp/PgDown` and arrow keys to
scroll through the terminal contents. To (q)uit the copy mode, simply press the
`q` key.

Source: [tmux Tutorial — Split Terminal Windows Easily - Lukasz Wrobel](https://lukaszwrobel.pl/blog/tmux-tutorial-split-terminal-windows-easily/)

## How to create Tmux sessions

To create a new Tmux session and attach to it, run the following command
from the Terminal:

```shell
tmux
```

Or:

```shell
tmux new
```

Once you are inside the Tmux session, you will see **a green bar at the bottom**.

## How to recover a shell after a disconnection

There is no way, but to prevent this I like using tmux. I start tmux,
start the operation and go on my way. If I return and find the
connection has been broken, all I have to do is reconnect and type tmux
attach.

Here's an example:

```shell
$ tmux
$ make <something big>
......
Connection fails for some reason
Reconect

$ tmux ls
0: 1 windows (created Tue Aug 23 12:39:52 2011) [103x30]

$ tmux attach -t 0
Back in the tmux sesion
```

## How to create named sessions

If you use multiple sessions, you might get confused which programs are
running on which sessions. In such cases, you can just create named
sessions. For example if you wanted to perform some activities related
to web server in a session, just create the Tmux session with a custom
name, for example `webserver` (or any name of your choice):

```shell
tmux new -s webserver
```

## How to detach from Tmux sessions

To detach from a current Tmux session, just press ++ctrl+b++ and ++d++
(You don't need to press this both Keyboard shortcut at a time; first
press ++ctrl+b++ and then press ++d++).

Once you're detached from a session, you will see an output something
like below:

```shell
[detached (from session 0)]
```

## How to list Tmux sessions

To view the list of open Tmux sessions, run:

```shell
tmux ls
```

## How to attach to Tmux sessions

You can attach to the last created session by running this command:

```shell
tmux attach
```

Or:

```shell
tmux a
```

If you want to attach to any specific named session, for example
"webserver", run:

```shell
tmux attach -t webserver
```

Or, shortly:

```shell
tmux a -t sebserver
```

Sources:

- [Tmux Command Examples To Manage Multiple Terminal Sessions](https://ostechnix.com/tmux-command-examples-to-manage-multiple-terminal-sessions/)
