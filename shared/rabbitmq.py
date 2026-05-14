import json

import pika

from shared.config.settings import settings


def publish_message(message: dict):

    credentials = pika.PlainCredentials(
        settings.RABBITMQ_USERNAME,
        settings.RABBITMQ_PASSWORD
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials
        )
    )

    channel = connection.channel()

    channel.queue_declare(queue="document-results")

    channel.basic_publish(
        exchange="",
        routing_key="document-results",
        body=json.dumps(message)
    )

    connection.close()
