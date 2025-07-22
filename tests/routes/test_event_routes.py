import pytest
from datetime import datetime
from tests.helpers import register_and_login, event_payload

def test_list_events_empty(client):
    resp = client.get('/api/events/')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['events'] == []
    assert data['total'] == 0


def test_create_event_success(client):
    token = register_and_login(client)
    resp = client.post(
        '/api/events/',
        json=event_payload(),
        headers={'Authorization': f'Bearer {token}'}
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['title'] == 'Networking Lunch'
    assert data['owner_id'] == 1


def test_create_event_missing_fields(client):
    token = register_and_login(client)
    resp = client.post(
        '/api/events/',
        json={'datetime': '2025-08-15T12:00:00'},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert resp.status_code == 400
    assert 'error' in resp.get_json()


def test_get_event_success(client):
    token = register_and_login(client)
    # create event
    create = client.post('/api/events/', json=event_payload(), headers={'Authorization': f'Bearer {token}'})
    event_id = create.get_json()['id']

    resp = client.get(f'/api/events/{event_id}')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['id'] == event_id
    assert data['title'] == 'Networking Lunch'


def test_get_event_not_found(client):
    resp = client.get('/api/events/999')
    assert resp.status_code == 404
    assert 'error' in resp.get_json()


def test_update_event_success(client):
    token = register_and_login(client)
    create = client.post('/api/events/', json=event_payload(), headers={'Authorization': f'Bearer {token}'})
    event_id = create.get_json()['id']

    update_resp = client.put(
        f'/api/events/{event_id}',
        json={'title': 'Updated Title'},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert update_resp.status_code == 200
    data = update_resp.get_json()
    assert data['title'] == 'Updated Title'


def test_update_event_permission_denied(client):
    token1 = register_and_login(client, username='alice', email='a@example.com')
    token2 = register_and_login(client, username='bob', email='b@example.com')
    create = client.post('/api/events/', json=event_payload(), headers={'Authorization': f'Bearer {token1}'})
    event_id = create.get_json()['id']

    resp = client.put(
        f'/api/events/{event_id}',
        json={'title': 'Hacked'},
        headers={'Authorization': f'Bearer {token2}'}
    )
    assert resp.status_code == 403


def test_delete_event_success(client):
    token = register_and_login(client) # type: ignore
    create = client.post('/api/events/', json=event_payload(), headers={'Authorization': f'Bearer {token}'})
    event_id = create.get_json()['id']

    resp = client.delete(
        f'/api/events/{event_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert resp.status_code == 200


def test_delete_event_not_found(client):
    token = register_and_login(client)
    resp = client.delete('/api/events/999', headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 404


def test_search_and_pagination(client):
    token = register_and_login(client)
    headers = {'Authorization': f'Bearer {token}'}
    # create three events
    for title in ['Alpha', 'Beta', 'Betamax']:
        payload = event_payload(title=title)
        client.post('/api/events/', json=payload, headers=headers)

    resp = client.get('/api/events/?search=Beta&per_page=1&page=1')
    data = resp.get_json()
    assert data['total'] == 2
    assert len(data['events']) == 1
    assert data['events'][0]['title'] == 'Beta'

    resp = client.get('/api/events/?search=Beta&per_page=1&page=2')
    data = resp.get_json()
    assert len(data['events']) == 1
    assert data['events'][0]['title'] == 'Betamax'


def test_event_ics_export(client):
    token = register_and_login(client)
    headers = {'Authorization': f'Bearer {token}'}
    create = client.post('/api/events/', json=event_payload(), headers=headers)
    event_id = create.get_json()['id']

    resp = client.get(f'/api/events/{event_id}.ics')
    assert resp.status_code == 200
    assert resp.mimetype == 'text/calendar'
    body = resp.data.decode()
    assert 'BEGIN:VCALENDAR' in body


def test_event_attendee_count(client):
    token = register_and_login(client)
    headers = {'Authorization': f'Bearer {token}'}
    create = client.post('/api/events/', json=event_payload(), headers=headers)
    event_id = create.get_json()['id']

    # second user registers
    token2 = register_and_login(client, username='bob', email='b@example.com')
    client.post(f'/api/events/{event_id}/register', headers={'Authorization': f'Bearer {token2}'})

    resp = client.get(f'/api/events/{event_id}')
    assert resp.status_code == 200
    assert resp.get_json()['attendee_count'] == 1

    list_resp = client.get('/api/events/')
    assert list_resp.status_code == 200
    list_data = list_resp.get_json()
    assert list_data['events'][0]['attendee_count'] == 1
