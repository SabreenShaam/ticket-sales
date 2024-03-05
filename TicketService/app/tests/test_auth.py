import json


def test_register(client, premium_register_data):
    response = client.post('/register', data=json.dumps(premium_register_data),
                           headers={'Content-Type': 'application/json'})
    assert json.loads(response.data).get('message') == 'Account created successfully'
    assert response.status_code == 201


def test_register_already_exist_user(client, premium_register_data):
    response = client.post('/register', data=json.dumps(premium_register_data),
                           headers={'Content-Type': 'application/json'})
    assert response.json.get('message') == 'User already exists, Please login'
    assert response.status_code == 409


def test_login(client, premium_register_data):
    response = client.get('/login', data=json.dumps(premium_register_data),
                          headers={'Content-Type': 'application/json'})
    assert json.loads(response.data).get('message') == 'Login Success'
    assert response.status_code == 200


def test_login_invalid_username(client, premium_register_data):
    premium_register_data['username'] = 'invalid_user'
    response = client.get('/login', data=json.dumps(premium_register_data),
                          headers={'Content-Type': 'application/json'})
    assert json.loads(response.data).get('message') == 'Invalid username or password Please try again'
    assert response.status_code == 401
