- http://www.multigesture.net/articles/how-to-write-an-emulator-chip-8-interpreter/
- http://www.malinc.se/math/latex/latexontheweben.php
- https://skerritt.blog/dynamic-programming/
- https://research.checkpoint.com/cryptographic-attacks-a-guide-for-the-perplexed/
- https://medium.com/@halfspring/guide-to-an-oauth2-api-with-django-6ba66a31d6d
- https://simpleisbetterthancomplex.com/tutorial/2018/12/19/how-to-use-jwt-authentication-with-django-rest-framework.html

### njs blog - Notes on structured concurrency, or: Go statement considered harmful

Every concurrency API needs a way to run code concurrently. One way is the asyoncronous call. There
are lots of variations in the notation and terminology, but the semantics are the same: these all
arrange for a func to start running concurrently to the rest of the program, and then return
immediately so that the parent can do other things.

Another option is to use callbacks. Again, the notation varies, but these all accomplish the same
thing: they arrange that from now on, if and when a certain event occurs, then a func will run. Then
once they've set that up, they immediately return so the caller can do other things. (Sometimes
callbacks get dressed up with fancy helpers like _promise_, _combinators_, or Twisted-style
_protocols/transports_, but the core idea is the same.)

Take any real-world, general-purpose concurrency API, and you'll probably find that it falls into one 
or the other of those buckets (or sometimes both, like asyncio).

But my new library Trio is weird. It doesn't use either approach. Instead, if we want to run myfunc
and anotherfunc concurrently, we write something like:

```Python
    async with trio.open_nursery() as nursery:
        nursery.start_soon(myfunc)
        nursery.start_soon(anotherfunc)
```

When people first encounter this "nursery" construct, they tend to find it confusing. Why is there
an indented block? What's this nursery object, and why do I need one before I can spawn a task? Then
they realize that it prevents them from using patterns they've gotten used to in other frameworks,
and they get really annoyed. It feels quirky and idiosyncratic and too high-level to be a basic
primitive. These are understandable reactions! But bear with me.

In this post, I want to convince you that nurseries aren't quirky or idiosyncratic at all, but
rather a new control flow primitive that's just as fundamental as for loops or function calls. And
furthermore, the other approaches we saw above – thread spawning and callback registration – should
be removed entirely and replaced with nurseries.

https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/
