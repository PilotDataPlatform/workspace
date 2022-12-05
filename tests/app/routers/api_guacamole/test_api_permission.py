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
from app.config import ConfigClass


def test_get_permission_200(test_client, guacapy_client_mock):
    payload = {
        'container_code': 'unittest',
        'username': 'unittest',
    }
    response = test_client.get('/v1/guacamole/permission', params=payload)
    assert response.status_code == 200


def test_grant_permission_200(test_client, guacapy_client_mock):
    payload = {
        'connection_name': 'Test connection',
        'container_code': 'unittest',
        'username': 'unittest',
        'permissions': ['READ'],
        'operation': 'add',
    }
    response = test_client.post('/v1/guacamole/permission', json=payload)
    assert response.status_code == 200


def test_grant_permission_400(test_client, guacapy_client_mock_grant_permission_400):
    payload = {
        'connection_name': 'Test connection',
        'container_code': 'unittest',
        'username': 'unittest',
        'permissions': ['READ'],
        'operation': 'add',
    }
    response = test_client.post('/v1/guacamole/permission', json=payload)
    assert response.status_code == 400


def test_create_user_200(test_client, guacapy_client_mock):
    payload = {
        'container_code': 'unittest',
        'username': 'unittest',
    }
    response = test_client.post('/v1/guacamole/users', json=payload)
    assert response.status_code == 200


def test_create_user_400(test_client, guacapy_client_mock_add_user_400):
    payload = {
        'container_code': 'unittest',
        'username': 'unittest',
    }
    response = test_client.post('/v1/guacamole/users', json=payload)
    assert response.status_code == 400


def test_create_user_bulk_200(test_client, guacapy_client_mock, httpx_mock):
    httpx_mock.add_response(
        method='POST',
        url=ConfigClass.AUTH_SERVICE + 'admin/roles/users',
        json={
            'result': [{'username': 'test'}],
            'total': 1,
        }
    )
    payload = {
        'container_code': 'unittest',
        'username': 'unittest',
    }
    response = test_client.post('/v1/guacamole/project/users', json=payload)
    assert response.status_code == 200


def test_create_user_existing_users_200(test_client, guacapy_client_mock_add_user_400, httpx_mock):
    httpx_mock.add_response(
        method='POST',
        url=ConfigClass.AUTH_SERVICE + 'admin/roles/users',
        json={
            'result': [{'username': 'test'}],
            'total': 1,
        }
    )
    payload = {
        'container_code': 'unittest',
        'username': 'unittest',
    }
    response = test_client.post('/v1/guacamole/project/users', json=payload)
    assert response.status_code == 200


def test_create_user_multiple_pages_200(test_client, guacapy_client_mock, httpx_mock):
    httpx_mock.add_response(
        method='POST',
        url=ConfigClass.AUTH_SERVICE + 'admin/roles/users',
        json={
            'result': [{'username': 'test'}],
            'total': 30,
        }
    )
    payload = {
        'container_code': 'unittest',
        'username': 'unittest',
    }
    response = test_client.post('/v1/guacamole/project/users', json=payload)
    assert response.status_code == 200
