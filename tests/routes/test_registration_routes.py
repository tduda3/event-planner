import pytest
from tests.helpers import register_and_login, event_payload

def test_rsvp_event_success(client):
    token = register_and_login(client)
    # Create an event
    create_resp = client.post(
        '/api/events/',
        json=event_payload(),
        headers={'Authorization': f'Bearer {token}'}
    )
    assert create_resp.status_code == 201
    event_id = create_resp.get_json()['id']

    # RSVP to the event
    resp = client.post(
        f'/api/events/{event_id}/register',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['event_id'] == event_id

def test_rsvp_event_not_found(client):
    token = register_and_login(client)
    resp = client.post(
        '/api/events/999/register',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert resp.status_code == 404

def test_cancel_registration_success(client):
    token = register_and_login(client)
    # Create and RSVP
    create_resp = client.post(
        '/api/events/',
        json=event_payload(),
        headers={'Authorization': f'Bearer {token}'}
    )
    event_id = create_resp.get_json()['id']
    reg_resp = client.post(
        f'/api/events/{event_id}/register',
        headers={'Authorization': f'Bearer {token}'}
    )
    reg_id = reg_resp.get_json()['id']

    # Cancel the registration
    resp = client.delete(
        f'/api/registrations/{reg_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['message'] == 'Registration canceled'

def test_cancel_other_user_forbidden(client):
    token1 = register_and_login(client)
    token2 = register_and_login(client, username='bob', email='bob@example.com')
    # Create and RSVP under token1
    create_resp = client.post(
        '/api/events/',
        json=event_payload(),
        headers={'Authorization': f'Bearer {token1}'}
    )
    event_id = create_resp.get_json()['id']
    reg_resp = client.post(
        f'/api/events/{event_id}/register',
        headers={'Authorization': f'Bearer {token1}'}
    )
    reg_id = reg_resp.get_json()['id']

    # Attempt cancel under token2
    resp = client.delete(
        f'/api/registrations/{reg_id}',
        headers={'Authorization': f'Bearer {token2}'}
    )
    assert resp.status_code == 403

def test_list_user_registrations(client):
    token = register_and_login(client)
    # Create and RSVP
    create_resp = client.post(
        '/api/events/',
        json=event_payload(),
        headers={'Authorization': f'Bearer {token}'}
    )
    event_id = create_resp.get_json()['id']
    client.post(
        f'/api/events/{event_id}/register',
        headers={'Authorization': f'Bearer {token}'}
    )

    # List registrations
    resp = client.get(
        '/api/users/1/registrations',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['event_id'] == event_id
