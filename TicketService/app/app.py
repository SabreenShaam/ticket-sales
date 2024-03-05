import traceback
import uuid
import datetime
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from utility.helper import validate_role
from config import JWT_SECRET_KEY, DB_ENGINE
from models.model import db
from flask_apscheduler import APScheduler

from service.consumer import Consume_Data_From_Kafka
from service.producer import push_the_message_to_topic
from service.query import save_user, search_uname, get_user, store_the_user_request
from utility.constants import REQUEST_MESSAGE, CHECK_MESSAGE, DEFAULT_ROLE, BASE_URL
from utility.helper import generate_response, generate_token, check_token_expiration, \
    generate_response_for_token_request, generate_response_for_generated_link

from service.query import get_job, update_the_job
from utility.constants import COMPLETED_STATUS

app = Flask(__name__)
CORS(app)
jwt = JWTManager()

# app.config['SQLALCHEMY_DATABASE_URI'] = DB_ENGINE
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db_ticket/ticket'
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
jwt.init_app(app)
db.init_app(app)
schedular = APScheduler()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@app.route('/', methods=['GET'])
def Index():
    return jsonify({'hello': 'world'})


@app.route('/register', methods=['POST'])
def Register():
    if request.method == 'POST':
        try:
            email = request.json['email']
            username = request.json['username']
            password = request.json['password']
            role = request.json['role']
            if role and not validate_role(role):
                return generate_response('invalid role', 400)
            if search_uname(username):
                logging.info("username {} already exists".format(username))
                return generate_response('User already exists, Please login', 409)
            save_user(email, username, password, role)
            logging.info("user account created for {} ".format(username))
            return generate_response('Account created successfully', 201)
        except KeyError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            db.session.rollback()
            logging.error("user registration error")
            logging.error(traceback.format_exc())
            return jsonify({'error': str(e)}), 401


@app.route('/login', methods=['POST'])
def Login():
    if request.method == 'POST':
        try:
            username = request.json['username']
            password = request.json['password']
            user = search_uname(username)
            if user and user.password_is_valid(password):
                logging.info("user {} login success".format(user))
                return generate_token('Login Success', user)
            return generate_response('Invalid username or password Please try again', 401)
        except KeyError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logging.error("user login error")
            logging.error(traceback.format_exc())
            return jsonify({'message': str(e)}), 401


@app.route('/request_for_ticketing_link', methods=['GET'])
@jwt_required(optional=True)
def Request_Ticket_Link():
    if request.method == 'GET':
        bearer = request.headers.get("Authorization")
        request_id = str(uuid.uuid4())
        requested_timestamp = datetime.datetime.utcnow()
        try:
            if bearer is not None:
                current_user = get_jwt_identity()
                user = get_user(current_user)
                if not user:
                    return generate_response('Login to continue', 401)
                store_the_user_request(request_id, requested_timestamp, user.role)
                push_the_message_to_topic(request_id, REQUEST_MESSAGE, requested_timestamp, user.role)
                logging.info("request_id {} sent to rule service".format(request_id))
                return generate_response_for_token_request('Your request is created successfully', request_id, 201)

            else:
                store_the_user_request(request_id, requested_timestamp)
                push_the_message_to_topic(request_id, REQUEST_MESSAGE, requested_timestamp, DEFAULT_ROLE)
                logging.info("request_id {} sent to rule service".format(request_id))
                return generate_response_for_token_request('Your request is created successfully', request_id, 201)
        except Exception as e:
            logging.error("link request error for request_id {}", format(request_id))
            logging.error(traceback.format_exc())
            return jsonify({'message': str(e)}), 401


@app.route('/check_ticketing_link', methods=['GET'])
@jwt_required(optional=True)
def Check_Ticket_Link():
    if request.method == 'GET':
        bearer = request.headers.get("Authorization")
        request_id = request.args.get('request_id')
        if not request_id:
            return generate_response('request_id is missing ', 400)
        if bearer is not None:
            current_user = get_jwt_identity()
            user = get_user(current_user)
            if not user:
                return generate_response('Login to continue', 401)
            job = get_job(request_id)
            if not job:
                return generate_response('Incorrect request_id', 400)
            if job.status == COMPLETED_STATUS:
                token = job.token
                job.token_is_valid = True
                update_the_job()
                logging.info("link issued for request_id {}", format(request_id))
                return generate_response_for_generated_link('Link Generated Successfully', BASE_URL + '/buy_ticket/' + token +
                                                            '?request_id=' + request_id, 200)
            else:
                push_the_message_to_topic(request_id, CHECK_MESSAGE, job.requested_timestamp, job.role)
                logging.info("request_id {} sent to rule service".format(request_id))
                logging.info("link is not ready yet for the request_id {}", format(request_id))
                return generate_response('Your link is not ready yet please wait', 200)

        else:
            job = get_job(request_id)
            if not job:
                return generate_response('Your request_id is invalid', 404)
            if job.status == COMPLETED_STATUS:
                token = job.token
                job.token_is_valid = True
                update_the_job()
                logging.info("link is not ready yet for the request_id {}", format(request_id))
                return generate_response_for_generated_link('Link Generated Successfully', BASE_URL + '/buy_ticket/' + token +
                                                            '?request_id=' + request_id, 200)

            else:
                push_the_message_to_topic(request_id, CHECK_MESSAGE, job.requested_timestamp, DEFAULT_ROLE)
                logging.info("request_id {} sent to rule service".format(request_id))
                logging.info("link is not ready yet for the request_id {}", format(request_id))
                return generate_response('Your link is not ready yet please wait', 200)


@app.route('/buy_ticket/<string:token>', methods=['GET'])
def Buy_Ticket(token):
    if request.method == 'GET':
        request_id = request.args.get('request_id')
        if not request_id:
            return generate_response('request_id is missing ', 400)
        job = get_job(request_id)
        if not job:
            return generate_response('Your request_id is invalid', 404)
        if job.token != token:
            return generate_response('Your link is Wrong', 400)
        if not job.token_is_valid:
            return generate_response('Your link is Invalid', 400)

        if check_token_expiration(token):
            return generate_response('Your link is Expired', 401)
        job.token_is_valid = False
        update_the_job()
        logging.info("ticket booking page accessed for request_id {}", format(request_id))
        return generate_response('Welcome to the Ticket Page', 200)


def Consume_Data():
    with app.app_context():
        db.create_all()
        Consume_Data_From_Kafka()


if __name__ == '__main__':
    schedular.add_job(id='consume messages from kafka', func=Consume_Data)
    schedular.start()
    app.run(host='0.0.0.0', port=5000)
