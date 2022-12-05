from common import LoggerFactory
from guacapy import Guacamole

from app.config import ConfigClass
from app.models.base import EAPIResponseCode
from app.resources.error_handler import APIException

logger = LoggerFactory('api_guacamole').get_logger()


def get_guacamole_client(container_code: str) -> Guacamole:
    try:
        guacamole_client = Guacamole(
            hostname=ConfigClass.GUACAMOLE_HOSTNAME,
            username=ConfigClass.GUACAMOLE_USERNAME,
            password=ConfigClass.GUACAMOLE_PASSWORD,
            url_path=ConfigClass.GUACAMOLE_URL_PATH.format(container_code=container_code),
        )
    except Exception as e:
        raise APIException(
            error_msg=f'Error connecting to guacamole: {e}', status_code=EAPIResponseCode.unavailable.value
        )
    return guacamole_client


def add_users_bulk(users: list[str], container_code: str) -> None:
    for username in users:
        guacamole_client = get_guacamole_client(container_code)
        payload = {
            'username': username,
            'attributes': {
                'access-window-end': None,
                'access-window-start': None,
                'disabled': None,
                'expired': None,
                'guac-email-address': None,
                'guac-full-name': None,
                'guac-organization': None,
                'guac-organizational-role': None,
                'timezone': None,
                'valid-from': None,
                'valid-until': None,
            },
        }
        try:
            guacamole_client.add_user(payload)
        except Exception as e:
            logger.error(f'Error adding user in guacamole: {e}')
