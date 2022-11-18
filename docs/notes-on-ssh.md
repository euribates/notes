---
title: Notas sobre SSH
tags:
  - unix
---

## Sobreo SSH

**SSH** (_Secure SHell_) es un protocolo y programa cuya principal función es el acceso remoto a un servidor por medio de un canal seguro en el que toda la información está cifrada.


## Use Your SSH Agent in a Crontab

Getting access to SSH inside a Crontab is often a problem for many as the environment in
which your cron runs **is not the same as your normal shell**. Simply running `ssh-add` will
not allow you to use your SSH Agent inside your crontab. Follow the below guide to setup
your crontab to use your ssh-agent:

1) Install Keychain.

2) Add the following to your `~/.zlogin` file which will be invoked on each login. This will
allow your crontab (and normal shell) to use your ssh keys and bypass needing to punch in
your password each time you need SSH. This will also span across multiple sessions and
shells.

```bash
# Use keychain to keep ssh-agent information available in a file
/usr/bin/keychain "$HOME/.ssh/id_rsa"
source "$HOME/.keychain/${HOSTNAME}-sh"
```

3) Finally, prepend the following to your cron job command to allow it access to your new
keychain:

```bash
source "$HOME/.keychain/${HOSTNAME}-sh"
```

Soorce: [Use Your SSH Agent in a Crontab](https://gist.github.com/Justintime50/297d0d36da40834b037a65998d2149ca)


## About ssh-agent and ssh-add in Unix

In Unix, **ssh-agent** is a background program that handles passwords for SSH
private keys. The ssh-add command prompts the user for a private key password
and adds it to the list maintained by ssh-agent. Once you add a password to
ssh-agent, you will not be prompted for it when using SSH or scp to connect to
hosts with your public key.

The public part of the key loaded into the agent must be put on the target
system in `~/.ssh/authorized_keys`; see Set up SSH public key authentication to
connect to a remote system.

To use `ssh-agent` and `ssh-add`, follow the steps below:

At the Unix prompt, enter:

```shell
eval `ssh-agent`
```

Make sure you use the backquote (`), located under the tilde (~), rather than the single quote (').

Enter the command:

```shell
ssh-add
```

Enter your private key password.
When you log out, enter the command:

```shell
kill $SSH_AGENT_PID
```

To run this command automatically when you log out, place it in your
`.logout` file (if you are using csh or tcsh) or your `.bash_logout` file
(if you are using bash).

Source: [Indiana University - About ssh-agent and ssh-add in Unix](https://kb.iu.edu/d/aeww)
