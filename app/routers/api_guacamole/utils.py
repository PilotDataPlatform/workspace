from app.config import ConfigClass


def format_connection_name(connection_name: str):
    return ConfigClass.WORKSPACE_PREFIX + '_' + connection_name
