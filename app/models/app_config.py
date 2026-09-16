from sqlalchemy import Column, JSON
from app.models.base import BaseModel

class AppConfig(BaseModel):
    __tablename__ = "app_configs"
    schema_version = Column(JSON, default=dict)
    theme = Column(JSON, default=dict)
    navigation = Column(JSON, default=dict)

