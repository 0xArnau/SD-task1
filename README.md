#### Resources:
- https://python-rq.org/docs/

#### Requirements:
- pip install [rq](https://github.com/rq/rq)
- pip install [redis](https://github.com/andymccurdy/redis-py)
- pip install [grpcio](https://grpc.io/)

###### Generate stubs
    python -m grpc_tools.protoc --proto_path=. ./task.proto --python_out=. --grpc_python_out=.

## Task 1: Communication models and Middleware

The goal is to design and implement a cluster manager capable of executing 
parallel computing jobs in a number of worker nodes. We recommend to use standard 
middleware services like xmlrpc, grpc, and Redis.

The structure of the cluster includes a Master node and a group of worker nodes.
The Master node exposes a simple API with functionalities to: 

-   Manage Workers (add, remove, list)
-   Submit a task the cluster (Queue)
-   Submit a group of tasks to the cluster (submitting many tasks to the Queue)

In the Queue mode, all workers are listening to the Queue, and process one task at a time from the Queue.
Worker nodes may retrieve data arguments (urls) from a Web Server (http.server) and store their results in a Redis server.

**Optional**: Implement a Web interface to the Cluster.


To validate the code, test it with two experiments:

The objective of this practical assignment is to write two very simple programs:

1. CountingWords: Counts the total number of words in different text files or text entries.
    For example, given the following text: "I love Distributed Systems", the output of CountingWords should be 4 words.
2. WordCount: Counts the number of occurrences of each word in a text  file. For instance, given the following text: "foo bar bar foo", the  output of WordCount should be: bar, 2; foo, 2.
