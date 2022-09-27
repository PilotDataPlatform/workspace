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
from fastapi import FastAPI

from .routers import api_root
from .routers.api_guacamole import api_connection, api_permission
from .routers.api_health import api_health


def api_registry(app: FastAPI):
    app.include_router(api_health.router, prefix='/v1')
    app.include_router(api_root.router, prefix='/v1')
    app.include_router(api_connection.router, prefix='/v1')
    app.include_router(api_permission.router, prefix='/v1')
