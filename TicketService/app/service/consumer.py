import logging
import traceback

from kafka import KafkaConsumer
import json

from service.query import get_job, update_the_job
from utility.constants import CONSUMER_TOPIC_NAME, KAFKA_SERVER_URL, COMPLETED_STATUS


REQUEST_ID = 'request_id'
TOKEN = 'token'


def Consume_Data_From_Kafka():
    try:
        consumer = KafkaConsumer(
            CONSUMER_TOPIC_NAME,
            bootstrap_servers=KAFKA_SERVER_URL,
            auto_offset_reset='earliest')
        print("starting the consumer")
        logging.info("consumer started")
        for message in consumer:
            message_object = json.loads(message.value)
            request_id = message_object.get(REQUEST_ID)
            print("Consumed token from Rule Service for request_id {}".format(request_id))
            print(message_object)
            logging.info("consumed the token for request_id {}". format(request_id))
            ticket_buying_token = message_object.get(TOKEN)
            job = get_job(request_id)
            if job:
                job.token = ticket_buying_token
                job.status = COMPLETED_STATUS
                job.token_is_valid = True
                update_the_job()
                print("job updated successfully")
    except Exception as e:
        logging.error("error when consuming token")
        logging.error(traceback.format_exc())
        print(str(e))
