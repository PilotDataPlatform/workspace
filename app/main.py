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
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import DBSessionMiddleware

from app.routers import api_root
from app.routers.api_guacamole import api_connection, api_permission
from app.routers.api_health import api_health
from app.routers.api_lxd import api_lxd

from app.resources.error_handler import APIException

from .config import ConfigClass


def create_app():
    """create app function."""
    app = FastAPI(
        title='Service Workspaces',
        description='Service Workspaces',
        docs_url='/v1/api-doc',
        version=ConfigClass.version,
    )

    app.add_middleware(DBSessionMiddleware, db_url=ConfigClass.RDS_DB_URI)
    app.add_middleware(
        CORSMiddleware,
        allow_origins='*',
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    setup_routers(app)

    @app.exception_handler(APIException)
    async def http_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.content,
        )
    return app


def setup_routers(app: FastAPI) -> None:
    app.include_router(api_health.router, prefix='/v1')
    app.include_router(api_root.router, prefix='/v1')
    app.include_router(api_connection.router, prefix='/v1')
    app.include_router(api_permission.router, prefix='/v1')
    app.include_router(api_lxd.router, prefix='/v1')
