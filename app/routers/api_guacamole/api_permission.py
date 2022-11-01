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
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from guacapy import Guacamole

from app.config import ConfigClass
from app.models.models_permission import (GetPermission, GetPermissionResponse,
                                          PostPermission)
from app.resources.error_handler import APIException

router = APIRouter()
API_TAG = 'Permission'


@cbv(router)
class Permission:
    logger = LoggerFactory('api_permisison').get_logger()

    @router.get(
        '/guacamole/permission',
        summary='Get permissons on a connection for a user',
        tags=[API_TAG],
        response_model=GetPermissionResponse,
    )
    def get(self, data: GetPermission = Depends(GetPermission)):
        guacamole_client = Guacamole(
            hostname=ConfigClass.GUACAMOLE_HOSTNAME,
            username=ConfigClass.GUACAMOLE_USERNAME,
            password=ConfigClass.GUACAMOLE_PASSWORD,
            url_path=ConfigClass.GUACAMOLE_URL_PATH.format(container_code=data.container_code),
        )
        connections = guacamole_client.get_connections()
        permissions = guacamole_client.get_permissions(data.username)
        result = {}
        for connection in connections['childConnections']:
            result[connection['name']] = permissions['connectionPermissions'].get(connection['identifier'], [])
        api_response = GetPermissionResponse()
        api_response.result = {'container_code': data.container_code, 'permissions': result}
        return api_response.json_response()

    @router.post('/guacamole/permission', summary='Add permissions for a user on a connection', tags=[API_TAG])
    def post(self, data: PostPermission):
        guacamole_client = Guacamole(
            hostname=ConfigClass.GUACAMOLE_HOSTNAME,
            username=ConfigClass.GUACAMOLE_USERNAME,
            password=ConfigClass.GUACAMOLE_PASSWORD,
            url_path=ConfigClass.GUACAMOLE_URL_PATH.format(container_code=data.container_code),
        )
        connection = guacamole_client.get_connection_by_name(data.connection_name)
        connection_id = connection['identifier']
        payload = []
        for permission in data.permissions:
            payload.append(
                {
                    'op': data.operation,
                    'path': f'/connectionPermissions/{connection_id}',
                    'value': permission,
                }
            )
        response = guacamole_client.grant_permission(data.username, payload)
        if response.status_code != 204:
            self.logger.error(f'Erroring updating guacamole permissions: {response}')
            raise APIException(
                status_code=response.status_code, error_msg='Error updating guacamole permisisons: {response.json()}'
            )
        return JSONResponse('success')
