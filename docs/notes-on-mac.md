## Notes on MAC

### Apps utiles

- Itsycal: `brew cask install itsycal`


### How to enter directory paths when in open/save dialogs

While in an open/save dialog, pressing `Command` + `Shift` + `G ` will allow you to type in a
directory path.

For instance, if I wanted to open my Documents directory for my user, I would type
`~/Documents`. The tilde (`~`) tells the computer to look in the current user's home directory.

Fuente: <https://www.engadget.com/2008/12/30/mac-101-enter-directory-paths-when-in-open-save-dialogs>

### How to delete process

1) Use a Keyboard Shortcut for “Force Quit Applications” on Mac

  Starting with one of the best and easiest is the system wide Force Quit function: Hit
  Command+Option+Escape from anywhere to bring up the simple “Force Quit Applications” window

2) Force Quit Currently Active Mac App with the Keyboard

  Hold down Command+Option+Shift+Escape for a second or two until the app forcibly closes. Be sure
  to do this while the app you want to force quit is the foremost application on the Mac, as it
  will force quit whatever is active when held down.

3) Force Quit an App from the Apple Menu

  Hold the Shift Key and click on the  Apple menu to find “Force Quit [Application Name]

4) Use Activity Monitor to Force Quit Apps

  Activity Monitor is a powerful way to forcibly quit any app, task, daemon, or process running on
  Mac OS X. You can find it in `/Applications/Utilities/` or open it from Spotlight with
  Command+Space and then type `Activity Monitor`. 

6) Using the Terminal & kill Command

  If all else fails, using the command line is a surefire way to force an app or process to quit by
  issuing the low-level kill command. Launch the Terminal and type one of the following commands:

    killall [processname]

  For example, “killall Safari” would kill all instances of the Safari process. If you know the
  process id, which you can find with the `ps` or `ps aux` command. Aim kill at that process
  specifically:

    kill -9 [pid]

Source: <http://osxdaily.com/2012/03/02/force-quit-mac-apps/>


### How to set the terminal fopr cammand line applicationes (like fc)

Define var `EDITOR` in `~/.bashrc`:

    export EDITOR=/Applications/MacVim.app/Contents/MacOS/Vim

###  How to Copy and Paste To/From the Clipboard on the Command Line

You use the **`pbcopy`** and **`pbpaste`** commands.

- `pbcopy` Copy to Clipboard

- `pbpaste`	Paste from Clipboard

To add the standard output from any command to the clipboard, pipe it to the pbcopy command:

    curl -L "http://coolsite.com" | pbcopy

To paste text from the clipboard to the standard output stream, use the pbpaste command:

    pbpaste

The clipboard text will be printed out. If you’d like to do more with
it, you can pipe the data to any other application that accepts the standard input stream.
For instance, to create paginated output from a large block of text, you can pipe it to less:

    pbpaste | less

Source: <http://sweetme.at/2013/11/17/copy-to-and-paste-from-the-clipboard-on-the-mac-osx-command-line/>



### How to Capture a Screen Shot with Mac OS

A) To **capture the entire screen**:

Press `Command-Shift-3`

The screen shot will be automatically saved as
a PNG file on your desktop with the filename starting with “Picture” followed by a number, example
Picture 1, Picture 2, and so on.  

b) To **copy the entire screen**

Press `Command-Control-Shift-3`

The screen shot will be placed on your clipboard

c) To **capture a portion of the screen**

Press `Command-Shift-4`

A cross-hair cursor will appear and you
can click and drag to select the area you wish to capture. When you release the mouse button, the
screen shot will be automatically saved as a PNG file on your desktop following the same naming
convention as explained on the first tip.

d) To **copy a portion of the screen** to the clipboard

Press `Command-Control-Shift-4`.

A cross-hair
cursor will appear and you can click and drag to select the area you wish to capture. When you
release the mouse button, selected area is copied to the clipboard. 

d) To **Capture Specific application window**

Press and hold `Command-Shift-4` then tap on the Spacebar.

The cursor will change to a camera, and you can move it around the screen. As you move the cursor
over an application window, the window will be highlighted. The entire window does not need to be
visible for you to capture it. When you have the cursor over a window you want to capture, just
click the mouse button and the screen shot will be saved as a PNG file on your desktop.

e) To **copy a specific application window**

Press and hold `Command-Control-Shift-4` then tap on the Spacebar.

The cursor will change to a camera, which you can move around the screen. As you move the cursor
over an application window, the window will be highlighted. The entire window does not need to be
visible for you to capture it. When you have the cursor over a window you want to capture, just
click the mouse button and you can paste the screen shot into another application.


### Input unicode HEX with the MAC

> Source <https://poynton.ca/notes/misc/mac-unicode-hex-input.html>

You can key unicode hex input directly into any application in Mac OS X. I’ll
explain how, assuming that you are using default keyboard settings.

Perhaps you know the Unicode code point for a particular character, such as
**`U+03B1`** for Greek lowercase alpha (α). The Unicode Hex Input method allows
keying such a code directly. First, **make sure that Unicode Hex Input is
enabled**. Under the Apple menu (at the left of the menu bar), choose System
Preferences…, then choose Keyboard. **Make sure there’s a check in the box to
the left of “Show Keyboard & Character Viewers in menu bar”**: This will display
a flag (or flag-like) icon near the right-hand end of your menubar. Then choose
Input Sources… to access the preferences for Language & Text. Near the bottom of
the (long) scrolling list, **place a check next to Unicode Hex Input**, and at
the bottom right,** make sure there's a check next to “Show Input menu in menu
bar.”** Close the System Preferences window. Now, return to the application
you're interested in, and look at the right end of the menu bar for a flag. Pull
down that menu; Unicode Hex Input will now be one of the choices.

Choosing the Unicode Hex Input method alters the behaviour of the **“option”**
key. To place **`U+03B1`** into your document, hold down the option key and –
while holding it down – tap the four keys `0`, `3`, `b`, and `1` in sequence. On
pressing the last of the four, the character α appears; you can then release the
option key. To return to the normal option-key behaviour, access the “flag” menu
and choose your usual input method.

Common used unicode chars

| Desc                   | Char | Sequence      |
|------------------------|------|---------------|
| BALLOT BOX             | ☐    | `option` 2610 |
| BALLOT BOX WITH CHECK  | ☑    | `option` 2611 |
| BALLOT BOT WITH X      | ☒    | `option` 2612 |
| WHITE STAR             | ☆    | `option` 2602 |
| BACK STAR              | ★    | `option` 2605 |
| DANGER                 | ⚠    | `option` 26A0 |
| RIGHT ARROW            | →    | `option` 2192 |
| LEFT ARROW             | ←    | `option` 2190 |
| APROX                  | ≈    | `option` 2248 |
| ASYMPTOTIC             | ≃    | `option` 2243 |
| IDENTITY               | ≡    | `option` 2261 |

### How to Change Sudo Password Timeout

From the command line, edit the sudoers file with the help of visudo – do not attempt to edit /etc/sudoers without visudo

    sudo visudo

Use the arrow keys to navigate to the end of the sudoers file then enter the following syntax on a new line (feel free to include a comment by preceding with a hash # so you can reference it later)

    Defaults timestamp_timeout=30

In this example we’re using `30` as the timeout grace period, meaning minutes.

Source: <http://osxdaily.com/2016/05/05/change-sudo-password-timeout/>
