import json
import logging
import traceback

from kafka import KafkaProducer

from utility.constants import KAFKA_SERVER_URL, PRODUCER_TOPIC_NAME, DEFAULT_ROLE

REQUEST_ID = 'request_id'
TOKEN = 'token'


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


def push_the_message_to_topic(token, request_id):
    try:
        producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER_URL],
                                 value_serializer=json_serializer)
        data = {
            REQUEST_ID: request_id,
            TOKEN: token,
        }
        print("Pushed the token to Ticket Service")
        print(data)
        producer.send(PRODUCER_TOPIC_NAME, data)
        logging.info("message sent for the request_id {}".format(request_id))
    except Exception as e:
        print(str(e))
        logging.error("error when pushing the message for the request_id {}".format(request_id))
        logging.error(traceback.format_exc())
