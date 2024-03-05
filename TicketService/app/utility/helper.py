import base64
import datetime
import json
import logging
import traceback

from flask import jsonify
from flask_jwt_extended import create_access_token

from utility.constants import PREMIUM_ROLE, STANDARD_ROLE, DEFAULT_ROLE


def generate_response(message, status):
    response = {'message': message}
    return jsonify(response), status


def generate_response_for_token_request(message, request_id, status):
    response = {'message': message, 'request_id': request_id}
    return jsonify(response), status


def generate_response_for_generated_link(message, link, status):
    response = {'message': message, 'link': link}
    return jsonify(response), status


def generate_token(message, user, expires=datetime.timedelta(hours=1)):
    response = {'message': message,
                'access_token': create_access_token(
                        identity=user, expires_delta=expires)}
    return jsonify(response), 200


def check_token_expiration(token):
    try:
        split_token = token.split(".")
        decoded_payload = json.loads(base64.b64decode(split_token[1] + '=' * (-len(split_token[1]) % 4)).decode())
        expiration_epoch = decoded_payload['exp']
        expiration_time = datetime.datetime.fromtimestamp(expiration_epoch)
        current_time = datetime.datetime.now()
        return current_time > expiration_time
    except Exception as e:
        logging.error("error when check token expiration")
        logging.error(traceback.format_exc())
        print(str(e))


def validate_role(role):
    roles = [PREMIUM_ROLE, STANDARD_ROLE, DEFAULT_ROLE]
    return role in roles
