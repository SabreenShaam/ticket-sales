import pytest
import json

from app import app as flask_app
from models.model import db


@pytest.fixture
def app():
    with flask_app.app_context():
        db.create_all()
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def premium_register_data(app):
    mock_register_data = {
        "email": "mac@gmail.com",
        "username": "mac",
        "password": "1q2W3E4r",
        "role": "premium"
    }
    return mock_register_data


@pytest.fixture
def standard_register_data(app):
    mock_register_data = {
        "email": "john@gmail.com",
        "username": "john",
        "password": "1q2W3E4r",
        "role": "standard"
    }
    return mock_register_data


@pytest.fixture
def login_premium_user_token(client, premium_register_data):
    response_data = client.get('/login', data=json.dumps(premium_register_data),
                               headers={'Content-Type': 'application/json'})
    result = json.loads(response_data.data.decode())
    token = 'Bearer ' + result['access_token']
    return token


@pytest.fixture
def login_standard_user_token(client, standard_register_data):
    client.post('/register', data=json.dumps(standard_register_data),
                headers={'Content-Type': 'application/json'})
    response_data = client.get('/login', data=json.dumps(standard_register_data),
                               headers={'Content-Type': 'application/json'})
    result = json.loads(response_data.data.decode())
    token = 'Bearer ' + result['access_token']
    return token


@pytest.fixture
def request_premium_user_token(client, login_premium_user_token):
    response_data = client.get('/request_ticketing_link',
                               headers={'Content-Type': 'application/json', 'Authorization': login_premium_user_token})
    request_id = json.loads(response_data.data).get('request_id')
    return request_id, login_premium_user_token


@pytest.fixture
def request_standard_user_token(client, login_standard_user_token):
    response_data = client.get('/request_ticketing_link',
                               headers={'Content-Type': 'application/json', 'Authorization': login_standard_user_token})
    request_id = json.loads(response_data.data).get('request_id')
    return request_id, login_standard_user_token


@pytest.fixture
def request_default_user_token_request(client):
    response_data = client.get('/request_ticketing_link')
    request_id = json.loads(response_data.data).get('request_id')
    return request_id


@pytest.fixture
def request_default_user_token_for_buy_ticket(client, login_standard_user_token):
    response_data = client.get('/request_ticketing_link',
                               headers={'Content-Type': 'application/json', 'Authorization': login_standard_user_token})
    request_id = json.loads(response_data.data).get('request_id')
    return request_id, login_standard_user_token
