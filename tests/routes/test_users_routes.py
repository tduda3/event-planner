import pytest
from tests.helpers import register_and_login, event_payload

# Helpers to register and log in

def register_user(client, username='alice', email='alice@example.com', password='password123'):
    return client.post(
        '/api/users/register',
        json={'username': username, 'email': email, 'password': password}
    )

def login_user(client, email='alice@example.com', password='password123'):
    return client.post(
        '/api/users/login',
        json={'email': email, 'password': password}
    )


def test_register_user_success(client):
    resp = register_user(client)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['username'] == 'alice'
    assert data['email'] == 'alice@example.com'
    # Password hash should not be exposed
    assert 'password_hash' not in data


def test_register_missing_fields(client):
    resp = client.post('/api/users/register', json={'username': 'bob'})
    assert resp.status_code == 400
    assert 'error' in resp.get_json()



def test_login_success(client):
    register_user(client)
    resp = login_user(client)
    assert resp.status_code == 200
    assert 'access_token' in resp.get_json()


def test_login_invalid_credentials(client):
    register_user(client)
    resp = client.post(
        '/api/users/login',
        json={'email': 'alice@example.com', 'password': 'wrong'}
    )
    assert resp.status_code == 401
    assert 'error' in resp.get_json()


def test_get_user_success(client):
    # Register and log in to obtain a token
    reg = register_user(client)
    login = login_user(client)
    token = login.get_json()['access_token']
    # First registered user will have ID 1
    user_id = 1

    resp = client.get(
        f'/api/users/{user_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['id'] == user_id
    assert data['username'] == 'alice'


def test_get_user_unauthorized(client):
    resp = client.get('/api/users/1')  # no token
    assert resp.status_code == 401


def test_get_user_not_found(client):
    register_user(client)
    login = login_user(client)
    token = login.get_json()['access_token']

    resp = client.get(
        '/api/users/999',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert resp.status_code == 404
    assert 'error' in resp.get_json()


def test_user_profile_page(client):
    token = register_and_login(client)
    headers = {'Authorization': f'Bearer {token}'}
    client.post('/api/events/', json=event_payload(title='My Event'), headers=headers)

    token2 = register_and_login(client, username='bob', email='bob@example.com')
    other_headers = {'Authorization': f'Bearer {token2}'}
    create = client.post('/api/events/', json=event_payload(title='Other Event'), headers=other_headers)
    event2_id = create.get_json()['id']
    client.post(f'/api/events/{event2_id}/register', headers=headers)

    resp = client.get('/users/1')
    assert resp.status_code == 200
    text = resp.get_data(as_text=True)
    assert 'My Event' in text
    assert 'Other Event' in text
