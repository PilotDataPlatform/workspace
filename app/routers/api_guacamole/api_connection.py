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
from common import LoggerFactory
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from guacapy import Guacamole
from requests.exceptions import HTTPError

from app.config import ConfigClass
from app.models.base import APIResponse
from app.models.models_connection import (
    DeleteConnection,
    DeleteConnectionResponse,
    GetConnection,
    GetConnectionResponse,
    PostConnection,
)
from app.resources.error_handler import APIException
from app.routers.api_guacamole.utils import format_connection_name

router = APIRouter()
API_TAG = 'Connection'


@cbv(router)
class Connection:
    logger = LoggerFactory('api_guacamole').get_logger()

    @router.get(
        '/guacamole/connection',
        summary='Get a connection by container_code',
        tags=[API_TAG],
        response_model=GetConnectionResponse,
    )
    def get(self, data: GetConnection = Depends(GetConnection)):
        guacamole_client = Guacamole(
            hostname=ConfigClass.GUACAMOLE_HOSTNAME,
            username=ConfigClass.GUACAMOLE_USERNAME,
            password=ConfigClass.GUACAMOLE_PASSWORD,
            url_path=ConfigClass.GUACAMOLE_URL_PATH,
        )
        connection = guacamole_client.get_connection_by_name(format_connection_name(data.container_code))
        api_response = GetConnectionResponse()
        api_response.result = {
            'id': connection['identifier'],
            'name': connection['name'],
            'protocol': connection['protocol'],
        }
        return api_response.json_response()

    @router.post('/guacamole/connection', summary='Add a new connection', tags=[API_TAG])
    def post(self, data: PostConnection):
        guacamole_client = Guacamole(
            hostname=ConfigClass.GUACAMOLE_HOSTNAME,
            username=ConfigClass.GUACAMOLE_USERNAME,
            password=ConfigClass.GUACAMOLE_PASSWORD,
            url_path=ConfigClass.GUACAMOLE_URL_PATH,
        )
        connection_name = format_connection_name(data.container_code)
        payload = {
            'name': connection_name,
            'parentIdentifier': 'ROOT',
            'protocol': 'ssh',
            'parameters': {
                'port': data.port,
                'hostname': data.hostname,
            },
            'attributes': {},
        }
        try:
            result = guacamole_client.add_connection(payload)
        except HTTPError as e:
            self.logger.error(f'Error adding guacamole connection: {e}')
            raise APIException(
                status_code=e.response.status_code, error_msg=f'Error adding guacamole connection: {e.response.json()}'
            )
        response = APIResponse()
        response.result = result
        return response.json_response()

    @router.delete(
        '/guacamole/connection',
        summary='Get a connection by container_code',
        tags=[API_TAG],
        response_model=DeleteConnectionResponse,
    )
    def delete(self, data: DeleteConnection = Depends(DeleteConnection)):
        guacamole_client = Guacamole(
            hostname=ConfigClass.GUACAMOLE_HOSTNAME,
            username=ConfigClass.GUACAMOLE_USERNAME,
            password=ConfigClass.GUACAMOLE_PASSWORD,
            url_path=ConfigClass.GUACAMOLE_URL_PATH,
        )
        connection = guacamole_client.get_connection_by_name(format_connection_name(data.container_code))
        try:
            guacamole_client.delete_connection(connection['identifier'])
        except HTTPError as e:
            self.logger.error(f'Erroring deleting guacamole connection: {e}')
            raise APIException(
                status_code=e.response.status_code, error_msg='Error deleting guacamole connection: {e.response.json()}'
            )
        api_response = APIResponse()
        api_response.result = 'success'
        return api_response.json_response()