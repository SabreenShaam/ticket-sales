import json
from models.model import JobModel


def test_premium_user_buy_ticket_request(mocker, client, request_premium_user_token):
    request_id, bearer_token = request_premium_user_token
    bearer_token = bearer_token.split()
    token = bearer_token[1]
    role = 'premium'
    status = 'COMPLETED'
    requested_timestamp = '2023-12-23 05:41:11'
    token = token
    token_is_valid = True
    mock_job_object = JobModel(request_id, role, status, requested_timestamp, token, token_is_valid)
    mocker.patch('app.get_job', return_value=mock_job_object)
    response = client.get('/buy_ticket/' + token + '?request_id=' + request_id)
    assert json.loads(response.data).get('message') == 'Welcome to the Ticket Page'
    assert response.status_code == 200


def test_standard_user_buy_ticket_request(mocker, client, request_standard_user_token):
    request_id, bearer_token = request_standard_user_token
    bearer_token = bearer_token.split()
    token = bearer_token[1]
    role = 'standard'
    status = 'COMPLETED'
    requested_timestamp = '2023-12-23 05:41:11'
    token = token
    token_is_valid = True
    mock_job_object = JobModel(request_id, role, status, requested_timestamp, token, token_is_valid)
    mocker.patch('app.get_job', return_value=mock_job_object)
    response = client.get('/buy_ticket/' + token + '?request_id=' + request_id)
    assert json.loads(response.data).get('message') == 'Welcome to the Ticket Page'
    assert response.status_code == 200


def test_default_user_buy_ticket_request(mocker, client, request_default_user_token_for_buy_ticket):
    request_id, bearer_token = request_default_user_token_for_buy_ticket
    bearer_token = bearer_token.split()
    token = bearer_token[1]
    role = 'default'
    status = 'COMPLETED'
    requested_timestamp = '2023-12-23 05:41:11'
    token = token
    token_is_valid = True
    mock_job_object = JobModel(request_id, role, status, requested_timestamp, token, token_is_valid)
    mocker.patch('app.get_job', return_value=mock_job_object)
    response = client.get('/buy_ticket/' + token + '?request_id=' + request_id)
    assert json.loads(response.data).get('message') == 'Welcome to the Ticket Page'
    assert response.status_code == 200
