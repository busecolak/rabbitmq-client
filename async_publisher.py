import logging
import threading
import time
import connection_util

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING, format=LOG_FORMAT)

MESSAGE_DELAY = 1
MESSAGE_COUNT = 1000
THREAD_COUNT = 10
EXCHANGE = "temp_exchange"
QUEUE = "temp_queue"

f = open("message.txt", "r")
temp_message = f.read()


class ProducerThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        LOGGER.warning("Starting " + self.name)

        self.produceMessage(self.name, self.counter)

    def produceMessage(self, thread_name, counter):
        LOGGER.warning("Running " + thread_name)

        connection = connection_util.createTCPConnection()
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct",
                                 passive=False, durable=True, auto_delete=False)
        channel.queue_declare(queue=QUEUE, durable=True)
        channel.queue_bind(queue=QUEUE, exchange=EXCHANGE,
                           routing_key="standard_key")

        while counter:
            time.sleep(MESSAGE_DELAY)

            message = temp_message

            channel.basic_publish(exchange=EXCHANGE,
                                  routing_key="standard_key", body=message)

            counter -= 1

        connection.close()


threads = []

for i in range(THREAD_COUNT):
    thread = ProducerThread(i, "Producer-Thread-" + str(i), MESSAGE_COUNT)
    threads.append(thread)

for t in threads:
    t.start()

for t in threads:
    t.join()

LOGGER.warning("Exiting Main Thread")
