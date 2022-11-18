from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LXDContainerModel(Base):
    __tablename__ = 'lxd_container'
    __table_args__ = {'schema': 'public'}
    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    project_code = Column(String())
    username = Column(String())
    project_code = Column(String())
    listen_address = Column(String())
    target_address = Column(String())
    listen_port = Column(Integer())
    target_port = Column(Integer())
    created_at = Column(DateTime(), default=datetime.utcnow)

    def to_dict(self):
        result = {}
        field_list = [
            'id',
            'username',
            'project_code',
            'listen_address',
            'target_address',
            'listen_port',
            'target_port',
            'created_at',
        ]
        for field in field_list:
            if field not in ['created_at']:
                result[field] = str(getattr(self, field))
            else:
                result[field] = getattr(self, field)
        return result
