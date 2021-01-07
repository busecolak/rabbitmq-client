#!/usr/bin/env python
import logging
import sys
import os
import connection_util

QUEUE = 'temp_queue'


def main():
    connection = connection_util.createTCPConnection()

    channel = connection.channel()

    channel.queue_declare(queue=QUEUE)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(
        queue=QUEUE, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
