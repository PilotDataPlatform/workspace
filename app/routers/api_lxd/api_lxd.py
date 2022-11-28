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
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from common import LoggerFactory
from app.models.models_lxd import CreateLXD, GetLXD
from app.commons.lxd_client import LXDClient
from app.commons.password import generate_password_hash
from app.config import ConfigClass


router = APIRouter()
API_TAG = 'LXD'


@cbv(router)
class LXDManager:
    _logger = LoggerFactory('api_lxd').get_logger()

    @router.get(
        '/lxd',
        summary='list LXD containers',
        tags=[API_TAG]
    )
    async def get(self, data: GetLXD = Depends(GetLXD)):
        lxd_client = LXDClient()
        containers = lxd_client.instances.all()
        forward = await lxd_client.get_network_forward()
        search_name = f"{data.container_code}-{data.username}"
        api_response = ""
        for container in containers:
            if container.name == search_name:
                container_data = {
                    "name": container.name,
                    "status": container.status,
                    "port_forward": []
                }
                host = await lxd_client.get_instance_address(container)
                for port_data in forward.ports:
                    if port_data['target_address'] == host:
                        container_data['port_forward'].append({
                            'listen_port': port_data['listen_port'],
                            'target_port': port_data['target_port'],
                            'listen_address': forward.listen_address,
                            'target_address': port_data['target_address'],
                        })
                api_response = container_data
                break
        return JSONResponse(api_response)

    @router.post(
        '/lxd',
        summary='Launch a new LXD container',
        tags=[API_TAG]
    )
    async def post(self, data: CreateLXD, background_tasks: BackgroundTasks):
        lxd_client = LXDClient()
        container_name = f"{data.container_code}-{data.username}"
        password, password_hash = generate_password_hash()
        with open('lxd_cloud_init.yaml', 'r') as f:
            cloud_init_data = f.read()

        config = {
            'name': container_name,
            'type': 'container',
            'source': ConfigClass.LXD_IMAGE_CONFIG,
            'config': {
                'user.meta-data': f'password: {password_hash}',
                'user.user-data': cloud_init_data.format(password_hash=password_hash),
            }
        }

        #background_tasks.add_task(lxd_client.create_instance_and_network_forward, config)
        await lxd_client.create_instance_and_network_forward(config, data.username, data.container_code)
        api_response = {
            "container_name": container_name,
            "password": password,
        }
        return JSONResponse(api_response)

    @router.delete(
        '/lxd',
        summary='delete a LXD container',
        tags=[API_TAG]
    )
    async def delete(self, data: CreateLXD, background_tasks: BackgroundTasks):
        lxd_client = LXDClient()
        container_name = f"{data.container_code}-{data.username}"
        instance = lxd_client.instances.get(container_name)
        #background_tasks.add_task(lxd_client.stop_and_delete_instance, instance)
        await lxd_client.stop_and_delete_instance(instance)
        api_response = {
            "result": "success",
        }
        return JSONResponse(api_response)
