import logging
import traceback
from datetime import timedelta, time
import datetime
from kafka import KafkaConsumer
import json

from service.query import save_job, get_job, get_rule, get_rule__, update_the_job
from utility.constants import CONSUMER_TOPIC_NAME, REQUEST_MESSAGE, PENDING_STATUS, PREMIUM, STANDARD, DEFAULT, \
    COMPLETED_STATUS, KAFKA_SERVER_URL, CHECK_MESSAGE, STANDARD_ROLE
from utility.helper import generate_token, update_db_and_push_to_kafka

MESSAGE_TYPE = 'message_type'
REQUEST_ID = 'request_id'
ROLE = 'role'
REQUESTED_TIMESTAMP = 'requested_timestamp'


def consume_request_from_kafka():
    try:
        consumer = KafkaConsumer(
            CONSUMER_TOPIC_NAME,
            bootstrap_servers=KAFKA_SERVER_URL,
            auto_offset_reset='earliest')
        print("starting the consumer")
        for message in consumer:
            message_object = json.loads(message.value)
            print("Consumed request from Ticket Service")
            print(message_object)
            message_type = message_object.get(MESSAGE_TYPE)
            request_id = message_object.get(REQUEST_ID)
            logging.info("consumed the request for request_id {}". format(request_id))
            role = message_object.get(ROLE)
            requested_timestamp = message_object.get(REQUESTED_TIMESTAMP)
            status = PENDING_STATUS
            if message_type == REQUEST_MESSAGE:
                save_job(request_id, requested_timestamp, role, status)
                rule_object = get_rule(role)
                if rule_object is not None and rule_object.rule == PREMIUM:
                    job = get_job(request_id)
                    expires = datetime.timedelta(hours=1)
                    update_db_and_push_to_kafka(job, request_id, expires)

            else:
                job = get_job(request_id)
                rule_object = get_rule(role)
                if job and rule_object:
                    if job.status == COMPLETED_STATUS:
                        continue
                    if rule_object.rule == STANDARD:
                        requested_time = job.requested_timestamp
                        target_time = requested_time + timedelta(minutes=10)
                        current_time = datetime.datetime.utcnow()
                        if current_time >= target_time:
                            expires = datetime.timedelta(hours=1)
                            update_db_and_push_to_kafka(job, request_id, expires)
                    if rule_object.rule == DEFAULT:
                        requested_time = job.requested_timestamp
                        next_day = requested_time + timedelta(days=1)
                        current_time = datetime.datetime.utcnow()
                        target_time = datetime.datetime.combine(next_day, time.min)
                        if current_time >= target_time:
                            expires = datetime.timedelta(hours=2)
                            update_db_and_push_to_kafka(job, request_id, expires)
    except Exception as e:
        print(str(e))
        logging.error("error when consuming the message")
        logging.error(traceback.format_exc())
