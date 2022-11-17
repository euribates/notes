--- 
title: Notas sobre find
---


## Find all files modifies on the last 24 hours

TLDR: `find . -mtime 0`

We can use the `-mtime` option to tell apart files or directories based
on modification time. It needs a numeric argument `n`, in the format
`[+|-]n`: `+n` is used to get results **greater than** n; `-n` to
get result **lesser than** n; and `n` for the exact value. From
the `find` man page:

```
    -atime n
         File  was  last  accessed n*24 hours ago.  When
         find figures out how many 24-hour periods ago
         the file  was  last  accessed,  any fractional
         part is ignored, so to match -atime +1, a file
         has to have been accessed at least two days ago.
```

This example search in my personal folder files (not directories,
because of `-t` option) modified in the last seven days:

```bash
find $HOME -type f -mtime -7
```

This gives the opposite: files modified more than 7 days ago:

```bash
find $HOME -type f -mtime +7
```

If we use the exact option, for example `-mtime 6`, it means *modified 6
days ago*. For example, if today is 23 April, 2021, and we use:

```bash
find $HOME -mtime 6
```

The find command will look for files with a modification time greater or
equal to `2021-04-17T00:00:00` and strictly less than
`2021-04-18T00:00:00`. This means we can find files modified today using
a value of 0:

```bash
find $HOME -mtime 0
```

Source: [Listar los archivos modificados en las últimas 24
horas](https://www.linuxito.com/gnu-linux/nivel-alto/400-listar-los-archivos-modificados-en-las-ultimas-24-horas)
