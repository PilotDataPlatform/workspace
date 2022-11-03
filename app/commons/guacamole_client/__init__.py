from guacapy import Guacamole

from app.config import ConfigClass
from app.models.base import EAPIResponseCode
from app.resources.error_handler import APIException


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
