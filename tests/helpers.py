def register_and_login(client, username='host', email='host@example.com', password='pass1234'):
    client.post('/users/register', json={
      'username': username,
      'email': email,
      'password': password
    })
    login = client.post('/users/login', json={
      'email': email,
      'password': password
    })
    return login.get_json()['access_token']

def event_payload():
    return {
        'title': 'Networking Lunch',
        'datetime': '2025-08-15T12:00:00',
        'location': 'Office Cafeteria',
        'description': 'Meet and greet with team'
    }
