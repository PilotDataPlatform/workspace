def test_get_connection_200(test_client, guacapy_client_mock):
    payload = {
        'container_code': 'unittest',
    }
    response = test_client.get('/v1/guacamole/connection', params=payload)
    assert response.status_code == 200


def test_create_connection_200(test_client, guacapy_client_mock):
    payload = {'container_code': 'unittest', 'username': 'unittest', 'port': 9000, 'hostname': 'fake.hostname'}
    response = test_client.post('/v1/guacamole/connection', json=payload)
    assert response.status_code == 200


def test_create_connection_400(test_client, guacapy_client_mock_connection_except):
    payload = {'container_code': 'unittest', 'username': 'unittest', 'port': 9000, 'hostname': 'fake.hostname'}
    response = test_client.post('/v1/guacamole/connection', json=payload)
    assert response.status_code == 400


def test_remove_connection_200(test_client, guacapy_client_mock):
    payload = {
        'container_code': 'unittest',
    }
    response = test_client.delete('/v1/guacamole/connection', params=payload)
    assert response.status_code == 200


def test_remove_connection_400(test_client, guacapy_client_mock_connection_except):
    payload = {
        'container_code': 'unittest',
    }
    response = test_client.delete('/v1/guacamole/connection', params=payload)
    print(response)
    assert response.status_code == 400
