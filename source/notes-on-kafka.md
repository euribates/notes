---
title: Notas sobre kafka
---

## Introduction to Kafka

**Apache Kafka** is a distributed streaming platform that:

- Publishes and subscribes to streams of records, similar to a message queue or enterprise messaging system.

- Stores streams of records in a fault-tolerant durable way.

- Processes streams of records as they occur.

Kafka is used for these broad classes of applications:

- real-time streaming data pipelines that reliably get data between systems or applications.

- real-time streaming applications that transform or react to the streams of data.

Kafka is run as a cluster on one or more servers that can span multiple datacenters. The Kafka
cluster stores streams of records in categories called **topics**. Each record consists of a key, a
value, and a timestamp.

Kafka has these core APIs:

**Producer API** : Applications can publish a stream of records to one or more Kafka topics.

**Consumer API** : Applications can subscribe to topics and process the stream of records produced
to them.

**Streams API** : Applications can act as a stream processor, consuming an input stream from one or
more topics and producing an output stream to one or more output topics, effectively transforming
the input streams to output streams.

**Connector API** : Build and run reusable producers or consumers that connect Kafka topics to
existing applications or data systems. For example, a connector to a relational database might
capture every change to a table.

In Kafka the communication between the clients and the servers is done with a simple,
high-performance, language agnostic TCP protocol. This protocol is versioned and maintains backwards
compatibility with older version. The Java client is provided for Kafka, but clients are available
in many languages.


## Topics and Logs

The core abstraction Kafka provides for a stream of records is the topic.

A topic is a category or feed name to which records are published. **Topics in Kafka are always
multi-subscriber**. This means that a topic can have zero, one, or many consumers that subscribe to
the data written to it.

For each topic, the Kafka cluster maintains a partitioned log that looks like this:

![Log anatomy](./kafka/log_anatomy.png)

Each partition is an ordered, immutable sequence of records that is continually appended to a
structured commit log. The records in the partitions are each assigned a sequential ID number called
the __offset__, that uniquely identifies each record within the partition.

The Kafka cluster durably persists all published records, whether they have been consumed using a
configurable retention period or not. For example, if the retention policy is set to two days, then
for the two days after a record is published, it is available for consumption, and then after the
two days have passed it is discarded to free up space. Kafka’s performance is effectively constant
with respect to data size, which means storing data for a long time is not a problem.

![Log consumer](./kafka/log_consumer.png)

The only metadata retained on a per-consumer basis is the offset or position of that consumer in the
log. **This offset is controlled by the consumer**. Normally a consumer will advance its offset linearly
as it reads records, however, because the position is controlled by the consumer it can consume
records in any order. For example, a consumer can reset to an older offset to reprocess data from
the past or skip ahead to the most recent record and start consuming from “now”.

This combination of features means that Kafka consumers can come and go without much impact on the
cluster or on other consumers. For example, you can use the command line tools to “tail” the
contents of any topic without changing what is consumed by existing consumers.

The partitions in the log allow it to scale beyond a size that will fit on a single server. Each
individual partition must fit on the servers that host it, but a topic can have many partitions so
it can handle an arbitrary amount of data. Partitions can also act as the unit of parallelism.


## Distribution

The partitions of the log are distributed over the servers in the Kafka cluster with each server
handling data and requests for a share of the partitions. Each partition is replicated across a
configurable number of servers for fault tolerance.

Each partition has one server that acts as the **“leader”** and zero or more servers which act as
**“followers”**. The leader handles all read and write requests for the partition while the followers
passively replicate the leader. If the leader fails, one of the followers will automatically become
the new leader. Each server acts as a leader for some of its partitions and a follower for others so
that load is successfully balanced within the cluster.


