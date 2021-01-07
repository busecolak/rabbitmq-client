#!/usr/bin/env python
import logging
import connection_util

EXCHANGE = 'temp_exchange'
QUEUE = 'temp_queue'
MESSAGE = 'Hello World!'

logging.basicConfig(level=logging.ERROR)

connection = connection_util.createTCPConnection()

channel = connection.channel()

channel.queue_declare(queue=QUEUE, durable=True)

channel.basic_publish(exchange=EXCHANGE,
                      routing_key='standard_key', body=MESSAGE)

print("[x] Sent " + MESSAGE)

connection.close()
