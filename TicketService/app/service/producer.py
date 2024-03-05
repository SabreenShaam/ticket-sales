import json
import logging
import traceback

from kafka import KafkaProducer

from utility.constants import KAFKA_SERVER_URL, PRODUCER_TOPIC_NAME

MESSAGE_TYPE = 'message_type'
REQUEST_ID = 'request_id'
ROLE = 'role'
REQUESTED_TIMESTAMP = 'requested_timestamp'


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


def push_the_message_to_topic(request_id, message_type, requested_timestamp, user):
    try:
        producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER_URL],
                                 value_serializer=json_serializer)
        data = {
            REQUEST_ID: request_id,
            REQUESTED_TIMESTAMP: str(requested_timestamp),
            ROLE: user,
            MESSAGE_TYPE: message_type
        }
        print("Request pushed to Rule Service")
        print(data)
        producer.send(PRODUCER_TOPIC_NAME, data)
        logging.info("request sent to rule service for request_id {}". format(request_id))
    except Exception as e:
        logging.error("error when producing the request message")
        logging.error(traceback.format_exc())
        print(str(e))
