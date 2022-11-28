from pylxd import Client
from pylxd.exceptions import LXDAPIException, NotFound
from app.config import ConfigClass
from app.commons.psql_service import create_lxd_container, delete_instance
from app.resources.error_handler import APIException
from app.models.base import EAPIResponseCode
import time
import random


class LXDClient(Client):

    def __init__(self, *args, **kwargs):
        self.host = ConfigClass.LXD_HOST
        kwargs["endpoint"] = f'https://{self.host}:{str(ConfigClass.LXD_PORT)}'
        kwargs["cert"] = (
            ConfigClass.LXD_CRT,
            ConfigClass.LXD_KEY
        )
        kwargs["verify"] = False
        super().__init__(*args, **kwargs)
        self.authenticate(ConfigClass.LXD_TRUST_PASSWORD)

    async def get_network(self):
        return self.networks.get(ConfigClass.LXD_NETWORK)

    async def get_available_port(self):
        retry = 5
        while retry:
            port = random.randrange(ConfigClass.PORT_RANGE_LOWER, ConfigClass.PORT_RANGE_UPPER)
            forward = await self.get_network_forward()
            used_ports = [i['listen_port'] for i in forward.ports]
            if port in used_ports:
                retry -= 1
                if retry == 0:
                    raise APIException(
                        error_msg="Unable to find free port",
                        status_code=EAPIResponseCode.internal_error.value
                    )
                continue
            break
        return port

    async def create_instance_and_network_forward(self, config: dict, username: str, project_code: str):
        instance = self.instances.create(config, wait=True)
        instance.start(wait=True)
        ipv4 = None
        retry = 0
        while not ipv4 and retry < 5:
            network = instance.state().network
            addresses = network.get("eth0")["addresses"]
            for address in addresses:
                if address.get("family") == "inet":
                    ipv4 = address["address"]
            if not ipv4:
                time.sleep(2)
                retry += 1

        for port in [22, 3389]:
            listen_port = await self.get_available_port()
            new_port = {
                "description": f"{instance.name} network forward",
                "listen_port": str(listen_port),
                "target_port": str(port),
                "protocol": "tcp",
                "target_address": ipv4,
            }
            network = await self.get_network()
            forward = network.forwards.get(self.host)
            ports = forward.ports
            ports.append(new_port)
            forward.ports = ports
            forward.save()

        #create_lxd_container({
        #    "username": username,
        #    "project_code": project_code,
        #    "target_port": target_port,
        #    "listen_port": listen_port,
        #    "target_address": ipv4,
        #    "listen_address": self.host,
        #})
        return 'success'

    async def get_instance_address(self, instance) -> str:
        if instance.state().network:
            addresses = instance.state().network.get("eth0")["addresses"]
            for address in addresses:
                if address.get("family") == "inet":
                    return address["address"]
        return None

    async def stop_and_delete_instance(self, instance):
        project_code, username = instance.name.split("-")
        address = await self.get_instance_address(instance)
        forward = await self.get_network_forward()
        new_port_data = []
        for port_data in forward.ports:
            if port_data['target_address'] != address:
                new_port_data.append(port_data)
        forward.ports = new_port_data
        forward.save()

        try:
            instance.stop(wait=True)
        except LXDAPIException:
            # Already stopped
            pass
        instance.delete(wait=True)
        #delete_instance(username, project_code)

    async def get_network_forward(self):
        network = await self.get_network()
        try:
            forward = network.forwards.get(self.host)
        except NotFound:
            return []
        return forward

    async def create_network_forward(self):
        """ Create a network forward without any ports assigned """
        network = self.get_network()
        config = {
            "config": {},
            "description": "workspace test",
            "listen_address": self.host,
            "ports": []
        }
        forward = network.forwards.create(config=config, wait=True)
        return forward
