gmail
========================================================================

.. tags:: Google,email


Notes on Gmail
--------------

How to send messages using gmail
--------------------------------

Using imap:

::

Send email from: Your gmail address
Hostname: imap.gmail.com
Port: 465
Username: Your gmail address
Password: Your app password
Encryption: SSL

Google’s Gmail SMTP server is a free SMTP service which anyone who has a
Gmail account can use to send emails. You can use it with personal
emails, or even with your website if you are sending emails for things
such as contact forms, newsletter blasts, or notifications.

To use Gmail’s SMTP server, you will need the following settings for
your outgoing emails:

::

Outgoing Mail (SMTP) Server: smtp.gmail.com
Use Authentication: Yes
Use Secure Connection: Yes (TLS or SSL depending on your mail client/website SMTP plugin)
Username: your Gmail account (e.g. user@gmail.com)
Password: your Gmail password
Port: 465 (SSL required) or 587 (TLS required)
