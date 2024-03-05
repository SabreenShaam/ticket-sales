import json


def test_premium_user_token_request(client, login_premium_user_token):
    response = client.get('/request_ticketing_link', headers={'Content-Type': 'application/json',
                                                              'Authorization': login_premium_user_token})
    assert json.loads(response.data).get('message') == 'Your request is created successfully'
    assert response.status_code == 201


def test_standard_user_token_request(client, login_standard_user_token):
    response = client.get('/request_ticketing_link', headers={'Content-Type': 'application/json',
                                                              'Authorization': login_standard_user_token})
    assert json.loads(response.data).get('message') == 'Your request is created successfully'
    assert response.status_code == 201


def test_default_unregistered_user_token_request(client):
    response = client.get('/request_ticketing_link', headers={'Content-Type': 'application/json'})
    assert json.loads(response.data).get('message') == 'Your request is created successfully'
    assert response.status_code == 201


def test_request_token_with_registered_invalid_token(client):
    response = client.get('/request_ticketing_link', headers={'Content-Type': 'application/json',
                                                              'Authorization': 'Bearer '
                                                                               'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
                                                                               '.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMzE0NzE4NiwianRpIjoiOTU4MTRlYTEtZTBlOS00MjUxLTgzNDQtZTc3NDAwOTM4MDY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MywibmJmIjoxNzAzMTQ3MTg2LCJjc3JmIjoiOTE3ZTIxYjItYWUyYy00OTkzLWIyZTUtM2RjZDdhMDhlZWY1IiwiZXhwIjoxNzAzMTUwNzg2fQ.s6k7V_0vaE5iVEPxEmBo42gtdlPULVORn2HONuMT4tk'})
    assert response.status_code == 401
