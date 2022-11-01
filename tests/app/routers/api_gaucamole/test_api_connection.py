# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
        'connection_name': 'Test connection',
    }
    response = test_client.delete('/v1/guacamole/connection', params=payload)
    assert response.status_code == 200


def test_remove_connection_400(test_client, guacapy_client_mock_connection_except):
    payload = {
        'container_code': 'unittest',
        'connection_name': 'Test connection',
    }
    response = test_client.delete('/v1/guacamole/connection', params=payload)
    assert response.status_code == 400
