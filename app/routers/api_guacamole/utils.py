from app.config import ConfigClass


def format_connection_name(container_code: str):
    return ConfigClass.WORKSPACE_PREFIX + '_' + container_code
