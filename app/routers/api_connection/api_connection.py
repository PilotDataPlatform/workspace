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
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from common import LoggerFactory
from app.models.models_connection import GetConnection, GetConnectionResponse, PostConnection
from app.config import ConfigClass
from app.resources.error_handler import APIException
from guacapy import Guacamole
from app.routers.api_connection.utils import format_connection_name
from requests.exceptions import HTTPError
from app.models.base import APIResponse


router = APIRouter()
API_TAG = 'Connection'


@cbv(router)
class Connection:
    _logger = LoggerFactory('api_connection').get_logger()

    @router.get(
        '/guacamole/connection',
        summary='Get a connection by container_code',
        tags=[API_TAG],
        response_model=GetConnectionResponse
    )
    def get(self, data: GetConnection = Depends(GetConnection)):
        guacamole_client = Guacamole(
            hostname=ConfigClass.GUACAMOLE_HOSTNAME,
            username=ConfigClass.GUACAMOLE_USERNAME,
            password=ConfigClass.GUACAMOLE_PASSWORD,
            url_path=ConfigClass.GUACAMOLE_URL_PATH
        )
        connection = guacamole_client.get_connection_by_name(format_connection_name(data.container_code))
        api_response = GetConnectionResponse()
        api_response.result = connection
        return api_response.json_response()

    @router.post(
        '/guacamole/connection',
        summary='Add a new connection',
        tags=[API_TAG]
    )
    def post(self, data: PostConnection):
        guacamole_client = Guacamole(
            hostname=ConfigClass.GUACAMOLE_HOSTNAME,
            username=ConfigClass.GUACAMOLE_USERNAME,
            password=ConfigClass.GUACAMOLE_PASSWORD,
            url_path=ConfigClass.GUACAMOLE_URL_PATH
        )
        connection_name = format_connection_name(data.container_code)
        payload = {
            "name": connection_name,
            "parentIdentifier": "ROOT",
            "protocol": "ssh",
            "parameters": {
                "port": data.port,
                "hostname": data.hostname,
            },
            "attributes": {},
        }
        try:
            result = guacamole_client.add_connection(payload)
        except HTTPError as e:
            raise APIException(
                status_code=e.response.status_code,
                error_msg=f"Error adding guacamole connection: {e.response.json()}"
            )
        response = APIResponse()
        response.result = result
        return response.json_response()
