import functools
import logging
import pika
import threading
import time
import connection_util

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -10s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING, format=LOG_FORMAT)

CONSUME_DELAY = 1
PREFETCH_COUNT = 1
THREAD_COUNT = 10
EXCHANGE = "temp_exchange"
QUEUE = "temp_queue"


class ConsumerThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        LOGGER.warning("Starting " + self.name)

        self.consumeMessage(self.threadID, self.name, self.counter)

    def consumeMessage(self, threadID, thread_name, counter):
        LOGGER.warning("Running " + thread_name)

        connection = connection_util.createTCPConnection()
        channel = connection.channel()
        self.channel = channel
        channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct",
                                 passive=False, durable=True, auto_delete=False)
        channel.queue_declare(queue=QUEUE, durable=True)
        channel.queue_bind(queue=QUEUE, exchange=EXCHANGE,
                           routing_key="standard_key")
        channel.basic_qos(prefetch_count=counter)

        cb = functools.partial(
            self.do_work, args=(connection, threadID))

        channel.basic_consume(on_message_callback=cb, queue=QUEUE)

        channel.start_consuming()

    def ack_message(self, channel, delivery_tag):
        if channel.is_open:
            channel.basic_ack(delivery_tag)
        else:
            pass

    def do_work(self, channel, method_frame, header_frame, body, args):
        (connection, thread_id) = args
        delivery_tag = method_frame.delivery_tag

        fmt1 = 'Thread id: {} Delivery tag: {} Message body: {}'
        LOGGER.warning(fmt1.format(thread_id, delivery_tag, body))

        time.sleep(CONSUME_DELAY)

        cb = functools.partial(self.ack_message, channel, delivery_tag)
        connection.add_callback_threadsafe(cb)


threads = []

for i in range(THREAD_COUNT):
    thread = ConsumerThread(i, "Consumer-Thread-" + str(i), PREFETCH_COUNT)
    threads.append(thread)

for t in threads:
    t.daemon = True
    t.start()

for t in threads:
    t.join()

LOGGER.warning("Exiting Main Thread")
