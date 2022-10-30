---
title: Notas sobre VS Code
---


## Introducción

**Vs Code** es un IDE multipropósito de Microsoft.


## Work with Python interpreters

By default, the Python extension looks for and uses the first Python
interpreter it finds in the system path. To select a specific environment, use
the Python: Select Interpreter command from the Command Palette
(++ctrl+shift+p++).

```
Python: Select Interpreter command
```

Sources:

- [Using Python Environments in Visual Studio Code](https://code.visualstudio.com/docs/python/environmentsDropbox/notes/notes-on-vscode.md_work-with-python-interpreters)

## Use VIM inside VSCode

Source: <https://www.barbarianmeetscoding.com/blog/2019/02/08/boost-your-coding-fu-with-vscode-and-vim>

### Install Vim extension

- Open Visual Studio Code
- Go to Extensions
- Type vim in the search box
- The first plugin named Vim is the one you want
- Click on the install button

Now after the extension is installed you may need to restart Visual Studio Code for the changes to
take effect. latest-vscode

Have you restarted it? Open a code file from your latest project and look at the cursor. Does it
look like a rectangle? Yes? Welcome to Vim

### How to Move Horizontally Word By Word

Word Motions allows you to move faster horizontally:

- Use `w` to jump from word to word (and `b` to do it backward)
- Use `e` to jump to the end of a word (and `ge` to do it backward)
- A word in Vim only includes letters, digits and numbers. If you want to consider special characters like `.,` (, {, etc as part of a word (called WORD in Vim jargon) you can use the capitalized equivalents of the keys above (`W`, `B`, `E`, `gE`)
- In general, word motions allow for more precise changes while WORD motions allow for faster movement.

### How to Move To A Specific Character

Find character motions allow you to move horizontally quickly and with high precision:

- Use `f{char}` to move (find) to the next occurrence of a character char in a line (and `F` to move
  backwards). For instance, `f"` sends you to the next occurrence of a double quote.

- Use `t{char}` to move the cursor just before (until) the next occurrence of a character char

- After using `f{char}` you can type `;` to go to the next occurrence or `,` to go to the previous
  one. You can see the `;` and `,` as commands for repeating the last character search.

### how to move horizontally extremely

To move extremely horizontally use:

- `0`: Moves to the first character of a line
- `^`: Moves to the first non-blank character of a line
- `$`: Moves to the end of a line
- `g_`: Moves to the non-blank character at the end of a line

### How to move vertically

Starting from `k` and `j`, we move on to a faster way of maneuvering vertically with:

- `}` jumps entire paragraphs downwards
- `{` similarly but upwards
- `CTRL-D` let’s you move down half a page
- `CTRL-U` let’s you move up half a page

### Hw to Moving Semantically

- Use `gd` to jump to definition of whatever is under your cursor

- Use `gf` to jump to a file in an import

### Editing Like Magic With Vim Operators

Motions aren’t just for moving. They can be used in combination with a series of commands called
operators to edit your code in Normal mode. These combos normally take this shape:

    an action to perform: delete, change, yank, etc
         /
        /
       /                  ____ a motion that represents a piece
      |                  /     of text to which to appy the action
      |                 /      defined by the operator
    {operator}{count}{motion}
                \
                 \
                  \
                   \_ a multiplier to "perform an action
                      {count} times"

One of such commands is delete triggered via the `d` key:

- `d5j` deletes 5 lines down
- `df'` deletes everything in the current line until the first occurrence of the ' character (including the character)
- `dt'` would do like above but excluding the character (so up until just before)
- `d/hello` deletes everything until the first occurrence of hello
- `ggdG` deletes a complete document

Other useful operators are:

- `c` change. This is the most useful operator. It deletes and sends you into insert mode so that you can type
- `y` yank or copy in Vim jargon
- `p` put or paste in Vim jargon
- `g~` to toggle caps

All these operators have some useful shorthand syntax aimed at saving you typing and increasing your
speed in common use cases:

- Double an operator to make it operate on a whole line: `dd` deletes a whole like, `cc` changes a whole line, etc.

- Capitalize an operator to make it operate from the cursor to the end of a line: `D` deletes from
  the cursor to the end of the line, `C` changes to the end of a line, etc.

### Editing Up a Notch With Text Objects

Text objects are structured pieces of text or, if you will, the entities of a document domain model.
What is a document composed of? Words, sentences, quoted text, paragraphs, blocks, (HTML) tags, etc.
These are text objects.

The way that you specify a text object within a command is by combining the letter `a` (which
represents the text object plus whitespace) or `i` (inner object without whitespace) with a
character that represents a text object itself: `w` for word, `s` for sentence, `'` `"` for quotes,
`p` for paragraph, `b` for block surrounded by `(`, `B` for block surrounded by `{` and `t` for tag.
So to delete different bits of text you could:

- `daw` to delete a word (plus trailing whitespace)
- `ciw` to change inner word
- `das` to delete a sentence (dis delete inner sentence)
- `da"` to delete something in double quotes including the quotes
- `ci"` to change something inside double quotes
- `dap` to delete a paragraph
- `dab` `da(` or `da)` to delete a block surrounded by (
- `daB` `da{` or `da}` to delete a block surrounded by {
- `dat` to delete an HTML tag
- `cit` to change the contents of an HTML tag

Combining text objects with operators is extremely powerful and you’ll use them very often. Stuff
like `cit`, `ci"` and `cib` is just brilliant.

Let’s say that we want to change the contents of this string below for something else:

    const salute = 'I salute you oh Mighty Warrior'

You type `ci'Hi!<ESC>` and it becomes:

    const salute = 'Hi!'

Just like that. You don’t need to go grab the mouse, select the text and then write something else.
You type three letters and Boom.

### Repeating The Last Change with The Dot Operator

Vim has yet another trick in store for you aimed at saving you more keystrokes: The magic `.`
command. This command allows you to repeat the last change you made. Imagine that you run `dd` to
delete a line. You could type `dd` again to delete another line but you could also use `.` which is
just a single keystroke. Ok, you save one keystroke, so what? Well, you can use the `.` command to
repeat any type of change, not just single commands. For instance, you could change a word for
“Awesome” like so `cawAwesome<CR>`, and then repeat that whole command with all those keystrokes by
just using `.`. Think of the possibilities!

The `.` command works great in combination with the repeat search commands (`;`, `,`, `n` or `N`).
Imagine that you want to delete all occurrences of *cucumber*. An alternative would be to search for
cucumber `/cucumber` then delete it with `daw`. From then on you can use `n` to go to the next match and `.`
to delete it! Two keystrokes!?! Again think of the possibilities!!

### Some handy Visual Studio Code only key mappings:

These are some handy mappings the VSCodeVim team came up with only for VSCode:

- `gb` adds another cursor on the next word it finds which is the same as the word under the cursor.
  Like `*`: but instead of jumping to next ocurrence it creates multiple cursors.

- `af` is a visual moe command that selects increasingly larger blocks of text.

- `gh` is the equivalent of hovering the mouse over where the cursor is. Super handy in order to
  enable a keyboard only workflow and still enjoy some features (error messages, types, etc) only
  available via the mouse.
