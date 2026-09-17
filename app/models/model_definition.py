from sqlalchemy import Column, String, JSON, Integer, Boolean
from app.models.base import BaseModel

class ModelDefinition(BaseModel):
    __tablename__ = "model_definitions"
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    label = Column(String)
    description = Column(String)
    fields = Column(JSON, default=list)
    is_published = Column(Boolean, default=False)
    version = Column(Integer, default=1)

