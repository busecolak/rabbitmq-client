import pika
import logging
import ssl

# example certificates
# CA_FILE_PATH = './SSL/ca_certificate.pem'
# CERT_FILE_PATH = './SSL/client_certificate.pem'
# KEY_FILE_PATH = './SSL/client_key.pem'

RMQ_PORT = 5672
RMQ_SSL_PORT = 5671
RMQ_HOST = 'localhost'
RMQ_VIRTUAL_HOST = '/'
RMQ_USER = 'admin'
RMQ_PASSWORD = 'password'
RMQ_SSL_SERVER_HOSTNAME = '*.example.com'


def configureSSLOptions():
    ### with client certificates (required if self-signed) ###
    # context = ssl.create_default_context(cafile=CA_FILE_PATH)
    # context.load_cert_chain(CERT_FILE_PATH, KEY_FILE_PATH)

    ### without client certificates (if ssl_options.fail_if_no_peer_cert=false) ###
    context = ssl.create_default_context()

    ssl_options = pika.SSLOptions(context, RMQ_SSL_SERVER_HOSTNAME)
    return ssl_options


def createSSLConnection():
    ssl_options = configureSSLOptions()
    credentials = pika.PlainCredentials(RMQ_USER, RMQ_PASSWORD)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RMQ_HOST,
            port=RMQ_SSL_PORT,
            virtual_host=RMQ_VIRTUAL_HOST,
            credentials=credentials,
            ssl_options=ssl_options)
    )
    return connection


def createTCPConnection():
    credentials = pika.PlainCredentials(RMQ_USER, RMQ_PASSWORD)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RMQ_HOST,
            port=RMQ_PORT,
            virtual_host=RMQ_VIRTUAL_HOST,
            credentials=credentials)
    )
    return connection
