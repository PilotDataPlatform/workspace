# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import random

from fastapi_sqlalchemy import db

from app.models.sql_lxd import LXDContainerModel
from app.config import ConfigClass


def get_available_port():
    retry = 5
    while retry:
        port = random.randrange(ConfigClass.PORT_RANGE_LOWER, ConfigClass.PORT_RANGE_UPPER)
        if db.session.query(LXDContainerModel).filter_by(listen_port=port).count():
            retry -= 1
            continue
        break
    return port


def create_lxd_container(data: dict) -> LXDContainerModel:
    lxd_container = LXDContainerModel(
        username=data['username'],
        project_code=data['project_code'],
        listen_address=data['listen_address'],
        target_address=data['target_address'],
        target_port=data['target_port'],
        listen_port=data['listen_port']
    )
    db.session.add(lxd_container)
    db.session.commit()
    return lxd_container


def search_instance(data: dict) -> list[LXDContainerModel]:
    return db.session.query(LXDContainerModel).filter_by(**data).all()


def delete_instance(username: str, project_code: str):
    entry = db.session.query(LXDContainerModel).filter_by(username=username, project_code=project_code).first()
    db.session.delete(entry)
    db.session.commit()
