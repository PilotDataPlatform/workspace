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

import pytest
from fastapi.testclient import TestClient
from requests.exceptions import HTTPError

from app.main import create_app

GUACAMOLE_CONNECTION = {'identifier': '3', 'name': 'lxd_test', 'parentIdentifier': 'ROOT', 'protocol': 'ssh'}

GUACAMOLE_PERMISSION = {
    'connectionPermissions': {
        '3': [
            'READ',
            'UPDATE',
            'DELETE',
        ],
    }
}


def guacapy_mock(mocker, response_code=204, connection_exception=False, init_exception=False, add_user_exception=False):
    class MockResponse:
        def __init__(self, response_code=response_code):
            self.status_code = response_code

        def json(self):
            return {}

    class GuacapyClientMock:
        def __init__(self, *args, **kwargs):
            if init_exception:
                response = MockResponse(response_code=503)
                raise HTTPError('', 503, 'Testing', response=response)

        def get_connections(self, *args, **kwargs):
            return {
                'childConnections': [GUACAMOLE_CONNECTION]
            }

        def get_connection_by_name(self, *args, **kwargs):
            return GUACAMOLE_CONNECTION

        def add_connection(self, *args, **kwargs):
            if connection_exception:
                response = MockResponse(response_code=400)
                raise HTTPError('', 400, 'Testing', response=response)
            return GUACAMOLE_CONNECTION

        def get_permissions(self, *args, **kwargs):
            return GUACAMOLE_PERMISSION

        def grant_permission(self, *args, **kwargs):
            return MockResponse(response_code=response_code)

        def delete_connection(self, *args, **kwargs):
            if connection_exception:
                response = MockResponse(response_code=400)
                raise HTTPError('', 400, 'Testing', response=response)
            return MockResponse(response_code=response_code)

        def add_user(self, *args, **kwargs):
            if add_user_exception:
                return {"type": "BAD_REQUEST"}
            return {}

    mocker.patch('app.commons.guacamole_client.Guacamole', GuacapyClientMock)


@pytest.fixture
def guacapy_client_mock_connection_except(mocker):
    guacapy_mock(mocker, connection_exception=True)


@pytest.fixture
def guacapy_client_mock_grant_permission_400(mocker):
    guacapy_mock(mocker, response_code=400)


@pytest.fixture
def guacapy_client_mock_no_connection(mocker):
    guacapy_mock(mocker, init_exception=True, response_code=503)

@pytest.fixture
def guacapy_client_mock_add_user_400(mocker):
    guacapy_mock(mocker, add_user_exception=True, response_code=503)


@pytest.fixture
def guacapy_client_mock(mocker):
    guacapy_mock(mocker)


@pytest.fixture
def test_client():
    app = create_app()
    client = TestClient(app)
    return client
