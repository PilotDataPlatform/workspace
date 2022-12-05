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
from pydantic import BaseModel, Field, validator

from app.models.base import APIResponse, EAPIResponseCode
from app.resources.error_handler import APIException


class GetPermission(BaseModel):
    container_code: str
    username: str


class GetPermissionResponse(APIResponse):
    result: dict = Field({}, example={})


class PostPermission(BaseModel):
    connection_name: str
    container_code: str
    username: str
    permissions: list[str]
    operation: str

    @validator('operation')
    def validate_operation(cls, v):
        if v not in ['add', 'remove']:
            raise APIException(error_msg='Invalid operation', status_code=EAPIResponseCode.bad_request)
        return v


class CreateUser(BaseModel):
    container_code: str
    username: str


class CreateUserResponse(APIResponse):
    result: dict = Field("", example="success")


class CreateUserBulk(BaseModel):
    container_code: str


class CreateUserBulkResponse(APIResponse):
    result: dict = Field("", example="success")
