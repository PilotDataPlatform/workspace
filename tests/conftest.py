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


def guacapy_mock(mocker, response_code=204, connection_exception=False):
    class MockResponse:
        def __init__(self, response_code=response_code):
            self.status_code = response_code

        def json(self):
            return {}

    class GuacapyClientMock:
        def __init__(self, *args, **kwargs):
            pass

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

    mocker.patch('app.routers.api_guacamole.api_connection.Guacamole', GuacapyClientMock)
    mocker.patch('app.routers.api_guacamole.api_permission.Guacamole', GuacapyClientMock)


@pytest.fixture
def guacapy_client_mock_connection_except(mocker):
    guacapy_mock(mocker, connection_exception=True)


@pytest.fixture
def guacapy_client_mock_grant_permission_400(mocker):
    guacapy_mock(mocker, response_code=400)


@pytest.fixture
def guacapy_client_mock(mocker):
    guacapy_mock(mocker)


@pytest.fixture
def test_client():
    app = create_app()
    client = TestClient(app)
    return client
