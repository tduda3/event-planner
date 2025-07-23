import pytest


def test_home_route(client):
    resp = client.get('/')
    assert resp.status_code == 200
