from flask_jwt_extended import create_access_token

from service.producer import push_the_message_to_topic
from service.query import update_the_job
from utility.constants import COMPLETED_STATUS


def generate_token(job, expires=None):
    return create_access_token(identity=job, expires_delta=expires)


def update_db_and_push_to_kafka(job, request_id, expires=None):
    token = generate_token(job, expires)
    job.status = COMPLETED_STATUS
    update_the_job()
    push_the_message_to_topic(token, request_id)
