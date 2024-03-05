import json


def test_premium_user_check_token_request(client, request_premium_user_token):
    request_id, token = request_premium_user_token
    response = client.get('/check_ticketing_link?request_id=' + request_id, headers={'Content-Type': 'application/json',
                                                                                     'Authorization': token})
    assert response.status_code == 200


def test_standard_user_check_token_request(client, request_standard_user_token):
    request_id, token = request_standard_user_token
    response = client.get('/check_ticketing_link?request_id=' + request_id, headers={'Content-Type': 'application/json',
                                                                                     'Authorization': token})
    assert json.loads(response.data).get('message') == 'Your Token is not ready yet please wait'
    assert response.status_code == 200


def test_default_unregistered_user_check_token_request(client, request_default_user_token_request):
    request_id = request_default_user_token_request
    response = client.get('/check_ticketing_link?request_id=' + request_id)
    assert json.loads(response.data).get('message') == 'Your Token is not ready yet please wait'
    assert response.status_code == 200
