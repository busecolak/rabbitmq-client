# rabbitmq-client

This is an example Python RabbitMQ Client, includes async consumer/producer. The clients also support the SSL connection.

## Components

### connection_util.py

The util file to configure amqp connection options such as host address/port, credentials, ssl options.

### async_publisher.py

The util to publish asynchronously the content given in the text file to the queue/exchange of the Rabbitmq server defined in the connection_util. The thread and the message count can be configured in the file.

### async_consumer.py

The util to consume asynchronously from the queue/exchange of the Rabbitmq server defined in the connection_util. The thread count and the consume delay can be configured in the file.

### producer.py

The basic producer to publish the given message to the queue/exchange of the Rabbitmq server defined in the connection_util.

### consumer.py

The basic consumer to consumer from the queue/exchange of the Rabbitmq server defined in the connection_util.

## Usage

* Configure the rabbitmq server options in connection_util.py
* Configure the Queue/Exchange and thread options in client files
* Edit the message text file to simulate the message size
* To run the async publisher

```bash
python async_publisher.py
```

* To run the async consumer

```bash
python async_consumer.py
```
