Neo4j
========================================================================


Notes on New4j
--------------

There are two important properties of graph database technologies you
need to understand:

1. Graph Storage

Some graph databases use “native” graph storage that is specifically
designed to store and manage graphs, while others use relational or
object-oriented databases instead. Non-native storage is often slower
than a native approach.

2. Graph Processing Engine

Native graph processing (a.k.a. “index-free adjacency”) is the most
efficient means of processing data in a graph because connected nodes
physically “point” to each other in the database. However, non-native
graph processing engines use other means to process Create, Read, Update
or Delete (CRUD) operations.

Graph databases are extremely useful in understanding big datasets in
scenarios as diverse as **logistics route optimization**, **retail
suggestion engines**, **fraud detection** and **social network
monitoring**.

Graphs Put Data Relationships at the Center
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you want a cohesive picture of your big data, including the
connections between elements, you need a graph database. In contrast to
relational and NoSQL databases, graph databases store data relationships
as relationships. This explicit storage of relationship data means
**fewer disconnects between your evolving schema and your actual
database**. In fact, the flexibility of a graph model allows you to add
new nodes and relationships without compromising your existing network
or expensively migrating your data.

All of your original data (and its original relationships) remain
intact.

With data relationships at their center, graphs are incredibly efficient
when it comes to query speeds, even for deep and complex queries. In
Neo4j in Action, the authors performed an experiment between a
relational database and a Neo4j graph database. Their experiment used a
basic social network to find friends-of-friends connections to a depth
of five degrees. Their dataset included 1,000,000 people each with
approximately 50 friends. The results of their experiment are listed in
the table below:

+-----+-----------------------+-----------------------+----------------+
| De  | RDBMS execution       | Neo4j execution       | Records        |
| pth | time(s)               | time(s)               | returned       |
+=====+=======================+=======================+================+
| 2   | 0.016                 | 0.01                  | ~2,500         |
+-----+-----------------------+-----------------------+----------------+
| 3   | 30.267                | 0.168                 | ~110,000       |
+-----+-----------------------+-----------------------+----------------+
| 4   | 1543.505              | 1.359                 | ~600,000       |
+-----+-----------------------+-----------------------+----------------+
| 5   | Unfinished            | 2.132                 | ~800,000       |
+-----+-----------------------+-----------------------+----------------+
