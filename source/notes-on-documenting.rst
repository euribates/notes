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
------------------------------------------------------------------------

Debemos empezar con un **resumen de alto nivel** donde se explique lo
que hace el sistema, y también lo que debería hacer. La segunda parte
deba explicar los detalles del problema que se está intenitando
solucionar, los desafios que suponen, y las suposiciones realizadas. El
objetivo de la sección es que el lector entienda «el porqué».

A continuación iriamos describiendo todos los **componentes de alto
nivel**: Aquí he usado esta base de datos relacional par cubrir el
requerimiento xyz, aquí usamos un *firewall* con los puertos xyx, para
este otro requerimiento, usamos xyz para el :term:`DNS`, etc.

Después vendría los **detalles de nivel inferior**: Esquemas de la base
de datos, tamaños de registro, estimación de capacidades, descubrimiento
de servicios, estrategias de recuperación ante fallos, etc.

Si hace falta, una sección de **configuración**, donde se debe
especificar detalles especiales o que puedan resultar confusos acerca de
la configuración.

A continuaucíón, una sección de **operaciones**, con todas las
operaciones habituales que se pueden / deben realizar en el sistema.
Como parar y arrancar servcios, como inspeccionar los *logs*, como
escalar el sistema. como se despliegan los cambios, etc.

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
