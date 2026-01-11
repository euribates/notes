documenting
========================================================================


Use a wiki for personal learning, notes and interesting links
-------------------------------------------------------------

I’ve been extending and improving my personal wiki for 1 year now and it
has been one of the best things I’ve done. I found writing blog posts
was too high friction and very often didn’t finish things because there
is so much you can talk about in any given article. But a wiki is just a
living document containing your notes and thoughts on things. I also use
it as my public bookmark manager as I collect interesting to me links
under each topic.

For my wiki, I render everything to the web first with
`GitBook <https://www.gitbook.com/>`__. And I have a macro I run that
automatically commits any changes I’ve made with Sublime Text on the mac
and Ulysses on the phone so everything is super easy to edit and
publish.

The C4 model
------------

The C4 model is an "abstraction-first" approach to diagramming software
architecture, based upon abstractions that reflect how software
architects and developers think about and build software. The small set
of abstractions and diagram types makes the C4 model easy to learn and
use.

Source: `The C4 model for visualising software
architecture <https://c4model.com/>`__.

Cómo documentar la infraestrutura
---------------------------------

First, start with a **high level summary** of what the thing is does, as
well as what it is supposed to do. The second part should outline things
like the problem it’s solving, the challenges faced, the assumptions
made. This way the reader can understand the why better

I then go through the **major components at a high level** - here I used
an relational data as because xyz requirement, here I used a firewall
with xyz ports open because requirements, I used xyz for DNS, etc

Then tackle **lower level stuff** - database designs, throughout
requirement, record sizes, service discovery, failover strategies

Then a **config section** where I document any touchy or special configs
that are relevant

Then a **section on operations** - what are some common operations tasks
this thing may need, or things the oncall folks may need (how to
stop/start. Where logs are, how to access things, how to scale, what the
limits are of the system), any caveats or ugliness that exists, where
the code is, how to deploy with teraform etc.

Finally, I include **some test results that are relevant** - how many
writes you can do, how fast we reconverge on failover, how many things
per unit we can do with the design

I have a template I’ve built up over the years that I use - I just open
it up and start filling in sections, removing irrelevant parts. But the
overall idea is to start very high level and drill down into the parts
that most need describing. Don’t go into detail on common elements or
well understood tech, just the stuff that the intended audience would
need, but always with an eye to "what details will we all forget in 3
years when we have to fix this thing"

And always lots of pictures/diagrams

update - link to a re-created `Design Document
Template <https://docs.google.com/document/d/13_F8_nAIrYj3c_L9LVTMS7pZrP66O1fUAvRfonAE9Gk/edit?usp=sharing>`__
as a Google doc.

Enlaces
-------

-  `Design Document
Template <https://docs.google.com/document/d/13_F8_nAIrYj3c_L9LVTMS7pZrP66O1fUAvRfonAE9Gk/edit?usp=sharing>`__
-  `Does anyone else keep their own knowledge
wiki? <https://lobste.rs/s/ord0rg/does_anyone_else_keep_their_own_knowledge>`__
-  `How do you document your
infrastructure <https://www.reddit.com/r/aws/comments/dxmkci/how_do_you_document_your_infrastructure/>`__
-  `Richard Litt List of knowledge
repositories <https://github.com/RichardLitt/meta-knowledge>`__
-  `The Blue Book <https://lyz-code.github.io/blue-book/>`__
-  `The C4 model for visualising software
architecture <https://c4model.com/>`__
