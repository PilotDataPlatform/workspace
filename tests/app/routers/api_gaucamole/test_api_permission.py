def test_get_permission_200(test_client, guacapy_client_mock):
    payload = {
        'container_code': 'unittest',
        'username': 'unittest',
    }
    response = test_client.get('/v1/guacamole/permission', params=payload)
    assert response.status_code == 200


def test_grant_permission_200(test_client, guacapy_client_mock):
    payload = {
        'container_code': 'unittest',
        'username': 'unittest',
        'permissions': ['READ'],
        'operation': 'add',
    }
    response = test_client.post('/v1/guacamole/permission', json=payload)
    assert response.status_code == 200


def test_grant_permission_400(test_client, guacapy_client_mock_grant_permission_400):
    payload = {
        'container_code': 'unittest',
        'username': 'unittest',
        'permissions': ['READ'],
        'operation': 'add',
    }
    response = test_client.post('/v1/guacamole/permission', json=payload)
    assert response.status_code == 400
