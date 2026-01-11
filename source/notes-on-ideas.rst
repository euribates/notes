Ideas
========================================================================

Ideas para proyectos.


Catalog system
------------------------------------------------------------------------

Not automating I guess, but I built a handhield inventory updater. What
that means: I use a Raspberry pi with a barcodescanner connected via
usb. Set it to run the python script at boot. The script: It asks to
scan an items barcode. When baecode is scannesd, it asks to scan barcode
on shelf. So I go: scan item, scan shelf, scan item. Scan shelf and when
done alle the items I have scanned has been updated with the value on
the shelf. It sends an sql update queerie with the shelf value with the
where clause having the item value.

I hook the pi up with a powerbank, connect wifi, out it in my pocket and
off I go. Btw, it also has a led diode connected to the gpio. The led
blinks slowly to indicate that it is ready to scan barcode, and blinks
fast to indicate that it is ready to receive the shelf value. So I can
actually know when it is ready and if the update was succsessfully based
ofo of the led diode. Btw, our store has 1750 different shelves, sp this
has made things so much easier.


Transcribing interviews
------------------------------------------------------------------------

I’m quite new as well, so my code is really not very sophisticated. I’m
currently working on transcribing some interviews, and I wrote a code to
start each line I type with Interviewer >> or Guest >>. After I’m done
typing what one of them says, I press Enter and it switches. I can also
add time stamps for the interview. It tracks how long I’ve worked and
how much of the interview is transcribed.

File sorter
------------------------------------------------------------------------

File sorter in your Downloads folder that places files in their
appropriate location, whether into folders organized by extension or
moving .mp3 files into your Music folder, etc.

Blackoout alerter
------------------------------------------------------------------------

If you have a couple of spare PCs/RPis lying around, you might could try
to set up one of them to act as a server and the other to act as a
client where the server and internet router both sit on a UPS/battery
power and the other one client machine just sits in a standard outlet,
then program each device to constantly ask if the other one is still on
the network. That way, if you lose power, the server on battery backup
will still be able to talk on the network, but he won’t get any
responses, and then he will know the power is out and he can text you
letting you know (and if you wanted to get REALLY fancy, could issue
commands to other devices on your network to safely shutdown)
