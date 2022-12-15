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
from functools import lru_cache
from typing import Any, Dict, Optional

from common import VaultClient
from pydantic import BaseSettings, Extra


class VaultConfig(BaseSettings):
    """Store vault related configuration."""

    APP_NAME: str = 'service_auth'
    CONFIG_CENTER_ENABLED: bool = False

    VAULT_URL: Optional[str]
    VAULT_CRT: Optional[str]
    VAULT_TOKEN: Optional[str]

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def load_vault_settings(settings: BaseSettings) -> Dict[str, Any]:
    config = VaultConfig()

    if not config.CONFIG_CENTER_ENABLED:
        return {}
    client = VaultClient(config.VAULT_URL, config.VAULT_CRT, config.VAULT_TOKEN)
    return client.get_from_vault(config.APP_NAME)


class Settings(BaseSettings):
    version = '0.1.0'
    APP_NAME: str = 'workspace_service'
    HOST: str = '0.0.0.0'
    PORT: int = 5068

    WORKSPACE_PREFIX: str = 'workspace'

    GUACAMOLE_HOSTNAME: str
    GUACAMOLE_USERNAME: str
    GUACAMOLE_PASSWORD: str
    GUACAMOLE_URL_PATH: str

    LXD_TRUST_PASSWORD: str
    LXD_CRT: str
    LXD_KEY: str
    LXD_HOST: str
    LXD_PORT: str = 8443
    LXD_NETWORK: str = 'lxdbr0'
    LXD_IMAGE_CONFIG: dict = {
        'type': 'image',
        'alias': 'indoc_ubuntu_22_04_xfce4',
    }
    LXD_LISTEN_ADDRESS: str

    PORT_RANGE_LOWER: int = 9000
    PORT_RANGE_UPPER: int = 9500

    RDS_HOST: str = "127.0.0.1"
    RDS_PORT: str = "5432"
    RDS_DBNAME: str = "workspace"
    RDS_USERNAME: str
    RDS_PASSWORD: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return env_settings, load_vault_settings, init_settings, file_secret_settings

    def __init__(self, *args: Any, **kwds: Any) -> None:
        super().__init__(*args, **kwds)
        self.RDS_DB_URI = (
            f"postgresql://{self.RDS_USERNAME}:{self.RDS_PASSWORD}"
            f"@{self.RDS_HOST}:{self.RDS_PORT}/{self.RDS_DBNAME}"
        )


@lru_cache(1)
def get_settings():
    settings = Settings()
    return settings


ConfigClass = get_settings()
