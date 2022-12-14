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
from pydantic import BaseModel, Field

from app.models.base import APIResponse


class GetConnection(BaseModel):
    container_code: str


class GetConnectionResponse(APIResponse):
    result: dict = Field({}, example={'id': '9', 'name': 'workspace_indoctestproject', 'protocol': 'ssh'})


class PostConnection(BaseModel):
    container_code: str
    connection_name: str = ""
    username: str
    port: int
    hostname: str


class DeleteConnection(BaseModel):
    container_code: str
    connection_name: str


class DeleteConnectionResponse(APIResponse):
    result: str = Field("", example="success")
