Autokey
=======

.. tags:: development

Qué es :index:`AutoKey`
-----------------------------------------------------------------------

**AutoKey** es una aplicación de *scripting* de código libre
para Linux, similar a `AutoHotKey`_ para windows.


AutoKey allows the user to define hotkeys and trigger phrases[1] which
expand to predefined text, automating frequent or repetitive tasks such
as correcting typographical errors or common spelling mistakes and
inserting boiler plate sections of text.

Like many of you, I’ve been aware that there are several desktop
automation utilities available for Linux, but until recently, I’d never
used one. However, one of our readers sent me an email suggesting that I
check out Autokey, so I did. (Thanks Keith)
http://code.google.com/p/autokey/ Essentially, Autokey lets you assign
commonly used text to a hot key; then the hot key can be used as a
shortcut for the original text. For example, I live in Albuquerque, and
as you might imagine, this is tedious to type and is often misspelled.
Wouldn’t it be nice if all I had to do was press alt-a, instead? As a
start, this is the type of thing that Autokey can do for us, and more.

Once we’ve defined a piece of text with Autokey, there are a couple of
ways we can access that text. We can assign the text to a hot key, such
as alt-a or ctl-alt-z. Alternatively, we can make the text available
from a menu in the Autokeypanel at the bottom of the screen. Finally, we
can define an abbreviation that can be used in place of the text. For
example, a Perl programmer such as myself, might like to use the
abbreviation, “sub” and have it defined as:

subx {

}

This way, any time I started to define a new subroutine, Autokey would
fill in a basic skeleton of a subroutine and move the cursor back up to
the subroutine name.

As you can see, we’re able to send special keys by using their names.
Autokey has a long list of special keys it can send. We also have the
ability to define abbreviations to be case insensitive or to only
trigger on windows with a specific name.

If this was all that Autokey could do, it would still be a useful tool,
but this article wouldn’t make for very interesting reading.
Fortunately, there’s more; Autokey has a built-in Python interpreter and
an API that allows us to do some really interesting things.

He’re a quick example:

choices = [“konqueror”, “firefox”, “chrome”]

retCode, choice = dialog.list_menu(choices)

if retCode == 0:

system.exec_command(choice + ” ” + clipboard.get_selection())

This quick little script allows us to highlight a URL, press a hot-key,
select one of three different browsers from a dialog box, and open the
URL with the chosen browser.

La API de AutoKey
------------------------------------------------------------------------

So let’s dig a bit deeper into Autokey’s Python API.

Autokey’s keyboard class provides send_keys(), and a few variations,
which provides a means of sending keystrokes to the windows manager. An
Autokey script first calculates what it wants to send, and uses the
send_keys() method to send it. The trick, of course, is to determine
what to send, and that is the purpose of much of the rest of the Autokey
API.

The mouse class provides click_relative() and click_absolute(). These
methods simulate mouse clicks and allow us to determine which mouse
button to simulate, as well as where it should click based on XY
coordinates. The absolute variant simulates mouse clicks anywhere on the
screen. The relative version simulates clicks within the currently
active window.

The store class allows our Autokey scripts to persistently store
key/value pairs and access them later. Here we find set_value(),
get_value(), and remove_value(). The set_value() method accepts a key
and a value. Then, the get_value() method can be passed a key value and
will return the appropriate value. The remove_value() method deletes a
given key/value pair from the database. I found it strange that there
seemed to be no way to know if a particular key/value pair exists. Then
I came across the has_key() method in one of the example scripts; it
isn’t documented in the API documentation. But, it apparently returns a
boolean value indicating that a given key exists.

The system class provides only two functions, exec_command() and
create_file(). The exec_command() method allows an Autokey script to run
an external command and optionally capture the command’s output. The
only caveat is that the method, and thus Autokey itself, blocks while
the command runs, so the command needs to terminate immediately. The
create_file() method creates a given file and inserts content into it.
Strangely, there doesn’t seem to be a corresponding read_file() method.

The QtClipboard and GtkClipboard classes provide access to the windows
manager’s clipboard. As you can see, there is a Qt and a Gtk variant.
You’ll have to be sure to use the appropriate version depending on which
windows manager you use. Both versions export the same methods. Here,
it’s important to recognize the difference between a clipboard and a
mere selection. With this distinction in mind, we find that the
\*clipboard classes export get_selection(), fill_selection(),
get_clipboard(), and fill_clipboard() methods. With these methods, we
can get and replace text in either the clipboard or the currently
selected text.

The engine class provides methods that allow us to create new scripts
and abbreviations. I actually didn’t find these methods too interesting
myself, so I won’t spend much time here discussing them. I simply
appreciated their existence from a completeness point of view.

The window class provides methods for managing and manipulating windows
within the windows manager. These methods allow us to move, resize, and
close windows as well as move them to different desktops. We can also
minimize, window shade, and maximize windows with methods from this
class. While recognizing the power to be had from these methods, I don’t
envision the need to manipulate a particular window and thus, haven’t
explored this class very thoroughly. Suffice it to say that there is
quite a bit you can do, if you need to.

I happen to think that I’ve described some pretty powerful Autokey
capabilities, but here comes the really cool part. The dialog class,
which also comes in both Qt and Gtk variants provides a very powerful
mechanism for interacting with the user. Here we find methods for
presenting the user with dialog boxes, password boxes, menu dialogs,
file and directory pickers, and color pickers. This is where I think the
real power is to be had from Autokey as it gives us the ability to write
simple interactive scripts and assign them to hot-keys for convenient
access. It wouldn’t be hard, for example, to write a script that would
allow us to select a URL from our browser window, press a hotkey, and be
presented with the user name and password that we need to use to access
the site. This password management system would work no matter which
browser we chose to use.

Over the years, I’ve grown accustomed to having my windows organized in
a particular way, depending on what I’m doing. For example, when I’m
doing web development, I like a web browser occupying two thirds of the
width of my screen, and all of the height. Then I like my console
filling the rest of the screen. With Autokey, this configuration, and
much more complex configurations, could be a keystroke away.


.. _AutoHotKey: https://www.autohotkey.com/
